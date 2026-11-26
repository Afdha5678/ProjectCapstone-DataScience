# 📋 Dokumen Audit & Tinjauan Data Bahan Makanan (BOM)
**Proyek:** Web Manajemen Stok Terintegrasi Kasir — Ale's Place  
**Target Data:** Hasil Normalisasi di `processed_data/` (`dim_kategori_menu`, `dim_bahan_baku`, `dim_menu`, `fact_resep_bom`, `inventory_resto.db`, `schema_and_seed.sql`)

---

## 1. Ringkasan Status Audit Teknis

| Pengecekan | Status | Hasil |
| :--- | :---: | :--- |
| Konsistensi Lintas Format (CSV vs SQLite vs `schema_and_seed.sql`) | ✅ PASS | Identik: `8` kategori, `178` bahan baku, `135` menu (`129` sellable, `6` sub-resep), `1.579` baris BOM, `1.579` baris di view `v_resep_lengkap`. |
| Integritas Foreign Key (`PRAGMA foreign_key_check`) | ✅ PASS | `0` error; eksekusi ulang `schema_and_seed.sql` pada DB kosong berjalan bersih. |
| Konsistensi Matematika Harga (`harga_beli_kemasan / isi_kemasan_beli`) | ✅ PASS | `0` selisih; `0` bahan baku berharga 0. |
| Konsistensi Satuan Dasar (`gram`, `ml`, `pcs`) | ✅ PASS | `0` mismatch antara `fact_resep_bom` dan `dim_bahan_baku` (`gram`: 117, `ml`: 27, `pcs`: 34). |
| Kelengkapan Menu | ✅ PASS | `135` dari `136` blok menu masuk (`Miruku 1` di-exclude karena stub duplikat self-referencing `Miruku Bath`). |
| Simulasi Pengurangan Stok (SQLite) | ✅ PASS | Uji transaksi `2x Ramen Soyu + 1x Takoyaki Isi 6` memotong stok sesuai satuan dasar (misal `MIE -120g`, `SOYU -40ml`, `POWDER TAKOYAKI -40g`, `AIR GALON -92.8571ml`). |

---

## 2. Poin Tinjauan Dapur & Bisnis (Perlu Konfirmasi)

> [!IMPORTANT]
> Beberapa angka berikut **sesuai persis dengan isi file CSV mentah (2018)**, namun terlihat janggal secara operasional dapur. Mohon ditinjau sebelum angka takaran dipakai untuk pemotongan stok *real-time*.

### A. Kejanggalan Takaran Bahan pada Resep Mentah
- [ ] **Pisang Galek pada `Cau Katsu` (6 Varian) = `453,33 gram` per porsi**
  - Di `DESSERT.csv` tertulis `6,800 gram` untuk 15 porsi (~0,45 kg pisang per 1 porsi camilan, memakan biaya Rp6.346 sendiri).
  - *Konfirmasi:* Apakah 1 porsi Cau Katsu memang menggunakan ~453 gram pisang, atau salah ketik dari `680 gram` (45,33 gram/porsi)?
- [ ] **Ketidakseragaman Takaran `BERAS` & `KWETIAW` di `HOTPLATE.csv`**
  - `HP Nasi Blackpepper Sapi` tertulis memakai **`50 gram` Beras**, sedangkan seluruh varian HP Nasi lainnya (`HP Nasi Siram Chicken Katsu`, `HP Nasi Redhot Ayam`, `HP Nasi Siram Sapi`) memakai **`125 gram` Beras**.
  - `HP Kwetiaw Blackpepper Sapi` & `HP Kwetiaw Blackpepper Ayam` tertulis memakai **`50 gram` Kwetiaw**, `HP Kwetiaw Siram Sapi` memakai **`60 gram` Kwetiaw**, sedangkan `HP Kwetiaw Siram Chicken Katsu` & `HP Kwetiaw Redhot Ayam` memakai **`125 gram` Kwetiaw**.
  - *Konfirmasi:* Apakah takaran tersebut perlu diseragamkan (misal Nasi = 125g, Kwetiaw = 125g), atau memang porsi Blackpepper lebih sedikit?
- [ ] **`TULANG BALUNG` = `1 gram` per porsi (Rp20)**
  - Tercatat `1 gram` di menu Hotplate, Ramen, Donburi, dan Siomay Kuah.
  - *Konfirmasi:* Dalam manajemen stok gudang, apakah ini hanya alokasi biaya kaldu tulang per porsi (sehingga tidak perlu memicu alert stok fisik 1 gram), atau ada takaran masak kaldu per panci?

---

## 3. Tinjauan Selisih HPP (`total_hpp_standar` vs `total_hpp_excel_raw`)

Terdapat **33 dari 135 menu** dengan selisih HPP > Rp 5 antara hasil kalkulasi standar (`dim_bahan_baku`) dan angka `TOTAL` di Excel mentah. Seluruh selisih berasal dari dua kategori berikut:

### A. Bug Ketikan / Rumus di Excel Mentah (Sudah Dikoreksi Otomatis)
- [ ] **Cau Katsu Bubble Gum** (`Std: Rp12.303,68` vs `Raw: Rp11.056,00` | `+Rp1.247,68`): Di Excel mentah salah membagi total batch Rp159.054 dengan **17**, padahal varian ini untuk **15 porsi** (sama dengan Cau Katsu Anggur).
- [ ] **HP Kwetiaw Blackpepper Sapi** (`Std: Rp16.319,51` vs `Raw: Rp15.408,00` | `+Rp911,51`): Di Excel mentah, kemasan `Bumbu Minyak` terketik `25,000` (nyasar dari kemasan Beras), seharusnya `1,000`.
- [ ] **Cah Jamur** (`Std: Rp6.900,00` vs `Raw: Rp6.104,00` | `+Rp796,00`): Di Excel mentah memakai harga sayur lokal lebih rendah (`Wortel` 15k vs 20k, `Jagung Semi` 10k vs 15k, `Bawang Daun` 10k vs 20k) dibanding Master `DATA BASE.csv`.
- [ ] **Donburi Mozaru Katsu** (`Std: Rp15.051,00` vs `Raw: Rp15.618,00` | `-Rp567,00`): Di Excel mentah, kemasan `Tomat` terketik `220` (nyasar dari kemasan Telur), seharusnya `1,000`.
- [ ] **Pingku Vanilla** (`Std: Rp8.415,60` vs `Raw: Rp8.859,00` | `-Rp443,40`): Di Excel mentah, harga `Cetakan Puding` pada baris ke-8 terketik `30,000`, seharusnya `7,500`.

### B. Penyeragaman Harga Master `DATA BASE.csv`
- [ ] **Sweet Takoyaki (6 varian)** (`+Rp253,71` s.d. `+Rp253,78`): Resep mentah masih memakai harga `Telur` lama (Rp1.015/pcs), sedangkan Master `DATA BASE.csv` memakai Rp1.522,73/pcs (`335,000 / 220`).
- [ ] **Minuman Kopi/Teh & Silky Pudding** (`Kopi Tubruk -Rp390,36`, `Teh Tarik -Rp224,79`, `Kopi Susu -Rp80,36`, `Hot Vietnam Coffe -Rp80,36`, `Silky Pudding -Rp33,63`): Resep mentah memakai harga terpisah `Air` (Rp6.000/9.000ml) dan `Gula` (Rp30k/17k), yang di Master disatukan ke `AIR GALON` (Rp5.000/19.000ml) dan `GULA PASIR` (Rp13.000/1.000g).
- [ ] **Ramen Shiroichi** (`+Rp209,96`): Resep mentah menulis kemasan `SUSUS DANCOW FULL CREAM` 500g, sedangkan `DATA BASE.csv` 400g (`42,000 / 400 = Rp105/g`).
- [ ] **Menu lainnya dengan selisih kecil (`< Rp350`):** `Saus Siram` (-Rp340), `Donburi Gyuniku` (+Rp327,54), `Beef Burger` (-Rp214), `HP Nasi Blackpepper Sapi` (+Rp195,51), `Ramen Chicken Katsu` (-Rp114,24), `Vanilla Blend` (+Rp94,26), `ChocoLatte` (-Rp60), `Nachos Cheese` (+Rp40,14), `Kuah Asam Manis` (+Rp40), `HP Kwetiaw Redhot Ayam` (-Rp35,67), `HP Nasi Siram Chicken Katsu` (+Rp20,33), `Pingku Manggo` (+Rp6,85), `Pingku Green Tea` (+Rp6,60).

---

## 4. Tinjauan Bahan Baku yang Belum Terpakai di Resep (17 Item)

Terdapat **17 bahan baku** di `dim_bahan_baku` (dari `DATA BASE.csv`) yang belum direferensikan oleh resep mana pun di `fact_resep_bom`:

- [ ] **Kemasan & Utilitas Operasional (7 item — wajar tidak masuk BOM per porsi atau perlu aturan khusus):**
  - `GAS`, `HI COOK`, `CUP GELAS`, `KERTAS ROTI`, `PLASTIK KLIP`, `SEDOTAN HITAM KECIL`, `TUSUK SATE`
  - *Catatan:* `GAS` dan `HI COOK` saat ini ikut ditandai `is_packaging = 1`. Di web nanti bisa dipertimbangkan memisahkan kategori *consumables/utilities* jika ingin dilacak terpisah dari kemasan makanan.
- [ ] **Bahan Makanan / Topping / Saus (10 item — cek apakah dipakai menu baru 2025–2026):**
  - `BOBBA KIWI`, `CARAMEL TOPPING`, `GARAM`, `GURITA`, `PASTA STRAWBERRY`, `PASTA TARO`, `SAOS SACHET CABE`, `SAOS SACHET TOMAT`, `SMOTIS`, `SUSU BUBUK`

---

## 5. Kesiapan Integrasi ke `Data Penjualan` (Kasir 2025–2026)

Saat dicocokkan langsung dengan **402 item jual unik** (total **58.714 porsi terjual**) pada seluruh 13 file `Data Penjualan`:
- **Exact match (case-insensitive):** hanya **30 item** (**11.287 porsi** atau **19,2%** dari total volume).
- **Akar masalah:** Banyak menu terlaris sebenarnya **sudah ada resepnya di `dim_menu`**, hanya saja penulisan kata di mesin kasir dibalik/berbeda ejaan:

| Qty Terjual | Nama Item di Kasir (`Data Penjualan`) | Padanan Resep di `dim_menu` | Status |
| :---: | :--- | :--- | :--- |
| `2,331x` | `Redhot Beef Ramen` | `Ramen Redhot Beef` | Perlu Mapping Alias |
| `1,955x` | `Le Mineral / Air Mineral` | `Air Mineral` | Perlu Mapping Alias |
| `1,355x` | `RedHot Chicken Katsu Ramen` | `Ramen Redhot Katsu` | Perlu Mapping Alias |
| `1,196x` | `BLIO Air Mineral` | `Air Mineral` | Perlu Mapping Alias |
| `1,172x` | `Chicken Katsu Ramen` | `Ramen Chicken Katsu` | Perlu Mapping Alias |
| `1,030x` | `FREE ice cream` | `Vanilla Ice Cream` / `Green Tea Ice Cream` | Perlu Mapping Varian |
| `965x` | `Pingku Greentea` | `Pingku Green Tea` | Perlu Mapping Alias |
| `809x` | `Sushi Aburi Salmon Mentai` | *(Belum ada di data 2018)* | **Perlu Resep Baru** |
| `809x` | `Shiro Ichi Ramen` | `Ramen Shiroichi` | Perlu Mapping Alias |
| `800x` | `Beef Curry Ramen` | `Ramen Curry Beef` | Perlu Mapping Alias |
| `760x` | `Soyu Ramen Original` | `Ramen Soyu` | Perlu Mapping Alias |
| `745x` | `Ramen Tomyam` | *(Belum ada di data 2018)* | **Perlu Resep Baru** |
| `705x` | `Lychee Mojito` | `Mojito Leci` | Perlu Mapping Alias |
| `688x` | `Es Teh Pucuk Harum` | *(Belum ada di data 2018)* | **Perlu Resep Baru** |
| `665x` | `Mango Juice` | *(Belum ada di data 2018)* | **Perlu Resep Baru** |

---

## 6. Rencana Tindak Lanjut Berikutnya
1. [ ] Review & konfirmasi poin takaran dapur pada **Bagian 2** dan harga pada **Bagian 3** (jika ada perubahan, cukup update aturan di `scripts/normalize_bahan_makanan.py` lalu jalankan ulang).
2. [ ] Lakukan **Normalisasi `Data Penjualan`** (13 bulan) untuk membersihkan merged rows, pajak/pembulatan, diskon, dan kolom pelanggan.
3. [ ] Buat tabel jembatan/mapping **`map_menu_kasir`** untuk menghubungkan item kasir 2025–2026 ke `dim_menu.id_menu` sekaligus mengidentifikasi daftar menu baru yang perlu diinput resepnya di aplikasi web.
