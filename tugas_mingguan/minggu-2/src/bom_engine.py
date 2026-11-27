"""
Modul Algoritma BoM Stock Deduction (Konversi Penjualan Kasir -> Pengurangan Stok Bahan Baku).
Lingkup Kerja: Data Science Specialist (Tim A26-CS218).

Fitur utama:
1. Konversi pesanan menu kasir (atau upload CSV NutaCloud) ke pengurangan bahan baku
   berdasarkan tabel mapping (`map_menu_kasir`) dan komposisi resep (`fact_resep_bom`).
2. Penerapan margin toleransi (*buffer percentage*) untuk mengantisipasi bahan tercecer/waste.
3. Konversi pembelian masuk per kemasan (`isi_kemasan_beli` -> satuan dasar) & perhitungan
   selisih (*variance*) saat pengecekan fisik gudang (*stock opname*).
4. Pembuatan saldo stok simulasi awal dengan pelabelan eksplisit (`is_simulated_stock = True`)
   apabila stok fisik aktual UMKM belum tersedia.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import pandas as pd

MINGGU_2_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = Path(__file__).resolve().parents[3]
DEFAULT_DWH_PATH = WORKSPACE_DIR / "tugas_mingguan" / "minggu-1" / "output" / "data_penjualan" / "ales_place_dwh.db"
DEFAULT_BURN_SUMMARY_PATH = MINGGU_2_DIR / "output" / "data_for_ai" / "ingredient_burn_rate_summary.csv"

OPERATIONAL_ITEM_EXACT = {"Pajak Daerah", "Pembulatan", "Biaya Pengemasan", "Thinwal 450"}
OPERATIONAL_CATEGORIES = {"Alat Makan Tkw", "Perlengkapan"}


@dataclass
class DeductionResult:
    """Hasil terstruktur dari proses pemotongan stok berbasis BoM."""

    deductions_df: pd.DataFrame
    updated_stock_df: pd.DataFrame
    unmapped_items: list[dict[str, Any]] = field(default_factory=list)
    total_portions_processed: float = 0.0
    total_portions_unmapped: float = 0.0
    buffer_waste_pct: float = 0.0


class BoMEngine:
    """Mesin konversi menu penjualan kasir NutaCloud ke pengurangan stok bahan baku."""

    def __init__(self, dwh_path: Path = DEFAULT_DWH_PATH) -> None:
        self.dwh_path = Path(dwh_path)
        self._load_reference_tables()

    def _load_reference_tables(self) -> None:
        conn = sqlite3.connect(self.dwh_path)
        try:
            self.dim_bahan = pd.read_sql("SELECT * FROM dim_bahan_baku ORDER BY id_bahan", conn)
            self.dim_menu = pd.read_sql("SELECT * FROM dim_menu ORDER BY id_menu", conn)
            self.fact_bom = pd.read_sql("SELECT * FROM fact_resep_bom", conn)
            self.map_kasir = pd.read_sql("SELECT * FROM map_menu_kasir", conn)
        finally:
            conn.close()

        # Lookup cepat: nama_item_kasir.lower() -> (id_menu_resep, nama_menu_resep, match_status)
        self.kasir_lookup: dict[str, tuple[Optional[int], Optional[str], str]] = {}
        for _, r in self.map_kasir.iterrows():
            key = str(r["nama_item_kasir"]).strip().lower()
            mid = int(r["id_menu_resep"]) if pd.notna(r["id_menu_resep"]) else None
            mname = str(r["nama_menu_resep"]) if pd.notna(r["nama_menu_resep"]) else None
            self.kasir_lookup[key] = (mid, mname, str(r["match_status"]))

        # Lookup langsung nama_menu sellable -> id_menu
        for _, r in self.dim_menu[self.dim_menu["is_sellable"] == 1].iterrows():
            key = str(r["nama_menu"]).strip().lower()
            if key not in self.kasir_lookup:
                self.kasir_lookup[key] = (int(r["id_menu"]), str(r["nama_menu"]), "MAPPED_DIRECT_MENU")

    def create_simulated_stock(
        self,
        burn_summary_path: Path = DEFAULT_BURN_SUMMARY_PATH,
        coverage_days: float = 7.0,
    ) -> pd.DataFrame:
        """
        Buat tabel stok awal simulasi berdasarkan kebutuhan N hari pemakaian historis.
        Sesuai rubrik Dasbor #4 & AI #1, setiap baris diberi label eksplisit sebagai data simulasi.
        """
        df_stock = self.dim_bahan.copy()
        burn_map: dict[int, float] = {}
        if Path(burn_summary_path).exists():
            df_burn = pd.read_csv(burn_summary_path)
            burn_map = dict(zip(df_burn["id_bahan"].astype(int), df_burn["burn_rate_mean"].astype(float)))

        sim_vals = []
        for _, r in df_stock.iterrows():
            iid = int(r["id_bahan"])
            daily = burn_map.get(iid, 0.0)
            if daily > 0:
                val = round(daily * coverage_days, 2)
                # Bulatkan ke atas ke integer untuk satuan pcs agar realistis
                if r["satuan_dasar"] == "pcs":
                    val = float(max(1, round(val)))
            else:
                # Bahan yang tidak terpakai di BoM aktif diberi saldo 1 kemasan agar tidak langsung nol
                val = float(r["isi_kemasan_beli"]) if r["isi_kemasan_beli"] > 0 else 1.0
            sim_vals.append(val)

        df_stock["stok_saat_ini"] = sim_vals
        df_stock["is_simulated_stock"] = True
        df_stock["data_label"] = f"SIMULASI_{int(coverage_days)}_HARI_HISTORIS"
        return df_stock

    def resolve_menu_id(self, nama_item: str) -> tuple[Optional[int], Optional[str], str]:
        """Cari padanan id_menu resep untuk nama item kasir atau nama menu standar."""
        clean = re.sub(r"\s+", " ", nama_item.split("\n")[0]).strip().lower()
        if clean in self.kasir_lookup:
            return self.kasir_lookup[clean]
        return None, None, "UNREGISTERED_ITEM"

    def deduct_from_sales(
        self,
        sales_items: list[dict[str, Any]] | pd.DataFrame,
        current_stock_df: pd.DataFrame,
        buffer_waste_pct: float = 0.0,
    ) -> DeductionResult:
        """
        Hitung dan terapkan pengurangan stok bahan baku dari daftar item terjual.

        Parameters
        ----------
        sales_items : list of dict or DataFrame
            Wajib memiliki kolom/key `nama_item` (atau `nama_item_bersih`) dan `qty`.
            Opsional `id_menu_resep` jika sudah tersedia.
        current_stock_df : DataFrame
            DataFrame stok bahan baku (minimal kolom `id_bahan`, `nama_bahan`, `satuan_dasar`, `stok_saat_ini`).
        buffer_waste_pct : float, default 0.0
            Margin toleransi waste/ceceran dapur (misal 0.05 untuk +5% pengurangan bahan).
        """
        if buffer_waste_pct < 0 or buffer_waste_pct > 0.5:
            raise ValueError("buffer_waste_pct harus berada di antara 0.0 dan 0.5 (50%).")

        df_in = pd.DataFrame(sales_items) if isinstance(sales_items, list) else sales_items.copy()
        updated_stock = current_stock_df.copy()

        empty_columns = [
            "id_bahan",
            "nama_bahan",
            "satuan_dasar",
            "pemakaian_teoritis",
            "buffer_waste",
            "total_pengurangan",
            "stok_sebelum",
            "stok_sesudah",
        ]
        if df_in.empty:
            return DeductionResult(pd.DataFrame(columns=empty_columns), updated_stock, [], 0.0, 0.0, buffer_waste_pct)

        name_col = "nama_item_bersih" if "nama_item_bersih" in df_in.columns else "nama_item"
        menu_qty_agg: dict[int, float] = {}
        unmapped_agg: dict[tuple[str, str], float] = {}
        processed_qty = 0.0
        unmapped_qty = 0.0

        for _, row in df_in.iterrows():
            qty = float(row["qty"])
            if qty == 0:
                continue
            item_name = str(row[name_col]).strip()

            mid: Optional[int] = None
            status = "MAPPED_EXACT"
            if "id_menu_resep" in df_in.columns and pd.notna(row["id_menu_resep"]):
                mid = int(row["id_menu_resep"])
            else:
                mid, _, status = self.resolve_menu_id(item_name)

            if mid is not None:
                menu_qty_agg[mid] = menu_qty_agg.get(mid, 0.0) + qty
                processed_qty += qty
            else:
                key = (item_name, status)
                unmapped_agg[key] = unmapped_agg.get(key, 0.0) + qty
                unmapped_qty += qty

        unmapped_list = [
            {"nama_item": k[0], "status": k[1], "qty": round(v, 2)}
            for k, v in sorted(unmapped_agg.items(), key=lambda x: -x[1])
            if abs(v) > 0
        ]

        # Agregasi pemakaian bahan via fact_resep_bom (abaikan menu dengan qty neto 0, mis. void penuh)
        order_rows = [{"id_menu": mid, "order_qty": q} for mid, q in menu_qty_agg.items() if abs(q) > 1e-9]
        if not order_rows:
            return DeductionResult(
                pd.DataFrame(columns=empty_columns),
                updated_stock,
                unmapped_list,
                processed_qty,
                unmapped_qty,
                buffer_waste_pct,
            )

        df_orders = pd.DataFrame(order_rows)
        bom_joined = df_orders.merge(self.fact_bom, on="id_menu", how="inner")
        bom_joined["theoretical_qty"] = bom_joined["order_qty"] * bom_joined["jumlah_pemakaian"]

        ing_deduction = (
            bom_joined.groupby("id_bahan", as_index=False)["theoretical_qty"]
            .sum()
            .rename(columns={"theoretical_qty": "pemakaian_teoritis"})
        )
        ing_deduction["pemakaian_teoritis"] = ing_deduction["pemakaian_teoritis"].round(4)
        # Buffer hanya diterapkan pada pemakaian keluar neto positif
        ing_deduction["buffer_waste"] = ing_deduction["pemakaian_teoritis"].apply(
            lambda x: round(x * buffer_waste_pct, 4) if x > 0 else 0.0
        )
        ing_deduction["total_pengurangan"] = (
            ing_deduction["pemakaian_teoritis"] + ing_deduction["buffer_waste"]
        ).round(4)

        stock_before_map = dict(zip(updated_stock["id_bahan"].astype(int), updated_stock["stok_saat_ini"].astype(float)))
        name_map = dict(zip(updated_stock["id_bahan"].astype(int), updated_stock["nama_bahan"]))
        unit_map = dict(zip(updated_stock["id_bahan"].astype(int), updated_stock["satuan_dasar"]))

        ing_deduction["nama_bahan"] = ing_deduction["id_bahan"].map(name_map)
        ing_deduction["satuan_dasar"] = ing_deduction["id_bahan"].map(unit_map)
        ing_deduction["stok_sebelum"] = ing_deduction["id_bahan"].map(stock_before_map).round(4)
        ing_deduction["stok_sesudah"] = (
            ing_deduction["stok_sebelum"] - ing_deduction["total_pengurangan"]
        ).round(4)

        ded_map = dict(zip(ing_deduction["id_bahan"].astype(int), ing_deduction["total_pengurangan"]))
        updated_stock["stok_saat_ini"] = updated_stock.apply(
            lambda r: round(float(r["stok_saat_ini"]) - ded_map.get(int(r["id_bahan"]), 0.0), 4),
            axis=1,
        )

        cols_order = [
            "id_bahan",
            "nama_bahan",
            "satuan_dasar",
            "pemakaian_teoritis",
            "buffer_waste",
            "total_pengurangan",
            "stok_sebelum",
            "stok_sesudah",
        ]
        ing_deduction = ing_deduction[cols_order].sort_values("total_pengurangan", ascending=False).reset_index(drop=True)

        return DeductionResult(
            deductions_df=ing_deduction,
            updated_stock_df=updated_stock,
            unmapped_items=unmapped_list,
            total_portions_processed=round(processed_qty, 2),
            total_portions_unmapped=round(unmapped_qty, 2),
            buffer_waste_pct=buffer_waste_pct,
        )

    def parse_nutacloud_csv(self, source: Any) -> pd.DataFrame:
        """
        Bersihkan file CSV laporan kasir NutaCloud mentah (atau format bersih `fact_penjualan_item.csv`)
        menjadi DataFrame siap-potong stok (`nama_item_bersih`, `qty`, `kategori_kasir`).
        Digunakan untuk fitur unggah file di prototipe Streamlit (Dasbor #3).
        """
        df = pd.read_csv(source)

        # Jika sudah format bersih hasil pipeline Minggu 1
        if {"nama_item_bersih", "qty"}.issubset(df.columns):
            out = df[["nama_item_bersih", "qty"]].copy()
            if "id_menu_resep" in df.columns:
                out["id_menu_resep"] = df["id_menu_resep"]
            if "kategori_kasir" in df.columns:
                out["kategori_kasir"] = df["kategori_kasir"]
            out["qty"] = pd.to_numeric(out["qty"], errors="coerce").fillna(0.0)
            return out

        # Jika format mentah laporan kasir NutaCloud
        required_raw = {"Nomor", "Item", "Qty"}
        if not required_raw.issubset(df.columns):
            raise ValueError(
                "Format CSV tidak dikenali. Pastikan file berasal dari ekspor NutaCloud "
                "(memiliki kolom Nomor, Item, Qty) atau file bersih fact_penjualan_item.csv."
            )

        df = df[~df["Nomor"].astype(str).str.contains("Grand Total", na=False)].copy()
        df["Item_str"] = df["Item"].fillna("").astype(str)
        df["Kategori_str"] = df["Kategori"].fillna("").astype(str).str.strip() if "Kategori" in df.columns else ""

        is_operational = (
            df["Item_str"].str.strip().isin(OPERATIONAL_ITEM_EXACT)
            | df["Item_str"].str.strip().str.startswith("Diskon Final")
            | df["Item_str"].str.strip().str.startswith("Voucher ")
            | df["Kategori_str"].isin(OPERATIONAL_CATEGORIES)
        )
        df_prod = df[~is_operational].copy()
        df_prod["nama_item_bersih"] = (
            df_prod["Item_str"].str.split("\n").str[0].str.replace(r"\s+", " ", regex=True).str.strip()
        )
        df_prod["qty"] = pd.to_numeric(df_prod["Qty"], errors="coerce").fillna(0.0)
        df_prod["kategori_kasir"] = df_prod["Kategori_str"].replace("", "Tanpa Kategori")
        return df_prod[["nama_item_bersih", "kategori_kasir", "qty"]].reset_index(drop=True)

    def apply_stock_in(
        self, current_stock_df: pd.DataFrame, id_bahan: int, jumlah_kemasan: float
    ) -> tuple[pd.DataFrame, dict[str, Any]]:
        """Tambahkan stok berdasarkan jumlah kemasan beli dan konversi otomatis ke satuan dasar."""
        if jumlah_kemasan <= 0:
            raise ValueError("jumlah_kemasan harus lebih besar dari 0.")
        updated = current_stock_df.copy()
        mask = updated["id_bahan"].astype(int) == int(id_bahan)
        if not mask.any():
            raise KeyError(f"id_bahan {id_bahan} tidak ditemukan.")

        row = updated.loc[mask].iloc[0]
        added_base = round(float(jumlah_kemasan) * float(row["isi_kemasan_beli"]), 4)
        before = float(row["stok_saat_ini"])
        after = round(before + added_base, 4)
        updated.loc[mask, "stok_saat_ini"] = after
        updated.loc[mask, "is_simulated_stock"] = False

        summary = {
            "id_bahan": int(id_bahan),
            "nama_bahan": str(row["nama_bahan"]),
            "satuan_dasar": str(row["satuan_dasar"]),
            "jumlah_kemasan": float(jumlah_kemasan),
            "added_base_qty": added_base,
            "stok_sebelum": before,
            "stok_sesudah": after,
        }
        return updated, summary

    def apply_stock_opname(
        self, current_stock_df: pd.DataFrame, actual_counts: dict[int, float]
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Sinkronkan stok sistem dengan hasil pengecekan fisik gudang malam hari (*stock opname*),
        dan kembalikan laporan selisih (*variance*).
        """
        updated = current_stock_df.copy()
        records = []
        for iid, actual in actual_counts.items():
            if actual < 0:
                raise ValueError(f"Stok fisik aktual tidak boleh negatif (id_bahan={iid}).")
            mask = updated["id_bahan"].astype(int) == int(iid)
            if not mask.any():
                continue
            row = updated.loc[mask].iloc[0]
            sys_val = float(row["stok_saat_ini"])
            variance = round(float(actual) - sys_val, 4)
            updated.loc[mask, "stok_saat_ini"] = round(float(actual), 4)
            updated.loc[mask, "is_simulated_stock"] = False
            updated.loc[mask, "data_label"] = "ACTUAL_OPNAME"
            records.append(
                {
                    "id_bahan": int(iid),
                    "nama_bahan": str(row["nama_bahan"]),
                    "satuan_dasar": str(row["satuan_dasar"]),
                    "stok_sistem": sys_val,
                    "stok_fisik_aktual": round(float(actual), 4),
                    "selisih_variance": variance,
                }
            )
        return updated, pd.DataFrame(records)
