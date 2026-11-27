# 📦 Ringkasan Tugas Minggu 1 (20 – 26 November 2026)

**Status:** ✅ **SELESAI & TERVERIFIKASI**  
**Penanggung Jawab Data Science:** Afdha Auliya Atiq & Hauzan Ziyadatul Khoir

---

## Dokumen Terkait Minggu 1
- **Plan Awal:** [plan-minggu-1-normalisasi.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1/plan-minggu-1-normalisasi.md)
- **Laporan Audit & Verifikasi:** [varifikasi-tugas-minggu-1.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/verifikasi/varifikasi-tugas-minggu-1.md)
- **Laporan Konfirmasi Owner:** [LAPORAN_KONFIRMASI_DATA_OWNER.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/LAPORAN_KONFIRMASI_DATA_OWNER.md)

## Artefak Kode & Data yang Dihasilkan
1. **Scripts ETL & Validasi (`scripts/`):**
   - `normalize_bahan_makanan.py`, `validate_data.py`
   - `clean_penjualan.py`, `validate_penjualan.py`
2. **Dataset Bahan Makanan & BoM (`processed_data/data_bahan_makanan/`):**
   - `dim_kategori_menu.csv` (8), `dim_bahan_baku.csv` (178), `dim_menu.csv` (135), `fact_resep_bom.csv` (1.579), `inventory_resto.db`, `schema_and_seed.sql`, `AUDIT_TINJAUAN_BAHAN_MAKANAN.md`
3. **Dataset Penjualan & Mapping Kasir (`processed_data/data_penjualan/`):**
   - `fact_transaksi.csv` (9.295), `fact_penjualan_item.csv` (49.240), `fact_penyesuaian_transaksi.csv` (17.920), `map_menu_kasir.csv` (381), `ales_place_dwh.db`
