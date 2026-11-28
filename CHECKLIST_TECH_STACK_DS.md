# ✅ Checklist Tech Stack & Rubrik Penilaian Data Science
**Tim Capstone:** `A26-CS218` — *Stok Makanan Sudah Habis* (Asah 2026)  
**Penanggung Jawab Data Science:** Afdha Auliya Atiq (`DS001B6Y0696`) & Hauzan Ziyadatul Khoir (`DS001B6Y0726`)  
**Sumber Acuan:** Dokumen Project Plan `A26-CS218` & Checklist Tech Stack Asah 2026  
**Terakhir Diperbarui:** 27 November 2026  

> **Pembagian Peran Resmi Tim `A26-CS218` (Mengacu Project Plan Halaman 2–6 & 10–13):**
> - **Data Science Specialist (`DS` — Afdha & Hauzan):** *Data wrangling*, EDA & analisis bisnis, Kamus Data, **penyediaan dataset siap-AI untuk tim AE**, algoritma Python **`BoM Stock Deduction`** (termasuk *buffer* margin waste), **`Daily Burn Rate` / `Safety Stock` / `Days of Inventory (DOI)`**, serta **prototipe dasbor Streamlit**.
> - **Next-Gen AI Engineer (`AE` — Ayunda & Faris):** Membangun & membandingkan **model ML *forecasting*** (prediksi kebutuhan stok esok hari), *REST API inference* (FastAPI), serta fitur **Generative AI** (*ChatGPT/Gemini API explanation*).
> - **AI Full-Stack Developer (`FS` — Aleandre & Alfarisi):** Web utama (`React + Vite`), backend (`Node.js`), database (`PostgreSQL`), replikasi aplikasi kasir NutaCloud, CRUD stok/opname, & *deployment*.

---

## Ringkasan Progres Checklist

| Kategori Rubrik | Total Item | Sudah Selesai | Fokus DS Minggu 2 | Target Minggu 3–4 / Catatan Peran |
| :--- | :---: | :---: | :---: | :--- |
| **1. Data Science** | 7 | **6** *(+1 parsial)* | **3 selesai** | 1 *(final check akurasi 95% di M4)* |
| **2. Dasbor untuk Memantau Bisnis** | 5 | **4** *(kode terverifikasi sintaks, live UI tunggu install `streamlit`)* | **4 selesai (kode)** | **1** *(integrasi ke web FS di M3)* |
| **3. Penyediaan Data untuk Model AI** | 4 | **3** *(+1 menunggu konfirmasi format tim AE)* | **3 selesai + 1 sinkronisasi** | Menyuplai dataset siap-latih untuk tim **AE** |
| **4. Model Prediksi untuk Fitur Aplikasi** | 5 | — | — | **Dipimpin Tim AE (Ayunda & Faris)** sesuai Project Plan |
| **TOTAL SCOPE LANGSUNG DS (Bagian 1–3)** | **16** | **13** *(+2 parsial/sinkronisasi)* | **10 selesai + 1 sinkronisasi** | **2** *(M3 & M4)* |

---

## 1. Data Science (7 Kriteria — Fokus Utama DS)

| No | Status Awal Sheet | Status Proyek Aktual | Kriteria Rubrik | Target Minggu | Bukti / Rencana Implementasi |
| :---: | :---: | :---: | :--- | :---: | :--- |
| 1 | `TRUE` | ✅ **SELESAI** | Mengidentifikasi dan menganalisis bersama tim masalah UMKM yang akan diselesaikan dan menjelaskan peran data dalam solusi tersebut. | Minggu 0–1 | Dokumen Use Case & Project Plan `A26-CS218` (*Ale's Place Cipoho — Digitalisasi Stok Bahan Makanan*). |
| 2 | `TRUE` | ✅ **SELESAI** | Merumuskan pertanyaan bisnis yang dapat dijawab melalui analisis data. | Minggu 0–1 | Rumusan masalah pemantauan stok manual, laju konsumsi harian, dan deteksi ambang batas stok kritis. |
| 3 | `FALSE` *(siap update TRUE)* | ✅ **SELESAI** | Melakukan seluruh tahapan pengolahan data (*data wrangling*). | Minggu 1 | [normalize_bahan_makanan.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1/scripts/normalize_bahan_makanan.py) & [clean_penjualan.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1/scripts/clean_penjualan.py) menghasilkan dataset bersih di `tugas_mingguan/minggu-1/output/`. |
| 4 | `FALSE` | ✅ **SELESAI** | Mengolah dan menganalisis data untuk menjawab pertanyaan bisnis, disertai penjelasan proses dan hasilnya. | Minggu 2 | [EDA_Penjualan_dan_Bahan_Baku.ipynb](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/notebooks/EDA_Penjualan_dan_Bahan_Baku.ipynb), [EDA_INSIGHT_OPERASIONAL.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/docs/EDA_INSIGHT_OPERASIONAL.md), & [stock_analytics.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/src/stock_analytics.py) (*Daily Burn Rate*, *weekday* vs *weekend*, *Safety Stock* / *DOI*). |
| 5 | `FALSE` | ✅ **SELESAI** | Menyajikan temuan dan rekomendasi yang mudah dipahami serta relevan dengan solusi tim. | Minggu 1–2 | [LAPORAN_KONFIRMASI_DATA_OWNER.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1/docs/LAPORAN_KONFIRMASI_DATA_OWNER.md) + rekomendasi operasional *re-stock* & *buffer* di [EDA_INSIGHT_OPERASIONAL.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/docs/EDA_INSIGHT_OPERASIONAL.md). |
| 6 | `FALSE` | ✅ **SELESAI** | Menyediakan data atau hasil analisis dalam bentuk yang dapat digunakan oleh anggota tim lain, disertai penjelasan cara penggunaannya. | Minggu 1–2 | [DATA_DICTIONARY.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/docs/DATA_DICTIONARY.md), dataset [data_for_ai/](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/output/data_for_ai), & modul Python [bom_engine.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/src/bom_engine.py) + [stock_analytics.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/src/stock_analytics.py) untuk **AE** & **FS**. |
| 7 | `FALSE` | 🟡 **PARSIAL (M1 ✅, M2 Unit Test ✅, M4 ⏳)** | Memeriksa ketepatan data dan hasil analisis sebelum digunakan dalam solusi akhir. | Minggu 1 & 4 | Audit data M1 di [varifikasi-tugas-minggu-1.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/verifikasi/varifikasi-tugas-minggu-1.md) & 7/7 unit test logika M2 ([test_minggu2.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/tests/test_minggu2.py)); uji validasi akurasi pemotongan stok **95%** dengan transaksi riil pada Minggu 4. |

---

## 2. Dasbor untuk Memantau Bisnis (5 Kriteria — Fokus Utama DS)

| No | Status Awal Sheet | Status Proyek Aktual | Kriteria Rubrik | Target Minggu | Bukti / Rencana Implementasi |
| :---: | :---: | :---: | :--- | :---: | :--- |
| 8 | `FALSE` | ✅ **SELESAI (Prototipe)** | Mengembangkan dasbor interaktif menggunakan **Streamlit** atau teknologi visualisasi lain yang sesuai. | Minggu 2 | [dashboard_streamlit.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/app/dashboard_streamlit.py) terverifikasi `py_compile` *(tinggal `pip install -r requirements.txt` untuk live UI preview)*. |
| 9 | `FALSE` | ✅ **SELESAI (Prototipe)** | Menampilkan indikator bisnis dan menyediakan filter yang relevan untuk membantu pengguna memahami kondisi bisnis. | Minggu 2 | KPI total stok, status `KRITIS / MENIPIS / AMAN`, *Daily Burn Rate*, *Safety Stock*, *ROP*, *Days of Inventory (DOI)*, filter vendor/status, & tab EDA di [dashboard_streamlit.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/app/dashboard_streamlit.py). |
| 10 | `FALSE` | ✅ **SELESAI (Prototipe)** | Menyediakan pembaruan data melalui **unggahan file** atau **koneksi ke sumber data**. | Minggu 2 | Koneksi langsung ke SQLite (`ales_place_dwh.db`) + widget `st.file_uploader` CSV NutaCloud & input Stock-In/Opname via [bom_engine.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/src/bom_engine.py). |
| 11 | `FALSE` | ✅ **SELESAI** | Memprioritaskan penggunaan data primer yang diperoleh langsung dari UMKM. Jika data primer tidak tersedia atau belum mencukupi, boleh menggunakan data dummy atau data publik yang sesuai dengan karakteristik data asli. | Minggu 1–2 | Memakai data primer NutaCloud (13 bulan) & resep 2018. Saldo stok awal simulasi 7 hari historis diberi kolom label jelas `is_simulated_stock = True` & `data_label = SIMULASI_7_HARI_HISTORIS`. |
| 12 | `FALSE` | ⏳ **TARGET MINGGU 3** | Mengintegrasikan dasbor ke aplikasi web bersama tim Full-stack. | Minggu 3 | Menyusun format output standar & bekerja sama dengan tim **FS (Aleandre & Alfarisi)** agar hasil konversi stok, DOI, & alert menipis tampil di dasbor web utama (`React + Node.js + PostgreSQL`). |

---

## 3. Penyediaan Data untuk Model AI (4 Kriteria — Kolaborasi DS $\rightarrow$ AE)

| No | Status Awal Sheet | Status Proyek Aktual | Kriteria Rubrik | Target Minggu | Bukti / Rencana Implementasi |
| :---: | :---: | :---: | :--- | :---: | :--- |
| 13 | `FALSE` | 🟡 **SIAP KESEPAKATAN TIM AE** | Menyepakati kebutuhan dan format data bersama tim Gen AI / AI Engineer. Jika data primer tidak mencukupi, boleh menggunakan data dummy/publik dengan label jelas beserta sumber, cara pembuatan, & keterbatasannya. | Minggu 2 | Spesifikasi format CSV + kamus data + label `data_source_label` (`PRIMARY_NUTACLOUD_X_BOM2018_PARTIAL_59PCT`) & limitasi sudah ditulis di [DATA_DICTIONARY.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/docs/DATA_DICTIONARY.md); tinggal konfirmasi final dengan **Ayunda & Faris (AE)**. |
| 14 | `FALSE` | ✅ **SELESAI** | Melakukan pelabelan, transformasi, atau *feature engineering* sesuai kebutuhan model. | Minggu 2 | [prepare_eda_and_ai_data.py](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/scripts/prepare_eda_and_ai_data.py) menghasilkan 63.756 baris deret waktu harian (396 hari $\times$ 161 bahan aktif) dengan fitur kalender, lag (`1/7/14`), dan rolling mean kausal (`7/28`). |
| 15 | `FALSE` | ✅ **SELESAI** | Menyusun **kamus data (*data dictionary*)** atau penjelasan isi dataset agar mudah digunakan. | Minggu 2 | [DATA_DICTIONARY.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-2/docs/DATA_DICTIONARY.md) mencakup skema tabel DWH, dataset AI, rumus stok, satuan (`gram`/`ml`/`pcs`), dan keterbatasan data. |
| 16 | `FALSE` | ✅ **SELESAI** | Menyiapkan pembagian data yang sesuai untuk *training* dan *testing* model serta **mencegah kebocoran data (*data leakage*)**. | Minggu 2 | Split temporal bebas *leakage* (`train_daily_usage.csv`: `2025-10-01` s.d. `2026-09-30` = 58.765 baris; `test_daily_usage.csv`: `2026-10-01` s.d. `2026-10-31` = 4.991 baris) terverifikasi oleh `test_ai_dataset_anti_leakage`. |

---

## 4. Model Prediksi untuk Fitur Aplikasi *(Tanggung Jawab Tim AE — Project Plan Hal. 4–5, 11, 13)*

> [!NOTE]
> Berdasarkan dokumen **Project Plan `A26-CS218`**, pengembangan model Machine Learning *forecasting* prediksi stok hari berikutnya, komparasi model regresi, *REST API inference*, dan integrasi *Generative AI* merupakan tugas **Next-Gen AI Engineer (`AE`: Ayunda Nugraheni K. & Faris Ambar Susilo)**.  
> **Peran DS pada bagian ini hanya mendukung dari sisi penyediaan data siap-latih (Bagian 3 di atas) dan tidak mengambil alih pemodelan ML atau API AE.**

| No | Kriteria Rubrik | Penanggung Jawab Resmi (Project Plan) | Dukungan dari DS |
| :---: | :--- | :---: | :--- |
| 17 | Mengembangkan model *forecasting* / regresi kebutuhan stok hari berikutnya | **AE** *(Ayunda & Faris)* | Menyuplai dataset deret waktu bersih (`daily_ingredient_usage`) |
| 18 | Melakukan *feature engineering* & mengevaluasi pengaruhnya pada model ML | **AE** *(Ayunda & Faris)* | Menyediakan fitur dasar kalender/lag di dataset & Kamus Data |
| 19 | Menguji model pada data hold-out dengan metrik MAE/RMSE | **AE** *(Ayunda & Faris)* | Menyediakan split *train/test* anti-leakage (Okt 2025–Sep 2026 vs Okt 2026) |
| 20 | Membandingkan minimal dua model & menjelaskan keterbatasannya | **AE** *(Ayunda & Faris)* | Memberikan dokumentasi keterbatasan data mentah (gap resep 2018 & stok simulasi) |
| 21 | Mengintegrasikan hasil prediksi & REST API ke website | **AE** & **FS** | Menyamakan format `id_bahan`, `nama_bahan`, dan `satuan_dasar` |
