# 📖 Kamus Data (*Data Dictionary*) & Panduan Dataset — Tim `A26-CS218`
**Penyusun:** Bidang Data Science (Afdha Auliya Atiq & Hauzan Ziyadatul Khoir)  
**Target Pengguna:** Tim Full-stack (`Node.js` + `PostgreSQL` + `React`) & Tim Next-Gen AI Engineer (`Python` / `Scikit-learn` / `FastAPI` / `Gen AI`)  
**Terakhir Diperbarui:** 27 November 2026

---

## 1. Peta Lokasi Dataset Bersih

| Folder | Isi Utama | Ditujukan Untuk |
| :--- | :--- | :--- |
| [minggu-1/output/data_bahan_makanan/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1/output/data_bahan_makanan) | Master bahan baku, kategori menu, menu jual, & resep gramasi (BoM) + `inventory_resto.db` + `schema_and_seed.sql` | Full-stack (`PostgreSQL` seed) & modul konversi stok |
| [minggu-1/output/data_penjualan/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1/output/data_penjualan) | 13 bulan riwayat transaksi NutaCloud bersih, detail item, penyesuaian nota, `map_menu_kasir.csv`, & `ales_place_dwh.db` | Analisis bisnis, dasbor, & audit akurasi transaksi riil |
| [minggu-2/output/data_for_ai/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/output/data_for_ai) | Dataset deret waktu pemakaian bahan harian siap-latih (396 hari x 161 bahan), *feature engineering*, & *time-based split* anti-leakage | Tim **AI Engineer (`AE`: Ayunda & Faris)** untuk training/evaluasi model ML *forecasting* |

---

## 2. Kamus Data: Master Bahan Makanan & Resep (`data_bahan_makanan/`)

### A. `dim_kategori_menu.csv` (8 baris)
| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `id_kategori` | `INTEGER (PK)` | ID unik kategori menu (`1..8`). |
| `nama_kategori` | `VARCHAR(100)` | Nama kategori (`DESSERT`, `DONBURI`, `HOTPLATE`, `MINUMAN`, `NASI GORENG / OMURICE`, `RAMEN`, `SALAD`, `SNACK`). |

### B. `dim_bahan_baku.csv` (178 baris)
| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `id_bahan` | `INTEGER (PK)` | ID unik bahan baku (`1..178`). |
| `nama_bahan` | `VARCHAR(150)` | Nama kanonikal bahan baku (huruf kapital standar, sinonim/typo sudah digabung). |
| `alias_mentah` | `TEXT` | Daftar ejaan asli dari CSV mentah sebelum penyatuan (dipisahkan `\|`). |
| `kategori_vendor` | `VARCHAR(100)` | Kelompok supplier asal di `DATA BASE.csv` (`SAYUR`, `TOKO HAI & FEI`, `OM WEGA`, dll.). |
| `satuan_dasar` | `VARCHAR(20)` | Satuan stok terkecil yang baku: hanya **`gram`**, **`ml`**, atau **`pcs`**. |
| `isi_kemasan_beli` | `DECIMAL(12,4)` | Konversi 1 kemasan beli ke `satuan_dasar` (contoh: 1 sak `BERAS` = `25000.0` gram). |
| `harga_beli_kemasan` | `DECIMAL(14,2)` | Harga beli per 1 kemasan berdasarkan referensi 2018 (Rp). |
| `harga_satuan_dasar` | `DECIMAL(14,4)` | Harga modal per 1 unit `satuan_dasar` (`harga_beli_kemasan / isi_kemasan_beli`). |
| `stok_saat_ini` | `DECIMAL(14,4)` | Saldo stok awal (`0.0` pada master; diisi saat operasional/simulasi). |
| `stok_minimum` | `DECIMAL(14,4)` | Batas stok minimum (*Safety Stock* / *Reorder Point*). |
| `is_packaging` | `INTEGER (0/1)` | `1` jika termasuk kemasan/utilitas non-pangan (`PAPER BOX`, `GAS`, `SEDOTAN`, dll.), `0` jika bahan pangan. |

### C. `dim_menu.csv` (135 baris)
| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `id_menu` | `INTEGER (PK)` | ID unik menu/resep (`1..135`). |
| `id_kategori` | `INTEGER (FK)` | Relasi ke `dim_kategori_menu.id_kategori`. |
| `nama_menu` | `VARCHAR(150)` | Nama menu standar pada resep. |
| `porsi_standar` | `VARCHAR(50)` | Satuan porsi jual resep (contoh: `1 porsi`, `1 cup`, `1 porsi (isi 6)`). |
| `is_sub_recipe` | `INTEGER (0/1)` | `1` jika resep kuah/batch dasar (`Kuah Hotplate`, `Takoyaki` 42 pcs), `0` jika menu jual. |
| `is_sellable` | `INTEGER (0/1)` | `1` untuk **129 menu** yang dijual langsung ke pelanggan. |
| `total_hpp_standar` | `DECIMAL(14,2)` | Total estimasi HPP (Rp) dihitung konsisten dari `fact_resep_bom`. |
| `total_hpp_excel_raw` | `DECIMAL(14,2)` | Angka total bawaan Excel mentah (pembanding audit). |

### D. `fact_resep_bom.csv` (1.579 baris)
| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `id_resep` | `INTEGER (PK)` | ID unik baris komposisi BoM. |
| `id_menu` | `INTEGER (FK)` | Relasi ke `dim_menu.id_menu`. |
| `id_bahan` | `INTEGER (FK)` | Relasi ke `dim_bahan_baku.id_bahan`. *(Pasangan `id_menu, id_bahan` dijamin unik)*. |
| `jumlah_pemakaian` | `DECIMAL(12,4)` | Takaran kebutuhan bahan baku untuk **1 porsi jual** (`porsi_standar`). |
| `satuan_pemakaian` | `VARCHAR(20)` | Selalu sama persis dengan `dim_bahan_baku.satuan_dasar`. |
| `estimasi_biaya_bahan` | `DECIMAL(14,2)` | Estimasi biaya bahan (`jumlah_pemakaian * harga_satuan_dasar`). |

---

## 3. Kamus Data: Penjualan NutaCloud & Mapping (`data_penjualan/`)

### A. `fact_transaksi.csv` (9.295 baris — 1 Oktober 2025 s.d. 31 Oktober 2026)
Kolom utama: `id_transaksi (PK)`, `catatan_nomor`, `waktu_transaksi` (`YYYY-MM-DD HH:MM:SS`), `tanggal` (`YYYY-MM-DD`), `jam` (`0..23`), `pelayan`, `channel_penjualan` (`Dine-In`, `Takeaway`, `GrabFood`, `ShopeeFood`, `GoFood`, `Event`), `brand_store` (`Ale's Place` / `Risoldut`), `metode_pembayaran`, `is_split_payment`, `nama_pelanggan`, `area_lantai`, `nomor_meja`, `pax`, `is_internal_order` (`1` untuk meja `CREW ALES`, `OWNER`, `BUNDA LULU`, `UMI HANA`, `OPERASIONAL`, `MARKETING`, atau diskon Crew/Owner), `subtotal_produk`, `total_penyesuaian_diskon_nota`, `pajak_daerah`, `pembulatan`, `biaya_pengemasan`, `grand_total`, `dibuat_oleh`, `waktu_dibuat`, `diubah_oleh`, `waktu_diubah`, `source_file`.

### B. `fact_penjualan_item.csv` (49.240 baris)
Kolom utama: `id_line (PK)`, `id_transaksi (FK)`, `waktu_transaksi`, `tanggal`, `nama_item_bersih`, `id_menu_resep (FK nullable -> dim_menu)`, `kategori_kasir`, `varian`, `pilihan_ekstra`, `notes`, `qty` (bertanda; `-1` untuk void), `harga_satuan`, `is_diskon_item`, `label_diskon_item`, `nominal_diskon_item`, `subtotal_net`, `is_void_adjustment` (`1` jika `qty <= 0`).

### C. `fact_penyesuaian_transaksi.csv` (17.920 baris)
Menyimpan baris non-menu (`PAJAK_DAERAH`, `PEMBULATAN`, `DISKON_NOTA`, `VOUCHER_NOTA`, `BIAYA_PENGEMASAN`, `ALAT_MAKAN_TKW`) agar rekonsiliasi keuangan tetap 100% akurat.

### D. `map_menu_kasir.csv` (381 item unik)
Jembatan antara `nama_item_kasir` (NutaCloud) dan `dim_menu.id_menu`:
- `MAPPED_EXACT` (30 item) & `MAPPED_ALIAS` (73 item) = **34.289 porsi (59,0% volume)** siap dikonversi ke bahan baku.
- `UNMAPPED_FNB` (240 item / 36,8%), `AMBIGUOUS_VARIANT` (9 item / 3,8%), `UNMAPPED_NON_FNB_MERCH` (29 item / 0,4%).

---

## 4. Kamus Data: Dataset Siap-AI untuk Tim AE (`data_for_ai/`)

File yang tersedia:
- `METADATA_DATASET_AI.md` (penjelasan variabel lengkap dalam format Markdown langsung di folder dataset AI)
- `daily_usage_full_features.csv` (**63.756** baris = `396` hari kalender $\times$ `161` bahan aktif di BoM)
- `train_daily_usage.csv` (**58.765** baris: `2025-10-01` s.d. `2026-09-30`)
- `test_daily_usage.csv` (**4.991** baris: `2026-10-01` s.d. `2026-10-31`)
- `ingredient_burn_rate_summary.csv` (**161** baris ringkasan *daily burn rate* per bahan pada 395 hari operasional aktif)

| Kolom di `train_daily_usage.csv` / `test_daily_usage.csv` | Tipe | Penjelasan & Catatan Anti-Leakage |
| :--- | :--- | :--- |
| `tanggal` | `DATE` | Tanggal kalender lengkap `2025-10-01` s.d. `2026-10-31`. |
| `id_bahan`, `nama_bahan`, `kategori_vendor`, `satuan_dasar`, `is_packaging` | `INT / STR` | Identitas & satuan dasar bahan (`gram` / `ml` / `pcs`). |
| `isi_kemasan_beli`, `harga_beli_kemasan`, `harga_satuan_dasar` | `FLOAT` | Informasi konversi kemasan beli & HPP 2018. |
| `total_pemakaian` / `target_pemakaian` | `FLOAT` | **Target prediksi (`y`):** Total pemakaian harian bahan baku (sudah termasuk `is_internal_order`, dan `0.0` jika hari itu tidak terpakai). |
| `estimasi_hpp` | `FLOAT` | Estimasi nilai biaya pemakaian hari tersebut (Rp). |
| `is_store_closed` | `INT (0/1)` | `1` pada `2026-03-21` (toko tutup Idul Fitri); `0` pada 395 hari aktif. |
| `day_of_week`, `is_weekend`, `day_of_month`, `month`, `week_of_year` | `INT` | Fitur kalender (*weekend* didefinisikan sebagai Jumat–Minggu `[4,5,6]` sesuai pola lonjakan resto). |
| `is_payday_window` | `INT (0/1)` | `1` jika tanggal `25` s.d. tanggal `5` (periode gajian). |
| `is_ramadan_period` | `INT (0/1)` | `1` pada periode Ramadhan `2026-02-18` s.d. `2026-03-20`. |
| `lag_1`, `lag_7`, `lag_14` | `FLOAT` | Pemakaian 1 hari, 7 hari, dan 14 hari sebelumnya (`shift(1/7/14)` — dijamin **zero data leakage**). |
| `rolling_mean_7`, `rolling_std_7`, `rolling_mean_28` | `FLOAT` | Rata-rata & simpangan baku historis **hanya dari masa lalu** (`shift(1).rolling(...)` — aman dipakai untuk *inference*). |
| `data_source_label` | `STR` | Label transparan: `PRIMARY_NUTACLOUD_X_BOM2018_PARTIAL_59PCT`. |

> [!WARNING]
> **Keterbatasan Dataset yang Wajib Diperhatikan Tim AE & Full-stack:**
> 1. Nilai `total_pemakaian` saat ini berasal dari **59,0% porsi penjualan** yang sudah memiliki resep di data 2018. Setelah Owner membalas [LAPORAN_KONFIRMASI_DATA_OWNER.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1/docs/LAPORAN_KONFIRMASI_DATA_OWNER.md), angka `total_pemakaian` untuk bahan menu baru (misal Salmon, Udon, Kopi) akan diperbarui.
> 2. Sebanyak **38 dari 161** bahan di BoM memiliki `total_pemakaian = 0` sepanjang 2025–2026 karena menu resep 2018-nya (seperti *Miruku Bath*, *Cau Katsu Bubble Gum*, *Burger*) tidak/belum tercatat terjual pada periode 2025–2026 atau tercatat dengan nama ambigu (`Cau Katsu`).
> 3. Untuk saldo stok awal gudang pada simulasi dasbor DS, data menggunakan **simulasi 7 hari pemakaian historis** yang diberi label eksplisit `SIMULASI_7_HARI_HISTORIS` hingga saldo fisik gudang dari UMKM tersedia.
