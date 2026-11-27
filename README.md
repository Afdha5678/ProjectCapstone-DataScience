# 🍜 Project Capstone `A26-CS218` — *Stok Makanan Sudah Habis* (Scope Data Science)

**Mitra UMKM:** Ale's Place Cipoho (PIC: Bapak Mochamad Ares Fadella)  
**Tim Data Science (`DS`):** Afdha Auliya Atiq & Hauzan Ziyadatul Khoir

---

## 📁 Struktur Repository

```text
0. Project Capstone/
├── Data Bahan Makanan/                 # Data mentah resep & database bahan 2018 (9 CSV)
├── Data Penjualan/                     # Data mentah laporan penjualan NutaCloud (13 CSV)
├── PROGRESS_MINGGUAN.md                # Tracker progres mingguan (Minggu 1–4)
├── CHECKLIST_TECH_STACK_DS.md          # Acuan rubrik & pembagian peran DS / AE / FS
├── requirements.txt                    # Dependensi Python (pandas, numpy, streamlit)
├── verifikasi/                         # Folder khusus laporan audit & verifikasi
│   └── varifikasi-tugas-minggu-1.md
└── tugas_mingguan/                     # Seluruh rencana & hasil kerjaan per minggu
    ├── minggu-1/                       # Data Wrangling & Pemetaan BoM
    │   ├── plan-minggu-1-normalisasi.md
    │   ├── tugas-minggu-1-ringkasan.md
    │   ├── docs/                       # LAPORAN_KONFIRMASI_DATA_OWNER.md, AUDIT_TINJAUAN_BAHAN_MAKANAN.md
    │   ├── scripts/                    # normalize_bahan_makanan.py, clean_penjualan.py, validate_*.py
    │   └── output/                     # data_bahan_makanan/ & data_penjualan/ (CSV, SQLite DWH, SQL)
    ├── minggu-2/                       # Algoritma BoM, Safety Stock/DOI, EDA, Data AI, & Streamlit
    │   ├── plan-minggu-2.md
    │   ├── docs/                       # DATA_DICTIONARY.md, EDA_INSIGHT_OPERASIONAL.md
    │   ├── notebooks/                  # EDA_Operasional_dan_Data_AI.ipynb (Jupyter Notebook EDA + grafik)
    │   ├── scripts/                    # prepare_eda_and_ai_data.py
    │   ├── src/                        # bom_engine.py, stock_analytics.py
    │   ├── app/                        # dashboard_streamlit.py
    │   ├── tests/                      # test_minggu2.py
    │   └── output/                     # data_for_ai/ (dataset deret waktu + train/test anti-leakage)
    ├── minggu-3/                       # Rencana Integrasi Web Utama (FS) & Sinkronisasi Output
    └── minggu-4/                       # Rencana Uji Akurasi 95% & Demo UMKM
```

---

## 🚀 Cara Menjalankan Modul & Dasbor (Minggu 2)

```powershell
# 1. Jalankan unit test Minggu 2 (7/7 test)
python tugas_mingguan/minggu-2/tests/test_minggu2.py

# 2. Jalankan prototipe dasbor Streamlit (pastikan sudah pip install -r requirements.txt)
streamlit run tugas_mingguan/minggu-2/app/dashboard_streamlit.py
```

- Tracker Target: [PROGRESS_MINGGUAN.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/PROGRESS_MINGGUAN.md)
- Checklist Rubrik DS: [CHECKLIST_TECH_STACK_DS.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/CHECKLIST_TECH_STACK_DS.md)