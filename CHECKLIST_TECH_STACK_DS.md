# ✅ Checklist Tech Stack & Rubrik Penilaian Data Science
**Tim Capstone:** `A26-CS218` — *Stok Makanan Sudah Habis* (Asah 2026)  
**Penanggung Jawab:** Afdha Auliya Atiq (`DS001B6Y0696`) & Hauzan Ziyadatul Khoir (`DS001B6Y0726`)  
**Terakhir Diperbarui:** 27 November 2026  

> Dokumen ini menjadi **acuan wajib** dalam setiap pengerjaan tugas mingguan agar seluruh deliverable Data Science, Dasbor, Penyediaan Data AI, dan Model Prediksi memenuhi 100% kriteria penilaian Capstone Asah 2026.

---

## Ringkasan Progres Checklist

| Kategori Rubrik | Total Item | Sudah Selesai (Verified) | Proses Minggu 2 | Target Minggu 3–4 |
| :--- | :---: | :---: | :---: | :---: |
| **1. Data Science** | 7 | **3** *(+1 parsial)* | 3 | 1 *(final check)* |
| **2. Dasbor untuk Memantau Bisnis** | 5 | 0 | **4** | **1** *(integrasi web)* |
| **3. Penyediaan Data untuk Model AI** | 4 | 0 | **4** | 0 *(revisi jika perlu)* |
| **4. Model Prediksi untuk Fitur Aplikasi** | 5 | 0 | **4** | **1** *(integrasi web)* |
| **TOTAL** | **21** | **3** | **15** | **3** |

---

## 1. Data Science (7 Kriteria)

| No | Status Awal Sheet | Status Proyek Aktual | Kriteria Rubrik | Target Minggu | Bukti / Rencana Implementasi |
| :---: | :---: | :---: | :--- | :---: | :--- |
| 1 | `TRUE` | ✅ **SELESAI** | Mengidentifikasi dan menganalisis bersama tim masalah UMKM yang akan diselesaikan dan menjelaskan peran data dalam solusi tersebut. | Minggu 0–1 | Dokumen Use Case & Wawancara Asah 2026 (*Ale's Place Cipoho — Digitalisasi Stok Bahan Makanan*). |
| 2 | `TRUE` | ✅ **SELESAI** | Merumuskan pertanyaan bisnis yang dapat dijawab melalui analisis data. | Minggu 0–1 | Rumusan prioritas masalah stok manual, penentuan bahan kritis, dan estimasi belanja esok hari. |
| 3 | `FALSE` *(siap update TRUE)* | ✅ **SELESAI** | Melakukan seluruh tahapan pengolahan data (*data wrangling*). | Minggu 1 | [normalize_bahan_makanan.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/scripts/normalize_bahan_makanan.py) & [clean_penjualan.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/scripts/clean_penjualan.py) menghasilkan dataset bersih di `processed_data/`. |
| 4 | `FALSE` | 🔄 **PROSES MINGGU 2** | Mengolah dan menganalisis data untuk menjawab pertanyaan bisnis, disertai penjelasan proses dan hasilnya. | Minggu 2 | Analisis pemakaian bahan harian (*Daily Burn Rate*), pola *weekday* vs *weekend*, dan profil item paling banyak menguras stok (disimpan di `tugas_mingguan/minggu-2/`). |
| 5 | `FALSE` | 🔄 **PROSES MINGGU 2** | Menyajikan temuan dan rekomendasi yang mudah dipahami serta relevan dengan solusi tim. | Minggu 1–2 | Laporan awal ke Owner ([LAPORAN_KONFIRMASI_DATA_OWNER.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/LAPORAN_KONFIRMASI_DATA_OWNER.md)) + laporan temuan & rekomendasi stok Minggu 2. |
| 6 | `FALSE` | 🔄 **PROSES MINGGU 2** | Menyediakan data atau hasil analisis dalam bentuk yang dapat digunakan oleh anggota tim lain, disertai penjelasan cara penggunaannya. | Minggu 1–2 | Dataset CSV & SQLite di `processed_data/` sudah tersedia; di Minggu 2 dilengkapi **Kamus Data (*Data Dictionary*) & Panduan API/Output** untuk tim Full-stack & Gen AI. |
| 7 | `FALSE` | 🟡 **PARSIAL (M1 ✅, M4 ⏳)** | Memeriksa ketepatan data dan hasil analisis sebelum digunakan dalam solusi akhir. | Minggu 1 & 4 | Ketepatan data Minggu 1 sudah diverifikasi di [varifikasi-tugas-minggu-1.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/verifikasi/varifikasi-tugas-minggu-1.md); validasi akhir akurasi model & stok (target 95%) dilakukan pada Minggu 4. |

---

## 2. Dasbor untuk Memantau Bisnis (5 Kriteria)

| No | Status Awal Sheet | Status Proyek Aktual | Kriteria Rubrik | Target Minggu | Bukti / Rencana Implementasi |
| :---: | :---: | :---: | :--- | :---: | :--- |
| 8 | `FALSE` | 🔄 **PROSES MINGGU 2** | Mengembangkan dasbor interaktif menggunakan **Streamlit** atau teknologi visualisasi lain yang sesuai. | Minggu 2 | Prototipe dasbor interaktif menggunakan **Streamlit** (`tugas_mingguan/minggu-2/` / `app/`). |
| 9 | `FALSE` | 🔄 **PROSES MINGGU 2** | Menampilkan indikator bisnis dan menyediakan filter yang relevan untuk membantu pengguna memahami kondisi bisnis. | Minggu 2 | KPI total bahan, status `KRITIS / MENIPIS / AMAN`, *Days of Inventory (DOI)*, *Daily Burn Rate*, serta filter kategori bahan/menu & rentang tanggal. |
| 10 | `FALSE` | 🔄 **PROSES MINGGU 2** | Menyediakan pembaruan data melalui **unggahan file** atau **koneksi ke sumber data**. | Minggu 2 | Koneksi langsung ke database SQLite (`ales_place_dwh.db` / `app_inventory.db`) **plus** fitur `st.file_uploader` untuk mengunggah laporan penjualan NutaCloud terbaru atau input *stock opname*. |
| 11 | `FALSE` | 🔄 **PROSES MINGGU 2** | Memprioritaskan penggunaan data primer yang diperoleh langsung dari UMKM. Jika data primer tidak tersedia atau belum mencukupi, boleh menggunakan data dummy atau data publik yang sesuai dengan karakteristik data asli. | Minggu 1–2 | Data utama berasal dari data primer NutaCloud (13 bulan) & resep 2018. Khusus **saldo stok awal gudang** (sambil menunggu data fisik Pak Ares) memakai simulasi berbasis 7 hari pemakaian dan **diberi label jelas sebagai data simulasi**. |
| 12 | `FALSE` | ⏳ **TARGET MINGGU 3** | Mengintegrasikan dasbor ke aplikasi web bersama tim Full-stack. | Minggu 3 | Menyediakan REST API / format output JSON standar untuk dihubungkan dengan dasbor web utama tim Full-stack (React.js). |

---

## 3. Penyediaan Data untuk Model AI (4 Kriteria)

| No | Status Awal Sheet | Status Proyek Aktual | Kriteria Rubrik | Target Minggu | Bukti / Rencana Implementasi |
| :---: | :---: | :---: | :--- | :---: | :--- |
| 13 | `FALSE` | 🔄 **PROSES MINGGU 2** | Menyepakati kebutuhan dan format data bersama tim Gen AI. Jika data primer tidak mencukupi, boleh menggunakan data dummy/publik dengan label jelas beserta sumber, cara pembuatan, & keterbatasannya. | Minggu 2–3 | Menyepakati skema JSON ringkasan status stok, anomali pemakaian, & rekomendasi belanja untuk fitur *explanation/AI* tim AE/Gen AI (Faris & Ayunda), termasuk pelabelan transparan untuk stok simulasi & gap resep 2018. |
| 14 | `FALSE` | 🔄 **PROSES MINGGU 2** | Melakukan pelabelan, transformasi, atau *feature engineering* sesuai kebutuhan model. | Minggu 2 | Agregasi deret waktu pemakaian harian per bahan (395 hari aktif + kalender penuh) serta fitur `day_of_week`, `is_weekend`, `is_payday`, `is_ramadan`, `lag_1/7/14`, `rolling_mean_7/14/28`. |
| 15 | `FALSE` | 🔄 **PROSES MINGGU 2** | Menyusun **kamus data (*data dictionary*)** atau penjelasan isi dataset agar mudah digunakan. | Minggu 2 | Membuat dokumentasi Kamus Data lengkap untuk seluruh tabel di `processed_data/` dan dataset fitur forecasting. |
| 16 | `FALSE` | 🔄 **PROSES MINGGU 2** | Menyiapkan pembagian data yang sesuai untuk *training* dan *testing* model serta **mencegah kebocoran data (*data leakage*)**. | Minggu 2 | Menggunakan *time-based split* murni (Train: Okt 2025 – Sep 2026; Out-of-time Test: Okt 2026) dan menghitung fitur lag/rolling secara kausal ($t < \text{target}$). |

---

## 4. Model Prediksi untuk Fitur Aplikasi (5 Kriteria)

| No | Status Awal Sheet | Status Proyek Aktual | Kriteria Rubrik | Target Minggu | Bukti / Rencana Implementasi |
| :---: | :---: | :---: | :--- | :---: | :--- |
| 17 | `FALSE` | 🔄 **PROSES MINGGU 2** | Mengembangkan model *classification*, *regression*, *forecasting*, dan model lain yang sesuai kebutuhan fitur. | Minggu 2 | Model *time-series forecasting* kebutuhan harian bahan baku untuk menghasilkan **Rekomendasi Restock Esok Hari** + klasifikasi status stok (`AMAN / MENIPIS / KRITIS`). |
| 18 | `FALSE` | 🔄 **PROSES MINGGU 2** | Melakukan *feature engineering* dan mengevaluasi pengaruhnya terhadap kinerja model. | Minggu 2 | Eksperimen perbandingan performa model *sebelum* vs *sesudah* penambahan fitur kalender/weekend/payday/lag. |
| 19 | `FALSE` | 🔄 **PROSES MINGGU 2** | Menguji model pada data yang tidak digunakan untuk *training* dengan pembagian data dan metrik evaluasi yang sesuai. | Minggu 2 & 4 | Evaluasi pada data uji *out-of-time* (Okt 2026) menggunakan metrik **MAE**, **RMSE**, dan **WAPE / sMAPE**. |
| 20 | `FALSE` | 🔄 **PROSES MINGGU 2** | Membandingkan hasil model dan menjelaskan keterbatasannya jika menguji lebih dari satu model. | Minggu 2 | Membandingkan minimal 3 pendekatan (misal *Seasonal Weekday/Weekend Baseline*, *Ridge Regression*, dan *Random Forest / LightGBM*), lengkap dengan analisis trade-off dan keterbatasan dataset. |
| 21 | `FALSE` | ⏳ **TARGET MINGGU 3** | Mengintegrasikan hasil prediksi ke aplikasi web bersama tim Full-stack. | Minggu 3 | Mengekspos endpoint prediksi & rekomendasi belanja esok hari melalui API Python agar tampil di aplikasi web utama. |
