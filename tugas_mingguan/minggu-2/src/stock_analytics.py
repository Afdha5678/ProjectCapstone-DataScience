"""
Modul Analitik Stok Bahan Baku: Daily Burn Rate, Safety Stock, Reorder Point, & Days of Inventory (DOI).
Lingkup Kerja: Data Science Specialist (Tim A26-CS218).

Catatan Pembagian Peran:
- Modul ini menangani kalkulasi statistika operasional stok & ambang batas kritis (Safety Stock / DOI)
  sesuai Project Plan Bagian B & C Minggu 2.
- Model ML Forecasting (prediksi deret waktu stok hari berikutnya & REST API inference) dikerjakan
  oleh tim AI Engineer (AE) menggunakan dataset pada `tugas_mingguan/minggu-2/output/data_for_ai/`.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd

MINGGU_2_DIR = Path(__file__).resolve().parents[1]
DEFAULT_BURN_SUMMARY_PATH = MINGGU_2_DIR / "output" / "data_for_ai" / "ingredient_burn_rate_summary.csv"

# Kategori vendor yang cenderung dibelanjakan harian (lead time 1 hari) vs mingguan (3 hari)
FRESH_VENDORS = {"SAYUR", "MITRA DAGING"}


def infer_default_lead_time(kategori_vendor: str, is_packaging: int) -> int:
    """Tentukan lead time belanja default (hari) berdasarkan sifat bahan segar vs kering/kemasan."""
    if int(is_packaging) == 1:
        return 3
    if str(kategori_vendor).strip().upper() in FRESH_VENDORS:
        return 1
    return 2


def classify_stock_status(
    stok_saat_ini: float,
    safety_stock: float,
    reorder_point: float,
    doi_days: float,
    burn_rate: float,
) -> Literal["KRITIS", "MENIPIS", "AMAN", "TIDAK_AKTIF"]:
    """Klasifikasikan status kesehatan stok tiap bahan baku."""
    if burn_rate <= 0:
        return "KRITIS" if stok_saat_ini <= 0 else "TIDAK_AKTIF"
    if stok_saat_ini <= 0 or stok_saat_ini <= safety_stock or doi_days < 1.0:
        return "KRITIS"
    if stok_saat_ini <= reorder_point or doi_days <= 2.0:
        return "MENIPIS"
    return "AMAN"


def evaluate_inventory_health(
    current_stock_df: pd.DataFrame,
    burn_summary_path: Path = DEFAULT_BURN_SUMMARY_PATH,
    z_score: float = 1.65,
    mode_hari: Literal["overall", "weekend", "weekday", "recent_30d"] = "overall",
    lead_time_override: int | None = None,
) -> pd.DataFrame:
    """
    Gabungkan saldo stok saat ini dengan laju pemakaian historis untuk menghasilkan:
    - `daily_burn_rate` & `daily_burn_std`
    - `safety_stock` = Z * sigma * sqrt(Lead Time)
    - `reorder_point` = (Burn Rate * Lead Time) + Safety Stock
    - `days_of_inventory` (DOI) = stok_saat_ini / daily_burn_rate
    - `status_stok` ('KRITIS', 'MENIPIS', 'AMAN', 'TIDAK_AKTIF')
    - `rekomendasi_beli_rop_unit` & `rekomendasi_beli_kemasan` (berbasis ambang batas ROP + target 3 hari aman)
    """
    df_burn = pd.read_csv(burn_summary_path)
    burn_cols = [
        "id_bahan",
        "total_pemakaian_395d",
        "burn_rate_mean",
        "burn_rate_std",
        "burn_rate_30d",
        "burn_rate_weekday",
        "burn_rate_weekend",
    ]
    merged = current_stock_df.merge(df_burn[burn_cols], on="id_bahan", how="left")
    for c in burn_cols[1:]:
        merged[c] = merged[c].fillna(0.0)

    rate_col_map = {
        "overall": "burn_rate_mean",
        "weekend": "burn_rate_weekend",
        "weekday": "burn_rate_weekday",
        "recent_30d": "burn_rate_30d",
    }
    selected_col = rate_col_map[mode_hari]
    merged["daily_burn_rate"] = merged[selected_col].round(4)

    lead_times = []
    safety_stocks = []
    rops = []
    dois = []
    statuses = []
    rop_shortfalls = []
    pack_suggestions = []
    est_costs = []

    for _, r in merged.iterrows():
        lt = (
            int(lead_time_override)
            if lead_time_override is not None
            else infer_default_lead_time(r.get("kategori_vendor", ""), r.get("is_packaging", 0))
        )
        rate = float(r["daily_burn_rate"])
        std = float(r["burn_rate_std"])
        stok = float(r["stok_saat_ini"])
        isi_kemasan = float(r["isi_kemasan_beli"]) if float(r["isi_kemasan_beli"]) > 0 else 1.0
        harga_kemasan = float(r["harga_beli_kemasan"])

        ss = round(z_score * std * math.sqrt(lt), 2) if rate > 0 else 0.0
        rop = round((rate * lt) + ss, 2) if rate > 0 else 0.0

        if rate > 0:
            doi = round(max(0.0, stok) / rate, 2)
        else:
            doi = float("inf") if stok > 0 else 0.0

        status = classify_stock_status(stok, ss, rop, doi, rate)

        # Target stok aman operasional: cukup untuk (Lead Time + 2 hari) + Safety Stock
        target_safe_level = (rate * (lt + 2)) + ss
        shortfall = round(max(0.0, target_safe_level - stok), 2) if status in ("KRITIS", "MENIPIS") else 0.0
        packs_needed = int(math.ceil(shortfall / isi_kemasan)) if shortfall > 0 else 0
        cost = round(packs_needed * harga_kemasan, 0)

        lead_times.append(lt)
        safety_stocks.append(ss)
        rops.append(rop)
        dois.append(doi if math.isfinite(doi) else 999.0)
        statuses.append(status)
        rop_shortfalls.append(shortfall)
        pack_suggestions.append(packs_needed)
        est_costs.append(cost)

    merged["lead_time_hari"] = lead_times
    merged["safety_stock"] = safety_stocks
    merged["reorder_point"] = rops
    merged["days_of_inventory"] = dois
    merged["status_stok"] = statuses
    merged["kebutuhan_restock_dasar"] = rop_shortfalls
    merged["saran_beli_kemasan"] = pack_suggestions
    merged["estimasi_biaya_beli"] = est_costs

    status_rank = {"KRITIS": 0, "MENIPIS": 1, "AMAN": 2, "TIDAK_AKTIF": 3}
    merged["_rank"] = merged["status_stok"].map(status_rank)
    merged = merged.sort_values(["_rank", "days_of_inventory", "daily_burn_rate"], ascending=[True, True, False])
    return merged.drop(columns=["_rank"]).reset_index(drop=True)
