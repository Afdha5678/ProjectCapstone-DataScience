"""Script validasi & audit hasil normalisasi Data Penjualan dan DWH terpadu."""

import sqlite3
from pathlib import Path

import pandas as pd

MINGGU_1_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = MINGGU_1_DIR / "output" / "data_penjualan"


def main() -> None:
    df_tx = pd.read_csv(OUT_DIR / "fact_transaksi.csv")
    df_items = pd.read_csv(OUT_DIR / "fact_penjualan_item.csv")
    df_adj = pd.read_csv(OUT_DIR / "fact_penyesuaian_transaksi.csv")
    df_map = pd.read_csv(OUT_DIR / "map_menu_kasir.csv")

    print("=== 1. ROW CONSERVATION & DATE INTEGRITY ===")
    print(f"fact_transaksi             : {len(df_tx):,}")
    print(f"fact_penjualan_item        : {len(df_items):,}")
    print(f"fact_penyesuaian_transaksi : {len(df_adj):,}")
    print(f"Total line rows (item+adj) : {len(df_items) + len(df_adj):,} (expected raw: 67,160)")
    assert len(df_items) + len(df_adj) == 67160

    null_dt_tx = df_tx["waktu_transaksi"].isna().sum()
    null_dt_it = df_items["waktu_transaksi"].isna().sum()
    print(f"Null waktu_transaksi (tx / item): {null_dt_tx} / {null_dt_it}")
    assert null_dt_tx == 0 and null_dt_it == 0

    print("\n=== 2. FINANCIAL RECONCILIATION (100% RECEIPTS) ===")
    calc_grand = (
        df_tx["subtotal_produk"]
        + df_tx["total_penyesuaian_diskon_nota"]
        + df_tx["pajak_daerah"]
        + df_tx["pembulatan"]
        + df_tx["biaya_pengemasan"]
    )
    diff = (calc_grand - df_tx["grand_total"]).abs()
    mismatches = (diff > 1.0).sum()
    print(f"Receipts with reconciliation diff > Rp 1: {mismatches} / {len(df_tx):,}")
    assert mismatches == 0

    print("\n=== 3. CATEGORICAL & PARSING CHECK ===")
    print("Channel distribution:")
    print(df_tx["channel_penjualan"].value_counts().to_string())
    print("\nInternal orders (is_internal_order=1):", int(df_tx["is_internal_order"].sum()))
    print("Split payments (is_split_payment=1) :", int(df_tx["is_split_payment"].sum()))
    print("Items with diskon (is_diskon_item=1):", int(df_items["is_diskon_item"].sum()))
    print("Void/return lines (qty <= 0)        :", int(df_items["is_void_adjustment"].sum()))
    print("Null kategori_kasir in items        :", int(df_items["kategori_kasir"].isna().sum()))

    print("\n=== 4. RECIPE MAPPING BREAKDOWN ===")
    summary_map = df_map.groupby("match_status").agg(
        unique_items=("nama_item_kasir", "count"),
        total_qty=("total_qty_terjual", "sum"),
        total_omzet=("total_omzet_net", "sum"),
    )
    print(summary_map.to_string())

    print("\n=== 5. SQLITE DWH INTEGRITY CHECK ===")
    conn = sqlite3.connect(OUT_DIR / "ales_place_dwh.db")
    fk_err = conn.execute("PRAGMA foreign_key_check;").fetchall()
    print(f"FK check errors: {len(fk_err)}")
    assert len(fk_err) == 0

    sample_ing = pd.read_sql(
        "SELECT tanggal, nama_bahan, total_pemakaian, satuan_dasar FROM v_pemakaian_bahan_harian LIMIT 10",
        conn,
    )
    print("\nSample v_pemakaian_bahan_harian:")
    print(sample_ing.to_string(index=False))
    conn.close()


if __name__ == "__main__":
    main()
