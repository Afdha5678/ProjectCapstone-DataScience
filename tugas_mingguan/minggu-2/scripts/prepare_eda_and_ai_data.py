"""
Minggu 2 - Tahap 1:
1. Ekstraksi statistik EDA operasional dari ales_place_dwh.db (untuk menjawab pertanyaan bisnis).
2. Penyusunan dataset deret waktu siap-AI untuk tim AE (Ayunda & Faris):
   - Reindexing kalender penuh (2025-10-01 s.d. 2026-10-31, 396 hari kalender)
   - Feature engineering kausal (tanpa data leakage)
   - Pembagian train (Okt 2025 - Sep 2026) & test (Okt 2026)
   - Pelabelan transparan data primer vs keterbatasan cakupan resep 2018 (59.0%)

Output di tugas_mingguan/minggu-2/output/data_for_ai/ :
  - daily_usage_full_features.csv
  - train_daily_usage.csv
  - test_daily_usage.csv
  - ingredient_burn_rate_summary.csv
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

MINGGU_2_DIR = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[3]
DWH_PATH = WORKSPACE / "tugas_mingguan" / "minggu-1" / "output" / "data_penjualan" / "ales_place_dwh.db"
AI_OUT_DIR = MINGGU_2_DIR / "output" / "data_for_ai"

CLOSED_DATES = {"2026-03-21"}  # Idul Fitri 2026 (0 transaksi di seluruh hari)


def compute_eda_insights(conn: sqlite3.Connection) -> None:
    """Cetak metrik EDA operasional terverifikasi untuk dokumentasi bisnis."""
    df_tx = pd.read_sql("SELECT * FROM fact_transaksi", conn)
    df_it = pd.read_sql("SELECT * FROM fact_penjualan_item", conn)
    df_usage = pd.read_sql("SELECT * FROM v_pemakaian_bahan_harian", conn)
    df_ing = pd.read_sql("SELECT * FROM dim_bahan_baku", conn)

    print("=== EDA RINGKASAN TRANSAKSI & OPERASIONAL ===")
    print(f"Total transaksi              : {len(df_tx):,}")
    print(f"Transaksi eksternal          : {(df_tx['is_internal_order'] == 0).sum():,}")
    print(f"Transaksi internal (crew/own): {(df_tx['is_internal_order'] == 1).sum():,}")
    print(f"Total omzet grand_total (all): Rp {df_tx['grand_total'].sum():,.0f}")
    ext_rev = df_tx.loc[df_tx["is_internal_order"] == 0, "grand_total"].sum()
    print(f"Total omzet eksternal        : Rp {ext_rev:,.0f}")

    # Weekday vs Weekend traffic
    df_tx["dt"] = pd.to_datetime(df_tx["tanggal"])
    df_tx["dow"] = df_tx["dt"].dt.dayofweek
    df_tx["is_weekend"] = df_tx["dow"].isin([4, 5, 6])  # Jum, Sab, Min
    daily_tx = df_tx.groupby(["tanggal", "is_weekend"]).agg(
        tx_cnt=("id_transaksi", "count"),
        omzet=("grand_total", "sum"),
    ).reset_index()
    print("\n--- Weekday (Sen-Kam) vs Weekend (Jum-Min) ---")
    print(daily_tx.groupby("is_weekend")[["tx_cnt", "omzet"]].mean().round(2).to_string())

    # Peak hours
    print("\n--- Top 5 Jam Tersibuk (Jumlah Transaksi) ---")
    print(df_tx["jam"].value_counts().head(5).to_string())

    # Channel distribution
    print("\n--- Distribusi Channel Penjualan ---")
    ch = df_tx.groupby("channel_penjualan").agg(
        tx=("id_transaksi", "count"),
        omzet=("grand_total", "sum"),
    ).sort_values("tx", ascending=False)
    print(ch.to_string())

    # Monthly trend
    df_tx["bulan"] = df_tx["tanggal"].str.slice(0, 7)
    print("\n--- Tren Bulanan (Transaksi & Omzet) ---")
    print(df_tx.groupby("bulan").agg(tx=("id_transaksi", "count"), omzet=("grand_total", "sum")).to_string())

    # Internal vs External ingredient consumption
    df_bom = pd.read_sql("SELECT id_menu, id_bahan, jumlah_pemakaian, estimasi_biaya_bahan FROM fact_resep_bom", conn)
    merged = df_it.merge(df_tx[["id_transaksi", "is_internal_order"]], on="id_transaksi", how="left")
    merged_bom = merged.dropna(subset=["id_menu_resep"]).merge(
        df_bom, left_on="id_menu_resep", right_on="id_menu", how="inner"
    )
    merged_bom["used_qty"] = merged_bom["qty"] * merged_bom["jumlah_pemakaian"]
    merged_bom["used_cost"] = merged_bom["qty"] * merged_bom["estimasi_biaya_bahan"]
    int_cost = merged_bom.groupby("is_internal_order")["used_cost"].sum()
    print("\n--- Estimasi HPP Pemakaian Bahan (Eksternal vs Internal) ---")
    print(int_cost.round(0).to_string())

    # Top 15 ingredients by total HPP & active burn rate
    top_ing = (
        df_usage.groupby(["id_bahan", "nama_bahan", "satuan_dasar"])
        .agg(total_pemakaian=("total_pemakaian", "sum"), total_hpp=("estimasi_hpp", "sum"))
        .reset_index()
        .sort_values("total_hpp", ascending=False)
    )
    print("\n--- Top 15 Bahan Baku Berdasarkan Estimasi Biaya Pemakaian (395 Hari Aktif) ---")
    top_ing["rata2_harian_395d"] = (top_ing["total_pemakaian"] / 395.0).round(2)
    print(top_ing.head(15)[["nama_bahan", "satuan_dasar", "total_pemakaian", "rata2_harian_395d", "total_hpp"]].to_string(index=False))

    # Unused ingredients count
    used_ids = set(df_usage["id_bahan"].unique())
    print(f"\nBahan baku aktif terpakai di penjualan: {len(used_ids)} / {len(df_ing)}")


def build_ai_ready_datasets(conn: sqlite3.Connection) -> None:
    """Bangun dataset time-series siap latih/uji untuk tim AE tanpa data leakage."""
    AI_OUT_DIR.mkdir(parents=True, exist_ok=True)

    df_usage = pd.read_sql("SELECT * FROM v_pemakaian_bahan_harian", conn)
    df_ing = pd.read_sql(
        """
        SELECT DISTINCT b.id_bahan, b.nama_bahan, b.kategori_vendor, b.satuan_dasar,
               b.isi_kemasan_beli, b.harga_beli_kemasan, b.harga_satuan_dasar, b.is_packaging
        FROM dim_bahan_baku b
        JOIN fact_resep_bom r ON b.id_bahan = r.id_bahan
        ORDER BY b.id_bahan
        """,
        conn,
    )

    all_dates = pd.date_range("2025-10-01", "2026-10-31", freq="D")
    date_strs = [d.strftime("%Y-%m-%d") for d in all_dates]

    # Full cartesian product: 396 days x active BOM ingredients
    grid = pd.MultiIndex.from_product(
        [date_strs, df_ing["id_bahan"].tolist()], names=["tanggal", "id_bahan"]
    ).to_frame(index=False)

    df_full = grid.merge(
        df_usage[["tanggal", "id_bahan", "total_pemakaian", "estimasi_hpp"]],
        on=["tanggal", "id_bahan"],
        how="left",
    ).merge(df_ing, on="id_bahan", how="left")

    df_full["total_pemakaian"] = df_full["total_pemakaian"].fillna(0.0).round(4)
    df_full["estimasi_hpp"] = df_full["estimasi_hpp"].fillna(0.0).round(2)
    df_full["is_store_closed"] = df_full["tanggal"].isin(CLOSED_DATES).astype(int)

    # Calendar & domain features (diketahui sebelum hari H, aman dari data leakage)
    dt = pd.to_datetime(df_full["tanggal"])
    df_full["day_of_week"] = dt.dt.dayofweek  # 0=Senin .. 6=Minggu
    df_full["is_weekend"] = df_full["day_of_week"].isin([4, 5, 6]).astype(int)
    df_full["day_of_month"] = dt.dt.day
    df_full["month"] = dt.dt.month
    df_full["week_of_year"] = dt.dt.isocalendar().week.astype(int)
    df_full["is_payday_window"] = ((dt.dt.day >= 25) | (dt.dt.day <= 5)).astype(int)
    # Ramadan 1447H approx 18 Feb - 20 Mar 2026 (periode Paket Iftar di data penjualan)
    df_full["is_ramadan_period"] = ((dt >= "2026-02-18") & (dt <= "2026-03-20")).astype(int)

    # Sort before causal lag/rolling computations
    df_full = df_full.sort_values(["id_bahan", "tanggal"]).reset_index(drop=True)
    grp = df_full.groupby("id_bahan")["total_pemakaian"]

    # Causal lags & rolling windows: selalu shift(1) agar TIDAK menggunakan nilai hari t (zero leakage)
    df_full["lag_1"] = grp.shift(1)
    df_full["lag_7"] = grp.shift(7)
    df_full["lag_14"] = grp.shift(14)
    df_full["rolling_mean_7"] = grp.transform(lambda s: s.shift(1).rolling(7, min_periods=1).mean()).round(4)
    df_full["rolling_std_7"] = grp.transform(lambda s: s.shift(1).rolling(7, min_periods=1).std().fillna(0.0)).round(4)
    df_full["rolling_mean_28"] = grp.transform(lambda s: s.shift(1).rolling(28, min_periods=1).mean()).round(4)

    # Label sumber data sesuai Rubrik Penyediaan Data AI #1
    df_full["data_source_label"] = "PRIMARY_NUTACLOUD_X_BOM2018_PARTIAL_59PCT"
    df_full["target_pemakaian"] = df_full["total_pemakaian"]

    # Split anti-leakage berbasis waktu: Train (12 bulan: Okt 2025 - Sep 2026), Test (Okt 2026)
    train_df = df_full[df_full["tanggal"] < "2026-10-01"].copy()
    test_df = df_full[df_full["tanggal"] >= "2026-10-01"].copy()

    df_full.to_csv(AI_OUT_DIR / "daily_usage_full_features.csv", index=False, encoding="utf-8")
    train_df.to_csv(AI_OUT_DIR / "train_daily_usage.csv", index=False, encoding="utf-8")
    test_df.to_csv(AI_OUT_DIR / "test_daily_usage.csv", index=False, encoding="utf-8")

    # Ringkasan burn rate per bahan baku pada 395 hari operasional aktif (tidak termasuk hari tutup libur)
    active_df = df_full[df_full["is_store_closed"] == 0].copy()
    burn = active_df.groupby(["id_bahan", "nama_bahan", "kategori_vendor", "satuan_dasar", "isi_kemasan_beli", "harga_beli_kemasan", "harga_satuan_dasar", "is_packaging"]).agg(
        total_pemakaian_395d=("total_pemakaian", "sum"),
        burn_rate_mean=("total_pemakaian", "mean"),
        burn_rate_std=("total_pemakaian", "std"),
        burn_rate_max=("total_pemakaian", "max"),
    ).reset_index()

    recent_30 = active_df[active_df["tanggal"] >= "2026-10-01"].groupby("id_bahan")["total_pemakaian"].mean().rename("burn_rate_30d")
    wkday = active_df[active_df["is_weekend"] == 0].groupby("id_bahan")["total_pemakaian"].mean().rename("burn_rate_weekday")
    wkend = active_df[active_df["is_weekend"] == 1].groupby("id_bahan")["total_pemakaian"].mean().rename("burn_rate_weekend")

    burn = burn.merge(recent_30, on="id_bahan", how="left").merge(wkday, on="id_bahan", how="left").merge(wkend, on="id_bahan", how="left")
    for c in ["total_pemakaian_395d", "burn_rate_mean", "burn_rate_std", "burn_rate_max", "burn_rate_30d", "burn_rate_weekday", "burn_rate_weekend"]:
        burn[c] = burn[c].round(4)

    burn.to_csv(AI_OUT_DIR / "ingredient_burn_rate_summary.csv", index=False, encoding="utf-8")

    print("\n=== PAKET DATA SIAP-AI (TIM AE) SELESAI ===")
    print(f"Active BOM ingredients : {len(df_ing)}")
    print(f"Full dataset rows      : {len(df_full):,} ({len(date_strs)} hari x {len(df_ing)} bahan)")
    print(f"Train split (Okt25-Sep26): {len(train_df):,} baris")
    print(f"Test split  (Okt 2026)   : {len(test_df):,} baris")
    print(f"Output directory       : {AI_OUT_DIR}")


def main() -> None:
    conn = sqlite3.connect(DWH_PATH)
    try:
        compute_eda_insights(conn)
        build_ai_ready_datasets(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
