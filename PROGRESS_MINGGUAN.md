# 📅 Tracker Target Mingguan & Progres Proyek Capstone
**Tim Capstone:** `A26-CS218` — *Stok Makanan Sudah Habis* (Asah 2026)  
**UMKM Mitra:** Ale’s Place Cipoho (Owner/PIC: Mochamad Ares Fadella)  
**Use Case:** *Digitalisasi Pencatatan Stok Bahan Makanan untuk Mengurangi Kesalahan Pemrosesan Manual*  
**Acuan Rubrik:** [CHECKLIST_TECH_STACK_DS.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/CHECKLIST_TECH_STACK_DS.md)

---

## Ringkasan Status Keseluruhan (Per 27 November 2026)

| Minggu | Periode | Fokus Utama Data Science (Poin #2) | Status | Folder Kerja & Verifikasi |
| :--- | :--- | :--- | :---: | :--- |
| **Minggu 1** | 20 – 26 Nov 2026 | *Data wrangling* laporan NutaCloud + pemetaan resep (*BoM*) ke master bahan baku | ✅ **SELESAI (100%)** | [tugas_mingguan/minggu-1/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1) • [Verifikasi M1](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/verifikasi/varifikasi-tugas-minggu-1.md) |
| **Minggu 2** | **27 Nov – 3 Des 2026** | Algoritma *BoM Stock Deduction*, *Safety Stock* / *Burn Rate* / *DOI*, Model Prediksi *Restock* (komparasi model + Kamus Data), & Prototipe Dasbor **Streamlit** | 🔥 **IN PROGRESS (Hari ke-1)** | [tugas_mingguan/minggu-2/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2) |
| **Minggu 3** | 4 – 10 Des 2026 | Format output API & integrasi logika konversi stok, prediksi *restock*, serta indikator peringatan ke web utama Full-stack & fitur penjelasan Gen AI | ⏳ **PLANNED** | [tugas_mingguan/minggu-3/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-3) |
| **Minggu 4** | 11 – 20 Des 2026 | Pengujian akurasi pemotongan stok & prediksi pakai data riil (target **95%**), evaluasi demo ke UMKM, perbaikan akhir, & dokumentasi final | ⏳ **PLANNED** | [tugas_mingguan/minggu-4/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-4) |

---

## Rincian Checklist Target per Minggu

### ✅ Minggu 1: Data Wrangling & Pemetaan BoM *(20 – 26 November 2026)*
- **Penanggung Jawab Utama Jadwal:** Mochammad Aleandre Moulidouane (UI Web) & Tim DS (Data Wrangling)
- **Checklist Tugas:**
  - [x] Audit 9 file CSV `Data Bahan Makanan` & 13 file CSV `Data Penjualan` (Okt 2025 – Okt 2026, 396 hari kalender).
  - [x] Normalisasi `Data Bahan Makanan` menjadi skema relasional 3NF (`dim_kategori_menu`, `dim_bahan_baku`, `dim_menu`, `fact_resep_bom`, `inventory_resto.db`, `schema_and_seed.sql`).
  - [x] Pembersihan & normalisasi 13 bulan laporan kasir NutaCloud (`fact_transaksi.csv`, `fact_penjualan_item.csv`, `fact_penyesuaian_transaksi.csv`, `ales_place_dwh.db`).
  - [x] Penyusunan tabel mapping menu kasir $\leftrightarrow$ resep (`map_menu_kasir.csv` — 103 menu terpetakan / 59,0% volume porsi).
  - [x] Pemisahan folder data bersih (`processed_data/data_bahan_makanan/` & `processed_data/data_penjualan/`).
  - [x] Pembuatan laporan konfirmasi kekurangan resep 2025–2026 ke Owner ([LAPORAN_KONFIRMASI_DATA_OWNER.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/LAPORAN_KONFIRMASI_DATA_OWNER.md)).
  - [x] Audit & verifikasi akhir Minggu 1 ([varifikasi-tugas-minggu-1.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/verifikasi/varifikasi-tugas-minggu-1.md)) dan push ke GitHub (`b231a2d`).

---

### 🔥 Minggu 2: Algoritma Stok, Model Prediksi & Prototipe Dasbor *(27 November – 3 Desember 2026)*
- **Penanggung Jawab Utama Jadwal:** Hauzan Ziyadatul Khoir & Afdha Auliya Atiq (DS)
- **Plan Detail:** [plan-minggu-2.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/plan-minggu-2.md)
- **Checklist Tugas (Mengacu Jadwal + Rubrik Tech Stack DS):**
  - [ ] **Kamus Data & Dokumentasi Dataset (`Data Dictionary`)** untuk tim Full-stack & Gen AI *(Rubrik DS #6, AI #1, AI #3)*.
  - [ ] **Analisis Data Bisnis (EDA)** untuk menjawab pertanyaan operasional (pola *burn rate*, *weekday* vs *weekend*, bahan paling kritis) *(Rubrik DS #4, #5)*.
  - [ ] **Modul `BoM Stock Deduction` + `Stock Ledger`** (`deduct_from_sales`, `stock_in_purchase`, `stock_opname` malam hari, label jelas untuk stok simulasi awal) *(Rubrik Dasbor #4)*.
  - [ ] **Modul `Safety Stock`, `Daily Burn Rate`, & `Days of Inventory (DOI)`** dengan indikator `AMAN / MENIPIS / KRITIS`.
  - [ ] **Model Prediksi Rekomendasi *Restock* Besok:** *Feature engineering*, *time-based split* tanpa *data leakage*, perbandingan $\ge 2$ model (Baseline vs Regresi vs Tree-based), evaluasi MAE/RMSE/WAPE, dan catatan keterbatasan model *(Rubrik AI #2, #4 & Model Prediksi #1–#4)*.
  - [ ] **Prototipe Dasbor Interaktif Streamlit:** Menampilkan KPI, filter relevan, simulasi kasir/opname, grafik *burn rate*, dan fitur **upload file CSV NutaCloud / koneksi SQLite** *(Rubrik Dasbor #1–#4)*.
  - [ ] **Unit Test & Verifikasi Minggu 2:** Simpan laporan verifikasi di `verifikasi/varifikasi-tugas-minggu-2.md` & push ke GitHub.

---

### ⏳ Minggu 3: Integrasi Web, API & Penjelasan AI *(4 – 10 Desember 2026)*
- **Penanggung Jawab Utama Jadwal:** Faris Ambar Susilo (AE) & Seluruh Tim Integrasi
- **Plan Draft:** [plan-minggu-3-draft.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-3/plan-minggu-3-draft.md)
- **Checklist Tugas:**
  - [ ] Penyusunan & finalisasi format output API JSON (`FastAPI` / backend service) untuk konversi stok, DOI, alert menipis, dan prediksi *restock*.
  - [ ] Integrasi dasbor & hasil prediksi ke aplikasi web utama bersama tim Full-stack *(Rubrik Dasbor #5, Model Prediksi #5)*.
  - [ ] Sinkronisasi dengan replikasi kasir NutaCloud yang dibuat tim Full-stack.
  - [ ] Integrasi format data untuk fitur penjelasan AI (*Gen AI / API explanation*) bersama tim AE *(Rubrik AI #1)*.
  - [ ] Update resep tambahan jika sudah ada balasan konfirmasi dari Bapak Ares.

---

### ⏳ Minggu 4: Validasi Akurasi 95%, Evaluasi & Demo UMKM *(11 – 20 Desember 2026)*
- **Penanggung Jawab:** Semua Perwakilan Bidang (`A26-CS218`)
- **Plan Draft:** [plan-minggu-4-draft.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-4/plan-minggu-4-draft.md)
- **Checklist Tugas:**
  - [ ] Pengujian akurasi pemotongan stok & prediksi *restock* menggunakan skenario data transaksi riil NutaCloud dengan **target akurasi $\ge$ 95%**.
  - [ ] Pemeriksaan akhir ketepatan seluruh data, analisis, dan batasan model sebelum demo *(Rubrik DS #7)*.
  - [ ] Penyusunan dokumentasi teknis & *user manual* untuk staf operasional Ale's Place Cipoho.
  - [ ] Demonstrasi ke Owner UMKM (Bapak Mochamad Ares Fadella), pengumpulan feedback, & perbaikan akhir.
