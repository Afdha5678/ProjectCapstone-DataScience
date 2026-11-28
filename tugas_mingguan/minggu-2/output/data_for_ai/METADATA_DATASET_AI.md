# 📋 Metadata Dataset Siap-AI (`data_for_ai/`)

**Tim Capstone:** `A26-CS218` — *Stok Makanan Sudah Habis* (Asah 2026)  
**Penyusun:** Data Science (`Afdha Auliya Atiq & Hauzan Ziyadatul Khoir`)  
**Ditujukan Untuk:** Next-Gen AI Engineer (`Ayunda & Faris`) & AI Full-Stack (`Aleandre & Alfarisi`)  
**Dibuat / Diperbarui:** `2026-11-28T13:50:03`  
**Label Sumber Data:** `PRIMARY_NUTACLOUD_X_BOM2018_PARTIAL_59PCT`

---

## 1. Daftar File di Folder Ini

| Nama File | Jumlah Baris | Rentang Waktu | Fungsi Utama |
| :--- | :---: | :---: | :--- |
| `train_daily_usage.csv` | **58,765** | `2025-10-01` s.d. `2026-09-30` | **Data Training ML** (365 hari $\times$ 161 bahan aktif BoM). |
| `test_daily_usage.csv` | **4,991** | `2026-10-01` s.d. `2026-10-31` | **Data Hold-Out Testing ML** (31 hari $\times$ 161 bahan) bebas *data leakage*. |
| `daily_usage_full_features.csv` | **63,756** | `2025-10-01` s.d. `2026-10-31` | **Dataset Gabungan Penuh** (396 hari kalender $\times$ 161 bahan) untuk *rolling CV*. |
| `ingredient_burn_rate_summary.csv` | **161** | 395 hari operasional aktif | **Ringkasan Burn Rate per Bahan** (tidak termasuk hari libur tutup `2026-03-21`). |
| `METADATA_DATASET_AI.md` | — | — | Dokumen metadata penjelasan seluruh variabel pada ke-4 file CSV di atas. |

---

## 2. Penjelasan Lengkap Variabel: `train_daily_usage.csv`, `test_daily_usage.csv`, & `daily_usage_full_features.csv` (`27` Kolom)

### A. Identitas Waktu & Bahan Baku (`11` Variabel)
| Nama Variabel | Tipe | Peran ML | Satuan / Contoh | Penjelasan |
| :--- | :---: | :---: | :--- | :--- |
| `tanggal` | `DATE (YYYY-MM-DD)` | Index Waktu | `2025-10-01` | Tanggal kalender lengkap (`396` hari berturut-turut tanpa bolong). |
| `id_bahan` | `INT` | Key Entitas | `1` s.d. `178` | Foreign key ke `dim_bahan_baku.id_bahan` (terdapat `161` bahan yang terdaftar di resep BoM). |
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
| `is_payday_window` | `INT (0/1)` | `1` jika tanggal $\ge 25$ atau $\le 5$ | Penanda periode gajian awal/akhir bulan. |
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
   - Cakupan BoM 2018 mencakup **59,0%** volume porsi NutaCloud 2025–2026; sebanyak **38 dari 161** bahan BoM bernilai `0` karena menu resep 2018-nya tidak muncul di transaksi 2025–2026.
   - Tidak ada data stok simulasi fiktif di dalam 4 file CSV AI ini (stok simulasi hanya dipakai di prototipe dasbor DS untuk saldo awal gudang yang belum tersedia dari UMKM).
