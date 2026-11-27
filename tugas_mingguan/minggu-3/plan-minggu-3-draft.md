# 🌐 Draft Plan Minggu 3: Format Output & Integrasi Logika Stok ke Web Utama
**Periode Target:** 4 – 10 Desember 2026  
**Penanggung Jawab Utama Jadwal:** Faris Ambar Susilo (AE) & Seluruh Tim Integrasi  
**Status:** ⏳ Menunggu Penyelesaian Minggu 2

> [!NOTE]
> **Pembagian Tugas Resmi Minggu 3 (Sesuai Project Plan Halaman 6):**
> - **Full-stack (`Aleandre & Alfarisi`):** Pembuatan replikasi aplikasi kasir NutaCloud di web (`React + Node.js + PostgreSQL`).
> - **Data Science (`Afdha & Hauzan` — Pekerjaan #2):** Penyusunan format output dan integrasi logika konversi stok (`BoM Stock Deduction`), status sisa umur stok (`DOI`), & indikator peringatan stok menipis (`Safety Stock`) ke dasbor web utama bersama tim FS.
> - **AI Engineer (`Faris & Ayunda` — Pekerjaan #3):** Integrasi model ML forecasting dan fitur Generative AI API (Gemini/OpenAI) ke website.

---

## Target Kerja Khusus DS Minggu 3
1. **Penyusunan Format Output Standar (JSON / Skema PostgreSQL):**
   - Menyiapkan spesifikasi struktur output dari `bom_engine.py` & `stock_analytics.py` (konversi potongan bahan, status `AMAN/MENIPIS/KRITIS`, *Daily Burn Rate*, *DOI*) agar mudah dikonsumsi backend `Node.js` + `PostgreSQL` tim Full-stack.
2. **Integrasi Dasbor & Logika Stok Bersama Tim Full-stack (`Dasbor #5`):**
   - Mendampingi Aleandre & Alfarisi menghubungkan alur *upload/input* rekap harian NutaCloud di website ke logika pemotongan stok otomatis dan indikator visual dasbor utama.
3. **Koordinasi Format Data untuk Tim AE (`AI #1`):**
   - Memberikan dukungan jika tim AE membutuhkan penyesuaian dataset atau menyelaraskan kode `id_bahan`/`satuan_dasar` antara hasil prediksi ML mereka dengan tabel stok utama.
4. **Update Master Resep (Jika Balasan Konfirmasi Owner Sudah Masuk):**
   - Memasukkan tambahan takaran Top 30 menu baru & stok awal riil dari Bapak Mochamad Ares Fadella ke master resep dan melakukan re-sync ke database tim.
