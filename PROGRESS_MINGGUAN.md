# 📅 Tracker Target Mingguan & Progres Proyek Capstone
**Tim Capstone:** `A26-CS218` — *Stok Makanan Sudah Habis* (Asah 2026)  
**UMKM Mitra:** Ale’s Place Cipoho (Owner/PIC: Mochamad Ares Fadella)  
**Use Case:** *Digitalisasi Pencatatan Stok Bahan Makanan untuk Mengurangi Kesalahan Pemrosesan Manual*  
**Acuan Rubrik & Pembagian Peran:** [CHECKLIST_TECH_STACK_DS.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/CHECKLIST_TECH_STACK_DS.md)

---

## Ringkasan Status Keseluruhan (Per 27 November 2026)

| Minggu | Periode | Fokus Utama Data Science (Project Plan Poin #2 & Checklist DS) | Status | Folder Kerja & Verifikasi |
| :--- | :--- | :--- | :---: | :--- |
| **Minggu 1** | 20 – 26 Nov 2026 | *Data wrangling* laporan NutaCloud + penyusunan skema pemetaan resep (*BoM*) ke master bahan baku | ✅ **SELESAI (100%)** | [tugas_mingguan/minggu-1/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1) • [Verifikasi M1](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/verifikasi/varifikasi-tugas-minggu-1.md) |
| **Minggu 2** | **27 Nov – 3 Des 2026** | Pengembangan algoritma ***BoM Stock Deduction*** (+ *buffer* waste), ***Safety Stock* / *Burn Rate* / *DOI***, EDA & Kamus Data, **penyiapan dataset siap-ML untuk AE**, & **prototipe dasbor Streamlit** | ✅ **SELESAI (Core DS)** *(menunggu live run Streamlit & sinkronisasi tim AE)* | [tugas_mingguan/minggu-2/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2) |
| **Minggu 3** | 4 – 10 Des 2026 | Penyusunan format output & integrasi logika konversi stok, status DOI, dan alert stok menipis ke dasbor web utama bersama tim **Full-stack** *(model ML & Gen AI API ditangani **AE**)* | ⏳ **PLANNED** | [tugas_mingguan/minggu-3/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-3) |
| **Minggu 4** | 11 – 20 Des 2026 | Pengujian akurasi pemotongan stok pakai skenario data transaksi riil (target **95%**), validasi akhir data, evaluasi demo ke UMKM, & dokumentasi | ⏳ **PLANNED** | [tugas_mingguan/minggu-4/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-4) |

---

## Rincian Checklist Target per Minggu (Khusus Scope DS)

### ✅ Minggu 1: Data Wrangling & Pemetaan BoM *(20 – 26 November 2026)*
- **Penanggung Jawab Jadwal:** Mochammad Aleandre Moulidouane (UI Web) & Tim DS (Data Wrangling)
- **Checklist Tugas DS:**
  - [x] Audit 9 file CSV `Data Bahan Makanan` & 13 file CSV `Data Penjualan` (Okt 2025 – Okt 2026, 396 hari kalender).
  - [x] Normalisasi `Data Bahan Makanan` menjadi skema relasional 3NF (`dim_kategori_menu`, `dim_bahan_baku`, `dim_menu`, `fact_resep_bom`, `inventory_resto.db`, `schema_and_seed.sql`).
  - [x] Pembersihan & normalisasi 13 bulan laporan kasir NutaCloud (`fact_transaksi.csv`, `fact_penjualan_item.csv`, `fact_penyesuaian_transaksi.csv`, `ales_place_dwh.db`).
  - [x] Penyusunan tabel mapping menu kasir $\leftrightarrow$ resep (`map_menu_kasir.csv` — 103 menu terpetakan / 59,0% volume porsi).
  - [x] Pemisahan folder data bersih ke `tugas_mingguan/minggu-1/output/` (`data_bahan_makanan/` & `data_penjualan/`).
  - [x] Pembuatan laporan konfirmasi kekurangan resep 2025–2026 ke Owner ([LAPORAN_KONFIRMASI_DATA_OWNER.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1/docs/LAPORAN_KONFIRMASI_DATA_OWNER.md)).
  - [x] Audit & verifikasi akhir Minggu 1 ([varifikasi-tugas-minggu-1.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/verifikasi/varifikasi-tugas-minggu-1.md)) dan push ke GitHub (`b231a2d`).

---

### 🔥 Minggu 2: Algoritma BoM & Safety Stock, EDA, Paket Data AI, & Dasbor Streamlit *(27 November – 3 Desember 2026)*
- **Penanggung Jawab Jadwal:** Hauzan Ziyadatul Khoir & Afdha Auliya Atiq (DS)
- **Plan Detail:** [plan-minggu-2.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/plan-minggu-2.md)
- **Checklist Tugas DS *(Tanpa mengambil job ML Forecasting / Gen AI milik AE maupun web produksi milik FS)*:**
  - [x] **Kamus Data (`DATA_DICTIONARY.md`) & Draft Format Data Tim:** Menjelaskan struktur data untuk tim FS (`PostgreSQL`/`Node.js`) & format dataset AI untuk disepakati bersama tim AE (*Ayunda & Faris*) *(Rubrik DS #6, AI #1, AI #3)* → [DATA_DICTIONARY.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/docs/DATA_DICTIONARY.md).
  - [x] **Analisis Bisnis / EDA (`EDA_INSIGHT_OPERASIONAL.md` & Notebook `.ipynb`):** Menjawab pertanyaan bisnis (pola *Senin–Minggu*, *weekday* vs *weekend*, *payday*, *channel/AOV*, gap resep, laju konsumsi bahan & dampak order internal) + visualisasi grafik *(Rubrik DS #4, #5)* → [EDA_Penjualan_dan_Bahan_Baku.ipynb](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/notebooks/EDA_Penjualan_dan_Bahan_Baku.ipynb) • [EDA_INSIGHT_OPERASIONAL.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/docs/EDA_INSIGHT_OPERASIONAL.md).
  - [x] **Paket Dataset Siap-Model untuk Tim AE (`output/data_for_ai/`):** Agregasi deret waktu harian per bahan, *feature engineering* (kalender/lag/rolling), pelabelan data primer vs simulasi, & pembagian *train/test split* anti-*data leakage* *(Rubrik AI #2, #4)* — *training & komparasi model ML dikerjakan oleh AE* → [output/data_for_ai/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/output/data_for_ai).
  - [x] **Modul Python `BoM Stock Deduction` (`src/bom_engine.py`):** Konversi rekap penjualan harian NutaCloud ke pemotongan stok bahan baku + margin toleransi (*buffer percentage* untuk waste dapur) + simulasi stok awal berlabel jelas *(Project Plan Bagian B & E; Rubrik Dasbor #4)* → [bom_engine.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/src/bom_engine.py).
  - [x] **Modul Python `Safety Stock`, `Daily Burn Rate`, & `Days of Inventory (DOI)` (`src/stock_analytics.py`):** Deteksi ambang batas stok kritis (`AMAN / MENIPIS / KRITIS`) & estimasi sisa umur stok *(Project Plan Bagian B & C)* → [stock_analytics.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/src/stock_analytics.py).
  - [x] **Prototipe Dasbor Interaktif Streamlit (`app/dashboard_streamlit.py`):** Menampilkan KPI stok *real-time*, indikator menipis/kritis, DOI, filter relevan, simulasi potong stok & opname, serta fitur **upload file CSV NutaCloud / koneksi SQLite** *(Rubrik Dasbor #1–#4, terverifikasi sintaks `py_compile`, live UI menunggu `pip install -r requirements.txt`)* → [dashboard_streamlit.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/app/dashboard_streamlit.py).
  - [ ] **Unit Test Pass (`7/7`), Verifikasi Final & Push Minggu 2:** Unit test [test_minggu2.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/tests/test_minggu2.py) lulus `7/7`; tersisa pembuatan laporan `verifikasi/varifikasi-tugas-minggu-2.md`, uji live Streamlit, & push ke GitHub.

---

### ⏳ Minggu 3: Format Output & Integrasi Logika Stok ke Web Utama *(4 – 10 Desember 2026)*
- **Penanggung Jawab Jadwal:** Faris Ambar Susilo (AE) & Seluruh Tim Integrasi
- **Plan Draft:** [plan-minggu-3-draft.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-3/plan-minggu-3-draft.md)
- **Checklist Tugas DS *(Jadwal Minggu 3 Poin #2)*:**
  - [ ] Menyusun format output standar (JSON/CSV/skema PostgreSQL) untuk hasil konversi stok BoM, *Daily Burn Rate*, *DOI*, dan alert stok menipis.
  - [ ] Berkolaborasi dengan **Full-stack (`Aleandre & Alfarisi`)** untuk mengintegrasikan logika konversi stok, indikator peringatan, & visualisasi dasbor ke website utama (`React + Node.js + PostgreSQL`) *(Rubrik Dasbor #5)*.
  - [ ] Menyediakan dukungan penyesuaian format data bila tim **AE (`Ayunda & Faris`)** membutuhkan saat integrasi model ML & Gen AI API mereka.
  - [ ] Memperbarui master resep jika balasan data konfirmasi dari Bapak Ares sudah diterima.

---

### ⏳ Minggu 4: Uji Akurasi Pemotongan Stok 95% & Evaluasi Demo UMKM *(11 – 20 Desember 2026)*
- **Penanggung Jawab:** Semua Perwakilan Bidang (`A26-CS218`)
- **Plan Draft:** [plan-minggu-4-draft.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-4/plan-minggu-4-draft.md)
- **Checklist Tugas DS *(Jadwal Minggu 4 Poin #2)*:**
  - [ ] Pengujian akurasi perhitungan pemotongan stok (`BoM Stock Deduction` & `Safety Stock/DOI`) menggunakan skenario data transaksi riil NutaCloud dengan **target akurasi $\ge$ 95%**.
  - [ ] Pemeriksaan akhir ketepatan seluruh data dan hasil analisis DS sebelum demonstrasi *(Rubrik DS #7)*.
  - [ ] Dokumentasi teknis modul DS & ikut serta dalam demonstrasi/evaluasi kepada Bapak Mochamad Ares Fadella.
