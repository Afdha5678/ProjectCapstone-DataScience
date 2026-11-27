# 📄 Laporan Evaluasi Kelengkapan Data & Permohonan Konfirmasi Operasional
**Kepada Yth:** Bapak Mochamad Ares Fadella (Owner / PIC Ale’s Place Cipoho)  
**Dari:** Tim Capstone Asah 2026 — A26-CS218 (*Stok Makanan Sudah Habis*)  
**Tanggal:** 27 November 2026  
**Perihal:** Rincian Kekurangan Data Resep Menu Terbaru (2025–2026) & Konfirmasi Kebutuhan Sistem Stok  

---

## 1. Pengantar & Ringkasan Kondisi Data Saat Ini

Terima kasih banyak atas data laporan penjualan **NutaCloud** (13 bulan) dan file **Data Bahan Baku & Resep Menu (2018)** yang telah Bapak berikan. Tim kami telah menyelesaikan proses pembersihan dan pencocokan seluruh data tersebut untuk membangun sistem pencatatan & pemotongan stok bahan baku otomatis.

Dari hasil pemeriksaan data yang masuk, berikut gambaran kondisinya:

| Jenis Data | Kondisi Saat Ini | Keterangan |
| :--- | :--- | :--- |
| **Data Penjualan Kasir (NutaCloud)** | ✅ **Lengkap & Bersih** | Periode **01 Okt 2025 – 31 Okt 2026** (13 bulan penuh, **9.295 transaksi**, **58.102 porsi terjual** dari **381 item unik**). |
| **Data Bahan Baku & Resep (2018)** | ⚠️ **Perlu Pembaruan & Pelengkapan** | Tersedia **178 bahan baku** dan **129 resep menu jual** standar tahun 2018. |
| **Hasil Pencocokan Kasir $\leftrightarrow$ Resep** | ⚠️ **Baru Mencakup 59,0% Penjualan** | **103 menu** (**34.289 porsi**) sudah cocok dengan resep 2018. Masih ada **240 item makanan/minuman baru (21.364 porsi / 36,8%)** dan **9 menu varian/promo umum (2.190 porsi / 3,8%)** yang belum memiliki data takaran resep. |

> **Mengapa konfirmasi ini penting?**  
> Agar fitur **pemotongan stok otomatis** dan **rekomendasi belanja esok hari** di aplikasi web nantinya akurat (menuju target validasi **95%**), sistem perlu mengetahui takaran bahan baku dari menu-menu baru yang sekarang laris terjual di tahun 2025–2026 (seperti Sushi, Ramen Tomyam, Juice, Udon, Bento, Coffee, dll.).

---

## 2. Daftar Permintaan Data & Konfirmasi kepada Owner

Agar tidak merepotkan Bapak, kami membagi permintaan konfirmasi menjadi **4 bagian prioritas** yang paling mudah dan cepat untuk dijawab.

### 🔹 Bagian A: Prioritas Utama — Top 30 Menu Terlaris yang Belum Memiliki Resep
Cukup melengkapi **30 menu terlaris di bawah ini** saja, cakupan pemotongan stok otomatis langsung meningkat dari **59,0% menjadi 80,0% (+12.190 porsi)**!

*(Catatan: Untuk minuman botol/kemasan jadi, Bapak cukup tulis **"1 botol/pcs langsung"**. Untuk menu yang hanya ganti lauk/topping dari menu lama, cukup tulis **"sama seperti menu X, ganti lauk ..."***)*

| No | Nama Menu di Kasir NutaCloud | Kategori | Terjual (13 Bln) | Mohon Diisi: Bahan Baku & Takaran per 1 Porsi (gram / ml / pcs) |
| :---: | :--- | :--- | :---: | :--- |
| 1 | **Sushi Aburi Salmon Mentai** | Sushi | 809x | *(Contoh: Beras 125g, Salmon ...g, Nori ...pcs, Saus Mentai ...g, dll)* |
| 2 | **Ramen Tomyam** | Ramen | 745x | |
| 3 | **Es Teh Pucuk Harum** | Minuman | 688x | *(Konfirmasi: apakah 1 porsi = 1 botol kemasan + Es Batu ...g?)* |
| 4 | **Mango Juice** | Varian Juice | 665x | |
| 5 | **Orange Juice** | Varian Juice | 619x | |
| 6 | **Kulit Salmon Crispy - Pack** | Pack Ekonomis | 583x | |
| 7 | **Extra Ice Cube** | Minuman | 505x | *(Berapa gram es batu per porsi?)* |
| 8 | **Sushi Aburi Salmon Cheese** | Sushi | 466x | |
| 9 | **Takoyaki Mentai** | Tako Oko Yakitori | 454x | *(Apakah sama dengan Takoyaki Isi 6 + Saus Mentai ...g?)* |
| 10 | **Gyozaa** | Snack | 446x | *(Isi berapa pcs per porsi + bahan sausnya?)* |
| 11 | **Greentea Shake** | Drink Shake | 431x | *(Apakah takarannya sama dengan Green Tea Blended?)* |
| 12 | **Extra Gurita** | Ala Carte | 405x | *(Berapa gram gurita per 1x extra?)* |
| 13 | **Spicy Tori Paitan Chashu Ramen** | Premium Menu | 384x | |
| 14 | **Extra Baby Gurita** | Ala Carte | 371x | *(Berapa gram/pcs per 1x extra?)* |
| 15 | **Strawberry Juice** | Varian Juice | 346x | |
| 16 | **Yaki Sosis** | Paket 5K | 343x | *(Pakai Sosis isi 6 / isi 7 / BP? Berapa pcs + saus?)* |
| 17 | **Dimsum Porsi** | Snack | 342x | *(Isi berapa pcs per porsi + saos/chili oil?)* |
| 18 | **Dimsum Mentai** | Snack | 332x | *(Isi berapa pcs + saus mentai ...g?)* |
| 19 | **Sushi Chicken Cheese Teriyaki** | Sushi | 318x | |
| 20 | **Nigiri Aleyujin** | Nigiri Sushi | 316x | |
| 21 | **Tori Paitan Chashu Ramen** | Premium Menu | 288x | |
| 22 | **Extra Nasi - Donbury** | Ala Carte | 287x | *(Apakah 125 gram Beras seperti Donburi?)* |
| 23 | **Sushi Tempura Crispy Roll** | Sushi | 279x | |
| 24 | **Ramen Brisket** | Premium Menu | 273x | |
| 25 | **Extra Katsu** | Ala Carte | 265x | *(Apakah 40g atau 50g Chicken Katsu?)* |
| 26 | **Salmon Cheese Gunkan** | Sushi | 263x | |
| 27 | **Nigiri Kani Mayo** | Nigiri Sushi | 261x | |
| 28 | **Nigiri Tamago Cheese** | Nigiri Sushi | 254x | |
| 29 | **Kani Cheese Gunkan** | Sushi | 240x | |
| 30 | **Kani Mentai Gunkan** | Sushi | 212x | |

---

### 🔹 Bagian B: Konfirmasi Menu Kategori Lain & Menu Cepat Dipetakan
Selain 30 menu di atas, terdapat beberapa kelompok menu yang sangat mudah dilengkapi jika Bapak bisa mengonfirmasi polanya secara kelompok:

1. **Menu Varian yang Hanya Tukar Lauk/Isian (Tinggal Konfirmasi):**
   - **Hotplate (4 menu, total 429x terjual):** `Nasi Hot Plate Red Hot Daging Sapi` (172x), `Nasi Hot Plate Chicken Katsu Black Papper` (155x), `Mie Hot Plate Red Hot Daging Sapi` (56x), `Kwetiaw Hot Plate Red Hot Daging Sapi` (46x).  
     *Pertanyaan:* Apakah resepnya sama persis dengan varian Chicken Katsu/Sapi lain, hanya menukar `Chicken Katsu (50g)` $\leftrightarrow$ `Daging Sapi (60g)`?
   - **Ramen Ebi Furai (4 menu, total 547x terjual):** `Red Hot Ebi Furai Ramen` (183x), `Ebi Furai Ramen` (172x), `Ebi Furai curry Ramen` (121x), `Ebi Furai Miso Ramen` (71x).  
     *Pertanyaan:* Apakah memakai kuah/mie ramen yang sama dengan Ramen biasa + berapa pcs `Ebi Furai` per mangkok?
2. **Menu Kemasan / Barang Jadi (1 pcs = 1 barang):**
   - **Es Krim Joyday (28 varian, total 1.167x terjual):** Apakah seluruhnya cukup dicatat potong stok **1 pcs per varian** (tanpa bahan campuran lain)?
   - **Risol Dut (10 varian, total 491x terjual — termasuk varian Frozen Pack):** Apakah 1 porsi = **berapa pcs** risol + apakah ada saus/minyak goreng tambahan untuk yang matang (*dine-in*)?
3. **Menu Varian Umum / Ambigu (9 item, total 2.190x terjual):**
   - **FREE ice cream (1.030x):** Rasa apa yang paling sering diberikan (Vanilla, Greentea, atau acak)? Berapa gram/ml per porsi (*scoop*)?
   - **Menu Pelajar (5 item, total 818x):** `Ramen - Pelajar` (428x), `Sweet Ice Tea - Pelajar` (342x), `Takoyaki - Pelajar` (32x), `Siomay Goreng - Pelajar` (12x), `Otak otak Kulit Tahu - Pelajar` (4x).  
     *Pertanyaan:* Apakah takaran porsinya sama persis dengan menu reguler (hanya beda harga promo pelajar), atau porsinya diperkecil?
   - **Cau Katsu (232x), Cau Katsu Mix (90x), Ropang Mix (20x):** Saat kasir memilih menu ini tanpa nama rasa spesifik, topping apa yang paling umum dipakai untuk perhitungan stok?
4. **Menu Kategori Baru Setelah 2018 (Daftar lengkap di Lampiran Bagian 4):**
   - **Udon** (9 menu, 700x) — misal pakai berapa gram mie udon + kuah apa?
   - **Bento & Okosama Lunch** (8 menu, 642x)
   - **Coffee** (14 menu, 775x — Ice Kopi Susu Gula Aren, Americano, Latte, Afogato, dll.)
   - **Shabu & Yakiniku** (4 menu, 312x)
   - **Paket Iftar** (20 paket Ramadhan, 156x — isi menu per paket apa saja?)
   - **Ala Carte / Extra Topping** (35 item, 2.071x — takaran per 1x extra)

---

### 🔹 Bagian C: Klarifikasi Kejanggalan pada File Resep Lama (Tahun 2018)
Saat memeriksa file resep 2018, kami menemukan beberapa angka takaran dan harga yang terlihat kurang wajar. Mohon konfirmasi Bapak:

1. **Pisang Galek pada `Cau Katsu` tertulis `453 gram` per porsi:**
   - Di file `DESSERT`, tercatat `6,800 gram` Pisang Galek untuk 15 porsi (~0,45 kg pisang per 1 porsi). Apakah memang 453 gram per porsi, atau salah ketik dari `680 gram` (~45 gram per porsi)?
2. **Perbedaan Takaran Nasi & Kwetiaw di Menu Hotplate:**
   - Pada `HP Nasi Blackpepper Sapi`, tertulis Beras `50 gram`, sedangkan menu HP Nasi lainnya memakai `125 gram`.
   - Pada `HP Kwetiaw Blackpepper Sapi/Ayam` tertulis Kwetiaw `50 gram`, `HP Kwetiaw Siram Sapi` tertulis `60 gram`, sedangkan varian siram/redhot ayam lainnya `125 gram`.
   - *Pertanyaan:* Mana takaran standar yang sebenarnya dipakai dapur saat ini?
3. **Pencatatan `Tulang Balung (1 gram)` & `Kaldu`:**
   - Di resep Ramen & Hotplate, `Tulang Balung` tertulis `1 gram` (Rp20) dan `Kaldu` tertulis `350 ml`. Di sistem gudang nanti, apakah stok `Tulang Balung` ingin dipantau per pembelian kiloan (misal sekali masak kuah butuh berapa kg tulang untuk berapa porsi)?
4. **Pembaruan Harga Beli Bahan Baku (Opsional namun Disarankan):**
   - Harga bahan di file 2018 (misal Telur Rp1.523/butir, Beras Rp13.000/kg, Daging Sapi Rp105.000/kg) kemungkinan sudah berubah. Jika sistem hanya memantau **jumlah stok (gram/ml/pcs)** tidak masalah, tetapi jika ingin sekalian menghitung **estimasi modal belanja esok hari**, kami membutuhkan daftar harga beli terbaru tahun 2026.

---

### 🔹 Bagian D: Informasi Operasional untuk Fitur Stok Web & Rekomendasi Belanja

Untuk membangun fitur **Indikator Stok Menipis (*Safety Stock*)** dan **Daftar Rekomendasi Belanja Esok Hari**, kami membutuhkan info operasional berikut dari pihak restoran:

1. **Daftar Bahan Utama yang Wajib Dipantau Setiap Malam:**
   - Dari **178 bahan baku** di file 2018, mana saja bahan prioritas yang paling sering dicek staf setiap malam (beserta **batas stok minimal / *safety stock*** masing-masing sebelum harus belanja lagi)?
   - *Catatan:* Di file 2018 ada **17 bahan** yang tercatat di daftar gudang tetapi tidak muncul di resep manapun (seperti `Bobba Kiwi`, `Caramel Topping`, `Garam`, `Gurita`, `Pasta Strawberry`, `Pasta Taro`, `Saos Sachet Cabe/Tomat`, `Smotis`, `Susu Bubuk`, `Gas`, `Hi Cook`, `Cup Gelas`, `Kertas Roti`, `Plastik Klip`, `Sedotan Kecil`, `Tusuk Sate`). Mohon info apakah bahan-bahan ini masih aktif distok di gudang sekarang?
2. **Stok Awal Saat Demo/Uji Coba:**
   - Daftar posisi stok aktual terbaru di gudang (1 hari atau 1 minggu sample) agar kami dapat menguji keakuratan sistem dengan skenario transaksi riil.
3. **Pola Belanja Restoran:**
   - Bahan segar (sayur, daging, ayam, seafood) dibeli setiap hari (H-1 malam untuk besok pagi), atau setiap berapa hari sekali?
   - Bahan kering/kemasan/saus dibeli setiap berapa hari/minggu sekali?
4. **Kebijakan Pencatatan Konsumsi Internal & Produk Mainan:**
   - Di laporan kasir NutaCloud, terdapat **787 transaksi internal** (meja `CREW ALES`, `OWNER`, `BUNDA LULU`, `UMI HANA`, `OPERASIONAL`, `MARKETING`, atau Diskon Crew/Owner). Apakah transaksi ini **tetap dihitung memotong stok dapur**? *(Saran tim: Ya, agar stok fisik gudang tetap sinkron dengan barang yang keluar ke dapur).*
   - Di kasir juga terdapat **29 item non-makanan** kategori `Produk Pinnkishfun` & `Lip Vinyl OMG` (total terjual 259 pcs, misal Slime, Squishy, Jepit Rambut). Apakah item mainan/aksesoris ini **dikeluarkan dari sistem stok bahan makanan**? *(Saran tim: Ya, fokus sistem hanya pada stok bahan makanan & minuman).*

---

## 3. Lampiran: Daftar Menu Baru Lainnya per Kategori (Di Luar Top 30)

Berikut ringkasan kategori menu lain yang belum ada resepnya di data 2018 (diurutkan dari yang paling sering terjual di masing-masing kategori):

- **Sushi & Nigiri Lainnya:** `Sosis BBQ Gunkan` (181x), `Sushi Tuna Pedas` (167x), `Sushi Karaage Roll` (94x), `Sushi Unagi` (86x), `Sushi Green Tuna` (72x), `Beef Mentai Bomb` (69x), `Tuna Mayo Gunkan` (61x), `Chicken Cheese Gunkan` (58x), `Sushi Gede Pangrango Vulcano` (43x), `Beef Mayo Bomb` (39x), `Sushi AIKO`, `Sushi AZUMI`, `Sushi Crabstik Roll`, `Sushi Uramaki Tamago Roll`.
- **Ramen Lainnya:** `Hiyashi Cuka Goma` (100x), `Abura Ramen Chicken Katsu` (64x), `Abura Ramen Beef` (60x), `Abura Original` (51x).
- **Udon (700x):** `Redhot Beef Udon` (131x), `Beef Curry Udon` (109x), `Niku Udon` (100x), `Chicken Katsu Udon` (92x), `Yaki Udon Beef` (91x), `Yaki Udon Seafood` (51x), `Redhot Chicken Katsu Udon` (48x), `Chicken Katsu Curry Udon` (45x), `Shiroichi Udon` (33x).
- **Bento & Anak (642x):** `Beef Teriyaki Bento` (175x), `Beef Yakiniku Bento` (136x), `Chicken Yakiniku Bento` (117x), `Chicken Teriyaki Bento` (84x), `Ramen Anak` (54x), `Okosama Lunch A/B` (55x), `Bento Mini` (21x).
- **Coffee (775x):** `Ice Kopi Susu Gula Aren` (188x), `Americano Ice/Hot` (137x), `Coffee Latte Ice/Hot` (117x), `Hazelnut Latte Ice/Hot` (90x), `Cappucino Ice/Hot` (84x), `Afogato Coffe Ice` (78x), `Caramel Latte Ice/Hot` (57x), `Double Espresso` (24x).
- **Minuman Lainnya:** `Teh Tawar Panas/Ice` (224x), `Teh Manis Panas` (80x), `Salted Caramel Creamy` (59x), `Yuzu & Blewah Shake` (35x), `Winter Milk Tea Shake` (18x), `Pucuk Watermelon` (14x), serta seri `Minuman 1 Liter` (`Lemonade`, `Lemon Mint Tea`, `Orange`, `Strawberry Mint Tea` — total 76x).
- **Tako / Yakitori Lainnya:** `Yakitori Enoki Beef` (87x), `Yakitori Tori Ayam` (46x), `Yakitori Salmon` (15x), `Yakitori Ayam` (12x).
- **Shabu & Yakiniku (312x):** `Yakiniku` (103x), `Shabu Shabu Kuah Tomyam` (83x), `Shabu-Shabu Kuah Original` (83x), `Shabu Shabu Mix` (43x).
- **Ala Carte / Extra Topping Utama:** `Extra Mie - Ramen` (207x), `Extra Tempura Ebi - Ramen` (84x), `Extra Jamur Enoki` (78x), `Extra Beef - Ramen/HP` (60x), `Extra Telur Dadar/Ceplok` (43x), `Extra Brastwurst` (38x), `Extra Telur 1/2 butir` (31x), dll.
- **Paket Iftar (Ramadhan):** `IFTAR 2A/2B/4A/4B/6A/6B/8A` (20 varian paket, total 156x terjual).

---

## 4. Draft Pesan WhatsApp Siap Kirim ke Pak Ares

> *Selamat malam Bapak Ares, perkenalkan kembali kami tim Capstone Asah (Dicoding) kelompok A26-CS218 yang mengerjakan sistem pencatatan stok Ale's Place Cipoho.*
> 
> *Saat ini kami sudah selesai membersihkan 13 bulan data transaksi NutaCloud (Okt 2025 – Okt 2026) dan menggabungkannya dengan data resep 2018 yang Bapak berikan. Namun kami menemukan bahwa resep tahun 2018 baru mencakup **59% porsi penjualan saat ini**, karena ada banyak menu baru di tahun 2025–2026 (seperti Sushi, Ramen Tomyam, Juice, Udon, Bento, dan Coffee) yang belum ada data takarannya.*
> 
> *Supaya sistem pemotongan stok otomatis dan rekomendasi belanja harian yang kami buat bisa akurat sesuai kondisi dapur sekarang, kami izin mengirimkan dokumen singkat berisi daftar menu prioritas & beberapa pertanyaan takaran untuk Bapak/tim dapur konfirmasi.*
> 
> *Kira-kira kapan kami bisa berdiskusi sebentar (atau Bapak mengisi tabel prioritas di dokumen tersebut)? Terima kasih banyak atas bantuannya, Pak 🙏*
