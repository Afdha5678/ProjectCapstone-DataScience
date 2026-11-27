# 🌐 Draft Plan Minggu 3: Integrasi Web Utama, API & Fitur Penjelasan AI
**Periode Target:** 4 – 10 Desember 2026  
**Penanggung Jawab Jadwal:** Faris Ambar Susilo (AE) & Seluruh Tim (`A26-CS218`)  
**Status:** ⏳ Menunggu Penyelesaian Minggu 2

---

## Target Kerja Minggu 3 (Jadwal + Rubrik Tech Stack DS)
1. **Backend API Integration (`src/api.py` — FastAPI):**
   - Membungkus `bom_engine.py`, `stock_analytics.py`, dan `restock_forecaster.py` menjadi endpoint REST API berformat JSON standar.
2. **Integrasi Dasbor & Prediksi ke Aplikasi Web Full-Stack (`Dasbor #5`, `Model Prediksi #5`):**
   - Menghubungkan output konversi stok, status `AMAN/MENIPIS/KRITIS`, *Days of Inventory*, dan rekomendasi belanja besok ke aplikasi web React.js & replikasi kasir NutaCloud yang dibangun tim Full-stack (Aleandre & Alfarisi).
3. **Integrasi Data ke Fitur Penjelasan Gen AI (`Penyediaan Data AI #1`):**
   - Menyediakan endpoint/payload JSON terstruktur berisi alasan stok menipis, lonjakan pemakaian, dan keterbatasan data untuk dipakai fitur penjelasan API tim AE/Gen AI.
4. **Update Master Resep (Jika Balasan Owner Sudah Masuk):**
   - Memasukkan tambahan resep Top 30 menu baru & stok awal riil dari Bapak Mochamad Ares Fadella ke `dim_menu` & `fact_resep_bom`.
