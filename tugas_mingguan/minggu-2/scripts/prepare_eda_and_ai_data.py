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
  - METADATA_DATASET_AI.md
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
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

    # Susun metadata variabel dalam format Markdown (METADATA_DATASET_AI.md)
    zero_usage_cnt = int((burn["total_pemakaian_395d"] == 0).sum())
    generated_at = datetime.now().isoformat(timespec="seconds")
    data_source_label = "PRIMARY_NUTACLOUD_X_BOM2018_PARTIAL_59PCT"

    md_lines = f"""# 📋 Metadata Dataset Siap-AI (`data_for_ai/`)

**Tim Capstone:** `A26-CS218` — *Stok Makanan Sudah Habis* (Asah 2026)  
**Penyusun:** Data Science (`Afdha Auliya Atiq & Hauzan Ziyadatul Khoir`)  
**Ditujukan Untuk:** Next-Gen AI Engineer (`Ayunda & Faris`) & AI Full-Stack (`Aleandre & Alfarisi`)  
**Dibuat / Diperbarui:** `{generated_at}`  
**Label Sumber Data:** `{data_source_label}`

---

## 1. Daftar File di Folder Ini

| Nama File | Jumlah Baris | Rentang Waktu | Fungsi Utama |
| :--- | :---: | :---: | :--- |
| `train_daily_usage.csv` | **{len(train_df):,}** | `2025-10-01` s.d. `2026-09-30` | **Data Training ML** (365 hari $\\times$ {len(df_ing)} bahan aktif BoM). |
| `test_daily_usage.csv` | **{len(test_df):,}** | `2026-10-01` s.d. `2026-10-31` | **Data Hold-Out Testing ML** (31 hari $\\times$ {len(df_ing)} bahan) bebas *data leakage*. |
| `daily_usage_full_features.csv` | **{len(df_full):,}** | `2025-10-01` s.d. `2026-10-31` | **Dataset Gabungan Penuh** ({len(date_strs)} hari kalender $\\times$ {len(df_ing)} bahan) untuk *rolling CV*. |
| `ingredient_burn_rate_summary.csv` | **{len(burn):,}** | 395 hari operasional aktif | **Ringkasan Burn Rate per Bahan** (tidak termasuk hari libur tutup `2026-03-21`). |
| `METADATA_DATASET_AI.md` | — | — | Dokumen metadata penjelasan seluruh variabel pada ke-4 file CSV di atas. |

---

## 2. Penjelasan Lengkap Variabel: `train_daily_usage.csv`, `test_daily_usage.csv`, & `daily_usage_full_features.csv` (`27` Kolom)

### A. Identitas Waktu & Bahan Baku (`11` Variabel)
| Nama Variabel | Tipe | Peran ML | Satuan / Contoh | Penjelasan |
| :--- | :---: | :---: | :--- | :--- |
| `tanggal` | `DATE (YYYY-MM-DD)` | Index Waktu | `2025-10-01` | Tanggal kalender lengkap (`396` hari berturut-turut tanpa bolong). |
| `id_bahan` | `INT` | Key Entitas | `1` s.d. `178` | Foreign key ke `dim_bahan_baku.id_bahan` (terdapat `{len(df_ing)}` bahan yang terdaftar di resep BoM). |
| `nama_bahan` | `STRING` | Identitas | `DAGING SAPI`, `MIE` | Nama standar bahan baku hasil normalisasi huruf kapital. |
| `kategori_vendor` | `STRING` | Fitur Kategorik | `SAYUR`, `MITRA DAGING` | Kelompok supplier asal di `DATA BASE.csv` (mencerminkan sifat barang segar vs kemasan). |
| `satuan_dasar` | `STRING` | Satuan / Filter | `gram`, `ml`, `pcs` | Satuan baku pemakaian & prediksi (**wajib dikelompokkan/diperhatikan** per bahan). |
| `isi_kemasan_beli` | `FLOAT` | Fitur Numerik | `25000.0` (1 sak beras) | Jumlah unit `satuan_dasar` per 1 kemasan belanja di supplier. |
| `harga_beli_kemasan` | `FLOAT` | Fitur Numerik | `325000.0` (Rp) | Harga beli per 1 kemasan berdasarkan referensi database 2018. |
| `harga_satuan_dasar` | `FLOAT` | Fitur Numerik | `13.0` (Rp/gram) | Modal per 1 unit `satuan_dasar` (`harga_beli_kemasan / isi_kemasan_beli`). |
| `is_packaging` | `INT (0/1)` | Fitur Biner | `0` = bahan pangan, `1` = kemasan | Penanda barang non-pangan (`PAPER BOX`, `GAS`, `SEDOTAN`, dll.). |
| `estimasi_hpp` | `FLOAT` | **Jangan jadi fitur X!** | `756.82` (Rp) | Nilai HPP pemakaian aktual hari $t$ (`total_pemakaian * harga_satuan_dasar`) — *hanya tersedia setelah hari $t$ selesai*. |
| `data_source_label` | `STRING` | Audit Label | `PRIMARY_NUTACLOUD_X_BOM2018_PARTIAL_59PCT` | Penanda asal data primer NutaCloud + keterbatasan cakupan resep 2018. |

### B. Target Prediksi (`2` Variabel)
| Nama Variabel | Tipe | Peran ML | Catatan Penting | Penjelasan |
| :--- | :---: | :---: | :--- | :--- |
| `total_pemakaian` | `FLOAT` | Nilai Mentah Target | **Jangan dimasukkan sebagai fitur X!** | Total konsumsi bahan pada `tanggal` tersebut dalam `satuan_dasar` (termasuk order internal Crew/Owner; `0.0` jika tidak ada penjualan menu terkait). |
| `target_pemakaian` | `FLOAT` | **Target (`y`)** | Alias resmi untuk `y` | Identik dengan `total_pemakaian`; gunakan kolom ini sebagai variabel target model *forecasting* / regresi. |

### C. Fitur Kalender & Konteks Bisnis (`8` Variabel — Diketahui Sebelum Hari $H$)
| Nama Variabel | Tipe | Nilai / Rentang | Penjelasan |
| :--- | :---: | :---: | :--- |
| `is_store_closed` | `INT (0/1)` | `1` pada `2026-03-21` | Penanda hari toko tutup operasional (Idul Fitri 2026 — seluruh pemakaian `0.0`). |
| `day_of_week` | `INT` | `0` (Senin) s.d. `6` (Minggu) | Indeks hari dalam sepekan. |
| `is_weekend` | `INT (0/1)` | `1` untuk Jumat, Sabtu, Minggu (`4,5,6`) | Didefinisikan mulai **Jumat** sesuai pola lonjakan trafik resto (`+67,8%` transaksi). |
| `day_of_month` | `INT` | `1` s.d. `31` | Tanggal dalam bulan. |
| `month` | `INT` | `1` s.d. `12` | Bulan kalender untuk menangkap efek musiman. |
| `week_of_year` | `INT` | `1` s.d. `53` | Minggu ISO dalam tahun berjalan. |
| `is_payday_window` | `INT (0/1)` | `1` jika tanggal $\\ge 25$ atau $\\le 5$ | Penanda periode gajian awal/akhir bulan. |
| `is_ramadan_period` | `INT (0/1)` | `1` pada `2026-02-18` s.d. `2026-03-20` | Penanda periode Ramadhan 1447H (lonjakan `Paket Iftar` Maret 2026). |

### D. Fitur Lag & Rolling Historis Kausal (`6` Variabel — *Zero Data Leakage*)
> Seluruh fitur di bawah dihitung per `id_bahan` memakai `.shift(1)` sehingga **nilai hari $t$ tidak pernah bocor ke fitur hari $t$**.

| Nama Variabel | Tipe | Nullable? | Rumus & Penjelasan |
| :--- | :---: | :---: | :--- |
| `lag_1` | `FLOAT` | Ya (hari ke-1) | `total_pemakaian` **1 hari sebelumnya** ($t - 1$). |
| `lag_7` | `FLOAT` | Ya (hari ke-1..7) | `total_pemakaian` **7 hari sebelumnya** ($t - 7$, hari yang sama pekan lalu). |
| `lag_14` | `FLOAT` | Ya (hari ke-1..14) | `total_pemakaian` **14 hari sebelumnya** ($t - 14$). |
| `rolling_mean_7` | `FLOAT` | Ya (hari ke-1) | Rata-rata bergerak 7 hari terakhir hingga $t - 1$ (`shift(1).rolling(7, min_periods=1).mean()`). |
| `rolling_std_7` | `FLOAT` | Tidak (`0.0` di awal) | Simpangan baku 7 hari terakhir hingga $t - 1$ (mengukur volatilitas pemakaian mingguan). |
| `rolling_mean_28` | `FLOAT` | Ya (hari ke-1) | Rata-rata bergerak 28 hari terakhir hingga $t - 1$ (tren jangka menengah bulanan). |

---

## 3. Penjelasan Lengkap Variabel: `ingredient_burn_rate_summary.csv` (`15` Kolom)

Ringkasan profil konsumsi tiap bahan baku (hanya dihitung pada **395 hari operasional aktif**, mengecualikan `2026-03-21`):

| Nama Variabel | Tipe | Penjelasan |
| :--- | :---: | :--- |
| `id_bahan`, `nama_bahan`, `kategori_vendor`, `satuan_dasar`, `isi_kemasan_beli`, `harga_beli_kemasan`, `harga_satuan_dasar`, `is_packaging` | `INT / STR / FLOAT` | Identitas master bahan baku (sama dengan bagian 2A). |
| `total_pemakaian_395d` | `FLOAT` | Akumulasi pemakaian sepanjang 395 hari aktif (dalam `satuan_dasar`). |
| `burn_rate_mean` | `FLOAT` | Rata-rata pemakaian harian keseluruhan (*Daily Burn Rate* selama 395 hari aktif). |
| `burn_rate_std` | `FLOAT` | Simpangan baku pemakaian harian selama 395 hari aktif (dipakai untuk rumus *Safety Stock*). |
| `burn_rate_max` | `FLOAT` | Pemakaian harian tertinggi yang pernah tercatat dalam periode 13 bulan. |
| `burn_rate_30d` | `FLOAT` | Rata-rata pemakaian harian pada **30 hari aktif terakhir** (periode Okt 2026). |
| `burn_rate_weekday` | `FLOAT` | Rata-rata pemakaian harian khusus hari **Senin – Kamis**. |
| `burn_rate_weekend` | `FLOAT` | Rata-rata pemakaian harian khusus hari **Jumat – Minggu**. |

---

## 4. Catatan Penting Penggunaan untuk Tim AE

1. **Kolom yang WAJIB di-drop saat menyusun `X_train` / `X_test`:**  
   Jangan masukkan `total_pemakaian`, `target_pemakaian`, `estimasi_hpp`, dan kolom teks ID mentah (`tanggal`, `nama_bahan`, `data_source_label`) langsung tanpa encoding sebagai fitur input `X`, karena `total_pemakaian` & `estimasi_hpp` adalah nilai aktual hari target $t$.
2. **Penanganan `NaN` Awal:**  
   Baris 1–14 pada awal riwayat Oktober 2025 memiliki `NaN` pada `lag_1` / `lag_7` / `lag_14` sebagai konsekuensi wajar lag kausal. Untuk model berbasis pohon (`LightGBM`/`XGBoost`) boleh dibiarkan `NaN`, atau diisi/dibuang (`dropna`) untuk model linear/`RandomForest`/`ARIMA` tanpa memengaruhi data `test_daily_usage.csv` (yang 100% terisi penuh karena berlanjut dari Okt 2025–Sep 2026).
3. **Keterbatasan Cakupan Data:**  
   - Cakupan BoM 2018 mencakup **59,0%** volume porsi NutaCloud 2025–2026; sebanyak **{zero_usage_cnt} dari {len(df_ing)}** bahan BoM bernilai `0` karena menu resep 2018-nya tidak muncul di transaksi 2025–2026.
   - Tidak ada data stok simulasi fiktif di dalam 4 file CSV AI ini (stok simulasi hanya dipakai di prototipe dasbor DS untuk saldo awal gudang yang belum tersedia dari UMKM).
"""
    (AI_OUT_DIR / "METADATA_DATASET_AI.md").write_text(md_lines, encoding="utf-8")

    print("\n=== PAKET DATA SIAP-AI (TIM AE) SELESAI ===")
    print(f"Active BOM ingredients : {len(df_ing)}")
    print(f"Full dataset rows      : {len(df_full):,} ({len(date_strs)} hari x {len(df_ing)} bahan)")
    print(f"Train split (Okt25-Sep26): {len(train_df):,} baris")
    print(f"Test split  (Okt 2026)   : {len(test_df):,} baris")
    print(f"Metadata MD            : {AI_OUT_DIR / 'METADATA_DATASET_AI.md'}")
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
