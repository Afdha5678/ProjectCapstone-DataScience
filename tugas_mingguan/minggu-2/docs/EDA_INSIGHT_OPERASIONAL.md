# 📊 Laporan Analisis Bisnis & EDA Operasional Stok (Ale's Place Cipoho)
**Periode Data:** 01 Oktober 2025 – 31 Oktober 2026 (**396** hari kalender, **395** hari operasional aktif)  
**Sumber Data:** [ales_place_dwh.db](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1/output/data_penjualan/ales_place_dwh.db) (Data Primer NutaCloud $\times$ Master BoM 2018)  
**Penyusun:** Bidang Data Science (`A26-CS218`) — Afdha Auliya Atiq & Hauzan Ziyadatul Khoir

---

## 1. Pertanyaan Bisnis yang Dijawab

1. **Bagaimana pola trafik transaksi dan beban dapur antara hari kerja (*weekday*) vs akhir pekan (*weekend*), serta kapan jam tersibuk (*peak hours*)?**
2. **Apakah transaksi internal (`CREW ALES`, `OWNER`, dll.) signifikan memengaruhi pemakaian stok bahan baku?**
3. **Bahan baku apa saja yang memiliki *Daily Burn Rate* dan nilai pemakaian tertinggi sehingga wajib diprioritaskan dalam pemantauan *Safety Stock*?**
4. **Bagaimana tren musiman bulanan memengaruhi kebutuhan persediaan bahan baku?**

---

## 2. Hasil Analisis & Temuan Utama

### A. Ringkasan Trafik & Perbandingan *Weekday* vs *Weekend*
Dari total **9.295 transaksi** (**8.508** transaksi eksternal pelanggan + **787** transaksi internal) dengan total `grand_total` **Rp 1.479.571.300** (omzet eksternal **Rp 1.443.778.300**):

| Segmen Hari | Rata-Rata Transaksi / Hari | Rata-Rata Omzet / Hari | Kenaikan vs Weekday |
| :--- | :---: | :---: | :---: |
| **Weekday** *(Senin – Kamis)* | **18,24 transaksi/hari** | **Rp 2.658.250 / hari** | — |
| **Weekend** *(Jumat – Minggu)* | **30,61 transaksi/hari** | **Rp 5.200.040 / hari** | **+67,8% trafik / +95,6% omzet** |

> **Temuan Kunci:** Beban dapur dan pemakaian bahan baku pada **Jumat–Minggu hampir 2 kali lipat** dibandingkan Senin–Kamis. Oleh karena itu, perhitungan *Safety Stock* dan rekomendasi belanja hari berikutnya harus memperhitungkan faktor *weekend* (bukan memakai rata-rata datar harian).

### B. Jam Tersibuk (*Peak Hours*) & Validasi Waktu *Stock Opname*
- Top 5 jam transaksi tertinggi berpusat pada sore–malam hari:
  1. **Pukul 20:00–20:59:** **1.374 transaksi** *(puncak tertinggi)*
  2. **Pukul 19:00–19:59:** **1.239 transaksi**
  3. **Pukul 18:00–18:59:** **1.198 transaksi**
  4. **Pukul 17:00–17:59:** **971 transaksi**
  5. **Pukul 15:00–15:59:** **889 transaksi**
- **Relevansi Solusi:** Karena puncak pesanan terjadi hingga pukul **20:59**, proses pengecekan fisik gudang oleh staf memang terjadi di malam hari setelah tutup toko. Otomatisasi pemotongan stok harian langsung memangkas waktu staf menghitung ulang sisa bahan setelah shift malam yang melelahkan.

### C. Distribusi Channel Penjualan & Tren Musiman
- **Channel Dominan:** `Dine-In` (**8.286** transaksi / Rp 1,375 M), diikuti `Takeaway` (**422** transaksi), `GrabFood` (**265**), `ShopeeFood` (**225**), `GoFood` (**87**), dan `Event` (**10**).
- **Lonjakan Musiman Ramadan:** Tren bulanan relatif stabil di kisaran **Rp 73,2 juta – Rp 140,6 juta/bulan**, namun melonjak tajam pada **Maret 2026** menjadi **1.112 transaksi / Rp 214.614.500** (dipicu kategori `Paket Iftar` Ramadhan) dan tutup 1 hari pada **21 Maret 2026** (Idul Fitri).

### D. Dampak Konsumsi Internal (`CREW ALES`, `OWNER`, dll.)
- Pada menu yang terpetakan ke BoM (59,0% volume porsi), pemakaian bahan baku dari **8.508 transaksi eksternal** bernilai **Rp 271.783.071**, sedangkan dari **787 transaksi internal** bernilai **Rp 5.827.129** (~**2,1%** dari total nilai konsumsi bahan baku terukur).
- **Rekomendasi:** Transaksi internal **wajib tetap dimasukkan** ke dalam modul `BoM Stock Deduction` dan perhitungan *Daily Burn Rate* agar angka stok sistem tidak meleset lebih tinggi daripada stok fisik gudang.

### E. Top 15 Bahan Baku Berdasarkan Nilai & Laju Pemakaian (*Daily Burn Rate* 395 Hari Aktif)
Dari **178** bahan baku di master, **123 bahan** tercatat aktif terpakai pada penjualan 2025–2026 (menu terpetakan BoM). Berikut 15 bahan dengan nilai konsumsi tertinggi:

| Peringkat | Nama Bahan | Satuan | Total Terpakai (395 Hari) | Rata-Rata Harian (*Burn Rate*) | Estimasi Biaya (Rp) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | **DAGING SAPI** | `gram` | 270.860,00 | **685,72 g/hari** | 28.440.300 |
| 2 | **CHICKEN KATSU** | `gram` | 286.420,00 | **725,11 g/hari** | 27.209.900 |
| 3 | **SOYU** | `ml` | 215.440,00 | **545,42 ml/hari** | 12.926.400 |
| 4 | **TELUR** | `pcs` | 6.872,28 | **17,40 pcs/hari** | 10.464.570 |
| 5 | **BUMBU MINYAK** | `gram` | 98.200,00 | **248,61 g/hari** | 9.329.000 |
| 6 | **MIE** | `gram` | 557.060,00 | **1.410,28 g/hari** | 7.798.840 |
| 7 | **SANQUIK MANGGA** | `ml` | 103.330,00 | **261,59 ml/hari** | 7.380.721 |
| 8 | **BUMBU KERING** | `gram` | 109.282,00 | **276,66 g/hari** | 6.994.048 |
| 9 | **BERAS** | `gram` | 499.450,00 | **1.264,43 g/hari** | 6.492.850 |
| 10 | **VANILLA** | `gram` | 47.250,00 | **119,62 g/hari** | 5.670.000 |
| 11 | **SANQUIK LEMON** | `ml` | 74.550,00 | **188,73 ml/hari** | 5.421.821 |
| 12 | **AIR MINERAL** | `pcs` | 3.154,00 | **7,98 pcs/hari** | 4.731.000 |
| 13 | **NORI LEMBAR** | `pcs` | 1.332,00 | **3,37 pcs/hari** | 4.662.000 |
| 14 | **GULA PASIR** | `gram` | 357.308,00 | **904,58 g/hari** | 4.645.004 |
| 15 | **CHIKUWA** | `gram` | 78.463,51 | **198,64 g/hari** | 4.472.429 |

---

## 3. Rekomendasi Operasional untuk Sistem & Tim
1. **Prioritaskan Pemantauan Harian pada Bahan Protein & Karbohidrat Utama:** `Daging Sapi`, `Chicken Katsu`, `Telur`, `Mie`, `Beras`, dan `Soyu` menyerap porsi biaya terbesar dan cepat menipis pada akhir pekan.
2. **Terapkan Margin Toleransi (*Buffer Waste*):** Pada modul `BoM Stock Deduction`, tambahkan parameter *buffer percentage* (misal 3%–5%) untuk bahan curah/berkuah seperti minyak, tepung, dan sayuran agar selisih ceceran dapur tidak membuat stok sistem terlihat lebih besar dari fisik.
3. **Konfigurasi *Lead Time* Berbeda:** Gunakan *lead time* 1 hari untuk bahan segar/harian (sayur, daging, mie, telur) dan 3–7 hari untuk bahan kering/supplier kemasan (`Soyu`, `Sanquik`, `Bumbu Hotplate`).
4. **Tingkatkan Cakupan Resep:** Segera lengkapi Top 30 menu baru (terutama Sushi/Salmon Mentai, Ramen Tomyam, dan Juice) sesuai [LAPORAN_KONFIRMASI_DATA_OWNER.md](file:///d:/0.%20Dokumen%20Kuliah/Semester%205/0.%20Project%20Capstone/tugas_mingguan/minggu-1/docs/LAPORAN_KONFIRMASI_DATA_OWNER.md) agar sistem dapat melacak bahan utama lain seperti Salmon dan Buah Segar.
