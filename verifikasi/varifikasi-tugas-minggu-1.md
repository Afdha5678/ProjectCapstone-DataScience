# 📋 Laporan Audit & Verifikasi Tugas Minggu 1 (Data Science)

**Program:** Asah 2026 (Dicoding & GoTo)  
**Tim Capstone:** `A26-CS218` — *Stok Makanan Sudah Habis*  
**UMKM Mitra:** Ale’s Place Cipoho (PIC: Mochamad Ares Fadella)  
**Penanggung Jawab Data Science:**  
- `DS001B6Y0696` — Afdha Auliya Atiq  
- `DS001B6Y0726` — Hauzan Ziyadatul Khoir  

**Periode Target Minggu 1:** 20 – 26 November 2026  
**Tanggal Verifikasi:** 27 November 2026  
**Status Akhir:** ✅ **LULUS VERIFIKASI — AMAN & SIAP LANJUT KE MINGGU 2**

---

## 1. Evaluasi Kesesuaian Terhadap Target Minggu 1 (*Plan vs Actual*)

Berdasarkan dokumen **Jadwal Rencana Kerja (Poin #2)** dan **Tabel Fitur Kerja Data Science (Baris #1 — Wajib)**, berikut hasil verifikasi kesesuaian target Minggu 1:

| Kriteria Target Minggu 1 | Status | Realisasi & Bukti Verifikasi |
| :--- | :---: | :--- |
| **1. *Data wrangling* laporan NutaCloud sehingga bersih dari baris non-menu/error** | ✅ **TERPENUHI** | Seluruh **13 file CSV** (Okt 2025 – Okt 2026, total **67.160** baris mentah di luar `Grand Total`) telah dibersihkan dan dinormalisasi menjadi `fact_transaksi.csv` (**9.295** transaksi), `fact_penjualan_item.csv` (**49.240** baris produk), dan `fact_penyesuaian_transaksi.csv` (**17.920** baris pajak, pembulatan, diskon nota, biaya pengemasan, & alat makan TKW). |
| **2. Penyusunan skema pemetaan resep (*Bill of Materials*) ke master data bahan baku** | ✅ **TERPENUHI** | Seluruh **9 file CSV** resep & bahan baku tahun 2018 telah dinormalisasi menjadi skema relasional 3NF (`dim_kategori_menu`, `dim_bahan_baku`, `dim_menu`, `fact_resep_bom`) dalam format CSV, SQLite (`inventory_resto.db`), dan SQL (`schema_and_seed.sql`) dengan **0 error Foreign Key**. |
| **3. Tabel *mapping* gramasi resep untuk setiap menu dan varian** | ⚠️ **TERPENUHI (DENGAN CATATAN EKSTERNAL)** | Skema jembatan `map_menu_kasir.csv` (**381** item kasir unik) sudah tersedia dan valid. Sebanyak **103 menu** (**34.289 porsi / 59,0% volume penjualan**) sudah terhubung ke resep gramasi. Sisanya (**240 item F&B baru 2025–2026** + **9 varian ambigu**) belum tersedia di file resep 2018 sehingga telah dibuatkan dokumen permohonan konfirmasi ke Owner. |
| **4. Pemisahan struktur folder data bersih untuk kolaborasi tim** | ✅ **TERPENUHI** | Seluruh output bersih dipisahkan rapi ke [processed_data/data_bahan_makanan/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_bahan_makanan) (kebutuhan Web/Stok) dan [processed_data/data_penjualan/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_penjualan) (kebutuhan DWH/Analisis/Forecasting). |

---

## 2. Inventaris Lengkap File & Script Hasil Minggu 1

### A. Script ETL & Validasi Otomatis (`scripts/`)
| File Script | Fungsi Utama |
| :--- | :--- |
| [normalize_bahan_makanan.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/scripts/normalize_bahan_makanan.py) | Parser & normalizer 9 file resep/bahan mentah ke skema relasional 3NF (CSV, SQLite, SQL). |
| [validate_data.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/scripts/validate_data.py) | Script audit integritas relasional, satuan dasar, harga nol, dan rekonsiliasi HPP bahan baku. |
| [clean_penjualan.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/scripts/clean_penjualan.py) | ETL normalisasi 13 file laporan NutaCloud, ekstraksi field majemuk/diskon, pemetaan menu kasir $\leftrightarrow$ BoM, dan pembangun DWH terpadu. |
| [validate_penjualan.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/scripts/validate_penjualan.py) | Script audit konservasi baris, integritas tanggal, rekonsiliasi 100% struk, dan verifikasi `ales_place_dwh.db`. |

### B. Output Bersih Data Bahan Makanan (`processed_data/data_bahan_makanan/`)
| File Output | Ukuran | Jumlah Baris / Entitas | Keterangan |
| :--- | :---: | :---: | :--- |
| [dim_kategori_menu.csv](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_bahan_makanan/dim_kategori_menu.csv) | 124 B | **8** kategori | DESSERT, DONBURI, HOTPLATE, MINUMAN, NASI GORENG / OMURICE, RAMEN, SALAD, SNACK. |
| [dim_bahan_baku.csv](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_bahan_makanan/dim_bahan_baku.csv) | 13,9 KB | **178** bahan baku | Master bahan baku terstandarisasi (`gram`, `ml`, `pcs`), dilengkapi `isi_kemasan_beli`, `harga_beli_kemasan`, `harga_satuan_dasar`, dan `is_packaging`. |
| [dim_menu.csv](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_bahan_makanan/dim_menu.csv) | 7,0 KB | **135** menu | **129** menu jual (`is_sellable=1`) dan **6** kuah/batch dasar (`is_sub_recipe=1`), beserta `total_hpp_standar` dan `total_hpp_excel_raw`. |
| [fact_resep_bom.csv](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_bahan_makanan/fact_resep_bom.csv) | 43,2 KB | **1.579** baris BOM | Komposisi takaran per **1 porsi jual** (unique pair `id_menu` + `id_bahan`). |
| [inventory_resto.db](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_bahan_makanan/inventory_resto.db) | 114,7 KB | 4 tabel + 1 view | Database SQLite dengan `FOREIGN KEY` aktif dan view `v_resep_lengkap`. |
| [schema_and_seed.sql](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_bahan_makanan/schema_and_seed.sql) | 335,6 KB | DDL + DML | Script SQL `CREATE TABLE`, `CREATE VIEW`, dan `INSERT` siap migrasi ke MySQL/PostgreSQL/SQLite. |
| [AUDIT_TINJAUAN_BAHAN_MAKANAN.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_bahan_makanan/AUDIT_TINJAUAN_BAHAN_MAKANAN.md) | 9,0 KB | Dokumen Audit | Catatan rincian selisih HPP dan kejanggalan resep 2018. |

### C. Output Bersih Data Penjualan (`processed_data/data_penjualan/`)
| File Output | Ukuran | Jumlah Baris / Entitas | Keterangan |
| :--- | :---: | :---: | :--- |
| [fact_transaksi.csv](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_penjualan/fact_transaksi.csv) | 3,21 MB | **9.295** transaksi | Header transaksi unik di level struk (`waktu_transaksi`, `channel_penjualan`, `brand_store`, `pelayan`, `area_lantai`, `nomor_meja`, `pax`, `is_internal_order`, dan rincian finansial). |
| [fact_penjualan_item.csv](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_penjualan/fact_penjualan_item.csv) | 5,98 MB | **49.240** baris item | Baris produk terjual bersih + ekstraksi diskon item + link `id_menu_resep`. |
| [fact_penyesuaian_transaksi.csv](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_penjualan/fact_penyesuaian_transaksi.csv) | 1,14 MB | **17.920** baris | Baris non-menu: `PAJAK_DAERAH`, `PEMBULATAN`, `DISKON_NOTA`, `VOUCHER_NOTA`, `BIAYA_PENGEMASAN`, dan `ALAT_MAKAN_TKW`. |
| [map_menu_kasir.csv](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_penjualan/map_menu_kasir.csv) | 26,1 KB | **381** item unik | Kamus pemetaan item NutaCloud $\leftrightarrow$ `dim_menu` beserta `match_status`, total qty, dan omzet net. |
| [ales_place_dwh.db](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/processed_data/data_penjualan/ales_place_dwh.db) | 11,29 MB | 8 tabel + 2 view | SQLite Data Warehouse terpadu (4 tabel BoM + 4 tabel Penjualan/Mapping + view `v_resep_lengkap` & `v_pemakaian_bahan_harian`). |

### D. Dokumen Tindak Lanjut ke Owner (Root Workspace)
- [LAPORAN_KONFIRMASI_DATA_OWNER.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/LAPORAN_KONFIRMASI_DATA_OWNER.md) — Laporan berbahasa bisnis untuk Pak Ares berisi daftar Top 30 menu terlaris yang belum ada resepnya, klarifikasi takaran 2018, pertanyaan operasional *safety stock*, serta draft pesan WhatsApp.

---

## 3. Audit Detail Tahap A: Normalisasi Data Bahan Makanan & Resep (BoM)

### A. Transformasi & Penanganan Anomali Data Mentah
1. **Ekstraksi Blok Vertikal & Multi-Tabel Vendor:**
   - Mengurai struktur cetak Excel yang menumpuk banyak resep dalam satu lembar (`DESSERT`, `DONBURI`, `HOTPLATE`, `MINUMAN`, `NASI GORENG`, `RAMEN`, `SNACK`, `Salad`) serta multi-header supplier pada `DATA BASE.csv`.
   - Menangani baris tanpa nomor urut (contoh: `LEMON BUAH` pada menu `Leci Mint tea` di `MINUMAN.csv` baris 134) agar tidak terlewat saat parsing.
2. **Standarisasi Satuan Dasar (*Base Unit of Measure*):**
   - Seluruh **178 bahan baku** diseragamkan menjadi hanya **3 satuan baku**: `gram` (**117** bahan), `ml` (**27** bahan), dan `pcs` (**34** bahan).
   - Mengoreksi satuan kemasan yang tertukar di Excel mentah, antara lain: `ES BATU` (`19,000` tertulis `liter` $\rightarrow$ `gram`), `GALON` (`19,000` tertulis `liter` $\rightarrow$ `ml`), `MINYAK GORENG` (`2,000` tertulis `liter` $\rightarrow$ `ml`), `SPRITE` (`1,500` tertulis `liter` $\rightarrow$ `ml`), `STRAWBERRY BUAH` (`12` tertulis `gram` $\rightarrow$ `pcs`), dan `YAKULT` (`5` tertulis `ml` $\rightarrow$ `pcs`).
3. **Penyatuan Sinonim, Typo & Duplikat:**
   - Menyatukan **33 nama bahan** yang tidak sinkron antara resep dan `DATA BASE.csv` (misal: `AIR` / `AIR PANAS/ES` / `GALON` $\rightarrow$ `AIR GALON`, `TIMUN` $\rightarrow$ `MENTIMUN`, `STICER ALES` $\rightarrow$ `STIKER ALES`, `SUSU KENTAL DAIRY CHAM` $\rightarrow$ `DAIRY CHARM`, `BOMBAY` $\rightarrow$ `BAWANG BOMBAY`, `ES` $\rightarrow$ `ES BATU`).
   - Menyelesaikan duplikasi `MISO` di `DATA BASE.csv` (menggunakan harga aktif Rp60/gram yang dipakai di `RAMEN.csv`) serta melengkapi harga `PAPER BOX` (Rp1.500/pcs dari lembar `DESSERT.csv`).
   - Menjumlahkan bahan yang muncul dua kali dalam satu resep (misal bawang untuk tumis + kaldu di `HOTPLATE.csv`, atau telur dadar + adonan di `Omurice`) agar pasangan `(id_menu, id_bahan)` bersifat unik.
4. **Konversi Resep Batch & *Flattening* Sub-Resep ke 1 Porsi Jual:**
   - **Resep Batch:** `Sweet Takoyaki` (dikonversi ke 1 porsi isi 6 dari batch 12), `Silky Pudding` (/12 cup), `Cau Katsu` (/15 porsi + packaging `Paper Box` & `Garpu Plastik` per porsi), dan `Miruku Bath` (/16 porsi + packaging `Wadah Miruku`, `Sendok Miruku`, `Cocoa Powder`, & `Stiker Ales` per porsi).
   - **Sub-Resep (*Flattened*):** `Cah Jamur` mengurai langsung bahan penyusun `Kuah Hotplate`, sedangkan `Takoyaki Isi 6`, `Isi 9`, dan `Isi 12` mengurai langsung bahan adonan `Takoyaki` (batch 42 pcs) sehingga pemotongan stok langsung memotong bahan mentah gudang.
   - **Stub Excluded:** `Miruku 1` dikeluarkan dari `dim_menu` karena merupakan baris duplikat *self-referencing* dari `Miruku Bath`.

### B. Hasil Pengujian Script `validate_data.py`
- `PRAGMA foreign_key_check` = **0 error**.
- Bahan baku dengan `harga_satuan_dasar <= 0` = **0**.
- Menu tanpa baris BoM = **0** (dari **135** menu).
- Menu tanpa pembanding `total_hpp_excel_raw` = **0**.
- **Rekonsiliasi HPP Standar vs Excel Mentah:** Seluruh selisih > Rp 500 hanya terjadi pada **4 menu**, dan keempatnya merupakan perbaikan bug ketik bawaan Excel:
  1. `Cau Katsu Bubble Gum` (`Std: 12.303,68` vs `Raw: 11.056,00` | `+1.247,68`): Di Excel salah membagi total batch dengan **17**, seharusnya **15 porsi**.
  2. `HP Kwetiaw Blackpepper Sapi` (`Std: 16.319,51` vs `Raw: 15.408,00` | `+911,51`): Di Excel kemasan `Bumbu Minyak` terketik `25,000`, seharusnya `1,000`.
  3. `Cah Jamur` (`Std: 6.900,00` vs `Raw: 6.104,00` | `+796,00`): Di Excel memakai harga sayur lokal lebih rendah daripada `DATA BASE.csv`.
  4. `Donburi Mozaru Katsu` (`Std: 15.051,00` vs `Raw: 15.618,00` | `-567,00`): Di Excel kemasan `Tomat` terketik `220`, seharusnya `1,000`.

### C. Catatan Anomali Bawaan Data Mentah 2018 (Diteruskan ke Owner)
- `Cau Katsu` (6 varian) tertulis menggunakan `6,800 gram` Pisang Galek untuk 15 porsi (`453,33 gram` per porsi).
- Ketidakseragaman takaran karbohidrat di `HOTPLATE.csv`: `HP Nasi Blackpepper Sapi` memakai `50g` Beras (varian nasi lain `125g`); `HP Kwetiaw Blackpepper Sapi/Ayam` (`50g`) & `HP Kwetiaw Siram Sapi` (`60g`) berbeda dengan varian kwetiaw lainnya (`125g`).
- `TULANG BALUNG` tercatat `1 gram` (Rp20) pada menu berkuah; dan terdapat **17 bahan baku** di `DATA BASE.csv` yang belum direferensikan oleh resep 2018 mana pun.

---

## 4. Audit Detail Tahap B: Pembersihan & Normalisasi Data Penjualan (NutaCloud)

### A. Integritas Kronologis Data Mentah (13 Bulan)
Setelah perbaikan dataset April & Mei oleh pemilik data, seluruh **13 file** CSV laporan kasir mencakup **01 Oktober 2025 – 31 Oktober 2026** (**396 hari kalender**, **395 hari aktif transaksi**; hanya tutup 1 hari pada `2026-03-21` bertepatan dengan Idul Fitri) dengan **0 file duplikat** dan **0 transaksi lintas file**.

### B. Transformasi & Pembersihan yang Diterapkan
1. **Un-merging & Konservasi Baris:** Menghapus baris footer `Grand Total` dan melakukan *forward-fill* kolom header transaksi (`Nomor`, `Tanggal`, `Pelayan`, `Tipe Penjualan`, `Metode Pembayaran`, `Masuk ke Rekening`, `Pelanggan`, `Total`, `Dibuat Oleh`, `Diubah Oleh`) di dalam masing-masing file.
2. **Pembersihan `Nomor` & Timestamp Indonesia:**
   - Memisahkan teks catatan yang bocor setelah karakter `\n` pada `Nomor` (**429** kasus, misal `SUDAH DP 150.000`, `CLAIM VOCHER TIKTOK`, `B7`) ke kolom `catatan_nomor`.
   - Mengonversi tanggal format Indonesia (`"01 Oktober 2025, 11:16:28"`) serta memecah `Dibuat Oleh` dan `Diubah Oleh` menjadi `YYYY-MM-DD HH:MM:SS`.
3. **Parsing Kolom `Pelanggan`:**
   - Memecah string majemuk (`"Desti/Lantai 2 Meja ATAS 4\nPAX = 4"`) menjadi `nama_pelanggan`, `area_lantai`, `nomor_meja`, dan `pax`, serta mengamankan kasus nama pelanggan yang memakai garis miring (`/`) tanpa informasi meja.
4. **Pemisahan Baris Produk vs Penyesuaian Keuangan:**
   - Memindahkan **17.920** baris operasional ke `fact_penyesuaian_transaksi.csv`: `Pajak Daerah` (**8.450**), `Pembulatan` (**6.935**), `Diskon Final` & `Voucher` (**1.722**), `Biaya Pengemasan` (**589**), dan `Alat Makan TKW` termasuk `Thinwal 450` (Rp9.600 pada struk `S/260318/3/46`).
   - Mempertahankan produk riil yang sebelumnya bernilai `Kategori = NaN` (`Lip Vinyl OMG` $\rightarrow$ `Produk Pinnkishfun`, `Level 4 - Ramen Redhot` $\rightarrow$ `Ramen`).
   - Mempertahankan **4 baris void/retur** (`qty <= 0`) dengan flag `is_void_adjustment = 1` agar kuantitas bersih dan pemotongan stok tetap seimbang.
5. **Ekstraksi Diskon Item & Standarisasi Kategori:**
   - Memisahkan teks `\n Diskon...` dari nama item (**792** baris berdiskon) menjadi `nama_item_bersih`, `is_diskon_item`, `label_diskon_item`, dan `nominal_diskon_item`.
   - Menyeragamkan **16 varian `Tipe Penjualan`** menjadi `channel_penjualan`: `Dine-In` (**8.286**), `Takeaway` (**422**), `GrabFood` (**265**), `ShopeeFood` (**225**), `GoFood` (**87**), `Event` (**10**), serta `brand_store` (`Ale's Place` vs `Risoldut`).
   - Menambahkan flag `is_split_payment` (**175** transaksi `Campuran`) dan `is_internal_order` (**787** transaksi meja `CREW ALES`, `OWNER`, `BUNDA LULU`, `UMI HANA`, `OPERASIONAL`, `MARKETING`, atau Diskon Crew/Owner).

### C. Hasil Pengujian Script `validate_penjualan.py`
| Metrik Validasi | Hasil Aktual | Target | Status |
| :--- | :---: | :---: | :---: |
| Konservasi total baris (`49.240` item + `17.920` penyesuaian) | **67.160** | 67.160 | ✅ **PASS** |
| Jumlah transaksi unik (`fact_transaksi.csv`) | **9.295** | 9.295 | ✅ **PASS** |
| Nilai `NULL` pada `waktu_transaksi` (header & item) | **0 / 0** | 0 / 0 | ✅ **PASS** |
| Nilai `NULL` pada `kategori_kasir` (`fact_penjualan_item`) | **0** | 0 | ✅ **PASS** |
| Rekonsiliasi struk (`subtotal_produk + diskon_nota + pajak + pembulatan + pengemasan == grand_total`, toleransi > Rp 1) | **0 selisih** | 0 selisih | ✅ **PASS** |
| `PRAGMA foreign_key_check` pada `ales_place_dwh.db` | **0 error** | 0 error | ✅ **PASS** |

---

## 5. Audit Integrasi Kasir $\leftrightarrow$ Resep BoM (`map_menu_kasir.csv`)

Hasil audit pemetaan seluruh **381 item unik** (total **58.102 porsi**, omzet net item **Rp 1.367.067.650**):

| Status Pemetaan (`match_status`) | Jumlah Item Unik | Total Qty Terjual | Persentase Qty | Total Omzet Net (Rp) | Keterangan |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `MAPPED_ALIAS` | 73 | 23.002 | 39,6% | 573.831.050 | Nama di kasir dibalik/beda ejaan dengan resep 2018 (contoh: `Redhot Beef Ramen` $\rightarrow$ `Ramen Redhot Beef`) |
| `MAPPED_EXACT` | 30 | 11.287 | 19,4% | 244.781.000 | Nama di kasir cocok persis dengan `dim_menu` |
| **Subtotal Terhubung ke BoM** | **103** | **34.289** | **59,0%** | **818.612.050** | **Siap dipakai langsung oleh mesin *BoM Stock Deduction* di Minggu 2** |
| `UNMAPPED_FNB` | 240 | 21.364 | 36,8% | 525.096.200 | Menu baru 2025–2026 (Sushi, Ramen Tomyam, Juice, Udon, Bento, Coffee, dll.) belum ada di file 2018 |
| `AMBIGUOUS_VARIANT` | 9 | 2.190 | 3,8% | 15.677.500 | Item promo/generik tanpa rasa/porsi pasti (`FREE ice cream` 1.030x, `Menu Pelajar` 818x, `Cau Katsu` 232x) |
| `UNMAPPED_NON_FNB_MERCH` | 29 | 259 | 0,4% | 7.681.900 | Produk non-makanan (`Produk Pinnkishfun` seperti Slime, Mainan, Jepit Rambut, & `Lip Vinyl OMG`) |
| **Total Keseluruhan** | **381** | **58.102** | **100,0%** | **1.367.067.650** | |

> [!NOTE]
> **Kesimpulan Cakupan Data:**  
> Meskipun cakupan resep saat ini baru **59,0%** karena keterbatasan file resep 2018 yang diberikan UMKM, hal ini **tidak menghambat** pekerjaan Minggu 2 karena mesin *BoM Stock Deduction* dan *Safety Stock* membaca tabel `dim_menu` & `fact_resep_bom` secara dinamis. Selain itu, Top 30 menu pada `UNMAPPED_FNB` saja sudah mewakili **12.190 porsi (21,0% tambahan)**, yang apabila dikonfirmasi Owner via [LAPORAN_KONFIRMASI_DATA_OWNER.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/LAPORAN_KONFIRMASI_DATA_OWNER.md) akan langsung mengangkat cakupan ke **80,0%**.

---

## 6. Keputusan *Go / No-Go* Menuju Minggu 2 (27 Nov – 3 Des 2026)

**Keputusan:** ✅ **GO — SIAP MASUK KE MINGGU 2**

### Checklist Persiapan Awal Minggu 2:
1. [ ] **Commit & Push** file terbaru (`LAPORAN_KONFIRMASI_DATA_OWNER.md` & `verifikasi/varifikasi-tugas-minggu-1.md`) ke repository GitHub (`origin/main`, posisi terakhir di commit `609a6eb`).
2. [ ] **Kirim** [LAPORAN_KONFIRMASI_DATA_OWNER.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/LAPORAN_KONFIRMASI_DATA_OWNER.md) ke PIC UMKM (Bapak Mochamad Ares Fadella) untuk melengkapi Top 30 menu baru, stok awal, dan batas *safety stock* secara paralel.
3. [ ] **Mulai Pengembangan Modul Minggu 2:**
   - Modul Python ***BoM Stock Deduction*** (membaca `ales_place_dwh.db` / `inventory_resto.db` + mencatat riwayat mutasi stok).
   - Modul ***Daily Burn Rate*, *Safety Stock*, *Days of Inventory (DOI)***, serta **Prediksi Rekomendasi *Restock* Besok**.
   - **Prototipe Dasbor Analisis Stok** dan perancangan kontrak format output JSON/API untuk integrasi dengan tim Fullstack di Minggu 3.
