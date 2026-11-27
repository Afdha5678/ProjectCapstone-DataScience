"""
Pipeline Pembersihan & Normalisasi Data Penjualan (13 Bulan: Okt 2025 - Okt 2026)
Restoran Ale's Place.

Input  :
  - Data Penjualan/*.csv (13 file laporan kasir mentah)
  - tugas_mingguan/minggu-1/output/data_bahan_makanan/dim_menu.csv
  - tugas_mingguan/minggu-1/output/data_bahan_makanan/inventory_resto.db

Output di tugas_mingguan/minggu-1/output/data_penjualan/ :
  - fact_transaksi.csv              (9.295 transaksi unik bersih di level struk)
  - fact_penjualan_item.csv         (baris penjualan produk bersih + ekstraksi diskon + link id_menu_resep)
  - fact_penyesuaian_transaksi.csv  (Pajak Daerah, Pembulatan, Diskon Nota/Voucher, Pengemasan, Alat Makan TKW)
  - map_menu_kasir.csv              (kamus mapping nama item kasir <-> dim_menu resep)
  - ales_place_dwh.db               (SQLite Data Warehouse terpadu: BOM + Penjualan + Mapping + Views)
"""

from __future__ import annotations

import csv
import glob
import os
import re
import shutil
import sqlite3
from pathlib import Path
from typing import Optional

import pandas as pd

MINGGU_1_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = Path(__file__).resolve().parents[3]
SALES_DIR = WORKSPACE_DIR / "Data Penjualan"
BOM_DIR = MINGGU_1_DIR / "output" / "data_bahan_makanan"
OUT_DIR = MINGGU_1_DIR / "output" / "data_penjualan"

ID_MONTHS = {
    "Januari": "01",
    "Februari": "02",
    "Maret": "03",
    "April": "04",
    "Mei": "05",
    "Juni": "06",
    "Juli": "07",
    "Agustus": "08",
    "September": "09",
    "Oktober": "10",
    "November": "11",
    "Desember": "12",
}

CHANNEL_MAP: dict[str, tuple[str, str]] = {
    "Dine In": ("Dine-In", "Ale's Place"),
    "DINE IN": ("Dine-In", "Ale's Place"),
    "Makan di tempat": ("Dine-In", "Ale's Place"),
    "Takeaway": ("Takeaway", "Ale's Place"),
    "Takeaway Walk in": ("Takeaway", "Ale's Place"),
    "Takeaway Delivery": ("Takeaway", "Ale's Place"),
    "Bungkus": ("Takeaway", "Ale's Place"),
    "TKW": ("Takeaway", "Ale's Place"),
    "Go Food Ale’s Place": ("GoFood", "Ale's Place"),
    "Go Food Risoldut": ("GoFood", "Risoldut"),
    "Grab Food Ale’s Place": ("GrabFood", "Ale's Place"),
    "Grab Food Risoldut": ("GrabFood", "Risoldut"),
    "Shopeefood": ("ShopeeFood", "Ale's Place"),
    "Shopeefood Ale's Place": ("ShopeeFood", "Ale's Place"),
    "Shopee Food Risoldut": ("ShopeeFood", "Risoldut"),
    "Event": ("Event", "Ale's Place"),
}

PELAYAN_ALIASES: dict[str, str] = {
    "syaila": "Syaila",
    "SAUQI": "Sauqi",
    "Putri melati": "Putri Melati Yuniar",
    "Daud M Asidiki": "Daud Maulana Assidiki",
}

INTERNAL_TABLE_KEYWORDS = (
    "CREW ALES",
    "OWNER",
    "BUNDA LULU",
    "UMI HANA",
    "OPERASIONAL",
    "MARKETING",
)

# Pemetaan nama item kasir (lowercase) -> nama_menu exact di dim_menu.csv
CASHIER_TO_RECIPE_ALIAS: dict[str, str] = {
    # Ramen
    "soyu ramen original": "Ramen Soyu",
    "chicken katsu ramen": "Ramen Chicken Katsu",
    "gyuniku ramen": "Ramen Gyuniku",
    "brastwurst ramen": "Ramen Brastwust",
    "redhot chicken katsu ramen": "Ramen Redhot Katsu",
    "redhot beef ramen": "Ramen Redhot Beef",
    "redhot brastwurst ramen": "Ramen Redhot Brastwust",
    "gyumiso ramen": "Ramen Gyumiso Beef",
    "chicken katsu miso ramen": "Ramen Miso Chicken Katsu",
    "beef curry ramen": "Ramen Curry Beef",
    "chicken katsu curry ramen": "Ramen Curry Chicken Katsu",
    "shiro ichi ramen": "Ramen Shiroichi",
    # Hotplate
    "kwetiaw hot plate chiken katsu black pepper": "HP Kwetiaw Blackpepper Ayam",
    "kwetiaw hot plate daging sapi black pepper": "HP Kwetiaw Blackpepper Sapi",
    "kwetiaw hot plate red hot chicken katsu": "HP Kwetiaw Redhot Ayam",
    "kwetiaw hot plate siram chicken katsu": "HP Kwetiaw Siram Chicken Katsu",
    "kwetiaw hot plate siram daging sapi": "HP Kwetiaw Siram Sapi",
    "mie hot plate chiken katsu black papper": "HP Mie Blackpepper Ayam",
    "mie hot plate daging sapi black papper": "HP Mie Blackpepper Sapi",
    "mie hot plate red hot chiken katsu": "HP Mie Redhot Ayam",
    "mie hot plate siram chiken katsu": "HP Mie Siram Katsu",
    "mie hot plate siram daging sapi": "HP Mie Siram Sapi",
    "nasi hot plate daging sapi black papper": "HP Nasi Blackpepper Sapi",
    "nasi hot plate red hot chicken katsu": "HP Nasi Redhot Ayam",
    "nasi hot plate siram chicken katsu": "HP Nasi Siram Chicken Katsu",
    "nasi hot plate siram daging sapi": "HP Nasi Siram Sapi",
    # Donburi & Omurice
    "curry katsudon": "Donburi Curry Katsu",
    "gyuniku don": "Donburi Gyuniku",
    "mozarella katsudon": "Donburi Mozaru Katsu",
    "omurice original": "Omurice",
    "omurice sosis brastwurst": "Omurice Brastwust",
    # Minuman & Mixologist
    "le mineral / air mineral": "Air Mineral",
    "blio air mineral": "Air Mineral",
    "air mineral hangat": "Air Mineral",
    "ocha free refill - ice": "Ocha Refill",
    "ocha free refill - hot": "Ocha Refill",
    "sweet ice tea": "Ice Tea",
    "lychee kult": "Leci Kult",
    "mango kult": "Manggo Kult",
    "lychee mojito": "Mojito Leci",
    "mango mojito": "Mojito Mango",
    "strawberry mojito": "Mojito Strawberry",
    "lychee smoothies": "Leci Smoothies",
    "mango smoothies": "Manggo Smoothies",
    "lychee mint tea": "Leci Mint Tea",
    "mango mint tea": "Manggo Mint Tea",
    "lemon mint tea": "Lemon Mint",
    "tomato juice": "Jus Tomat",
    "greentea blended": "Green Tea Blended",
    "vanila oreo": "Oreo Blended",
    "hot choco latte": "ChocoLatte",
    "hot greentea latte": "GreenTea Latte",
    # Dessert & Ropang & Silky Pudding
    "pingku greentea": "Pingku Green Tea",
    "pingku mango": "Pingku Manggo",
    "ropang coklat": "Ropang Cokelat",
    "silky puding coklat": "Silky Pudding Coklat",
    "silky puding greentea": "Silky Pudding Greentea",
    "silky puding mangga": "Silky Pudding Manggo",
    "silky puding taro": "Silky Pudding Taro",
    "extra silky puding chocolate": "Silky Pudding Coklat",
    "extra silky puding green tea": "Silky Pudding Greentea",
    "extra silky puding mango": "Silky Pudding Manggo",
    "extra silky puding taro": "Silky Pudding Taro",
    "scoope of ic greentea": "Green Tea Ice Cream",
    "scoope of ic vanilla": "Vanilla Ice Cream",
    # Snack, Tako, Sushi
    "beef okonomiyaki": "Okonomiyaki Beef",
    "chicken katsu okonomiyaki": "Okonomiyaki Chicken",
    "mozarella okonomiyaki": "Okonomiyaki Mozarella",
    "okonomiyaki": "Okonomiyaki Original",
    "sosis bakar original": "Sosis Ori",
    "otak otak kulit tahu": "Otak-Otak",
    "sushi hanamera - cooking class >15": "Sushi Hanamera",
    "sushi kanimaki - cooking class >15 org": "Sushi Kanimaki",
}

AMBIGUOUS_ITEMS = {
    "cau katsu",
    "cau katsu mix",
    "ropang mix",
    "free ice cream",
    "ramen - pelajar",
    "takoyaki - pelajar",
    "sweet ice tea - pelajar",
    "siomay goreng - pelajar",
    "otak otak kulit tahu - pelajar",
}


def sort_sales_files(paths: list[str]) -> list[Path]:
    """Urutkan file laporan penjualan berdasarkan angka awalan (1..13)."""
    def prefix_num(p: str) -> int:
        m = re.match(r"^(\d+)", Path(p).name)
        return int(m.group(1)) if m else 999

    return [Path(p) for p in sorted(paths, key=prefix_num)]


def parse_indonesian_datetime(val: object) -> Optional[str]:
    """Konversi string tanggal Indonesia ('01 Oktober 2025, 11:16:28') menjadi 'YYYY-MM-DD HH:MM:SS'."""
    if pd.isna(val):
        return None
    s = str(val).strip()
    if not s:
        return None
    m = re.match(r"^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4}),?\s+(\d{2}:\d{2}:\d{2})$", s)
    if not m:
        return None
    day, mon_name, year, time_part = m.groups()
    mon_num = ID_MONTHS.get(mon_name.capitalize())
    if not mon_num:
        return None
    return f"{year}-{mon_num}-{day.zfill(2)} {time_part}"


def parse_user_timestamp(val: object) -> tuple[Optional[str], Optional[str]]:
    """Pecah kolom 'Dibuat Oleh' / 'Diubah Oleh' ('Kasir 1\\n 01 Oktober 2025, 10:28:31') -> (user, datetime)."""
    if pd.isna(val):
        return None, None
    s = str(val).strip()
    if not s:
        return None, None
    if "\n" in s:
        user_part, dt_part = s.split("\n", 1)
        return user_part.strip(), parse_indonesian_datetime(dt_part.strip())
    return s, None


def parse_pelanggan(val: object) -> tuple[Optional[str], Optional[str], Optional[str], Optional[int]]:
    """
    Pecah kolom Pelanggan ('Desti/Lantai 2 Meja ATAS 4\\nPAX = 4') menjadi:
    (nama_pelanggan, area_lantai, nomor_meja, pax).
    """
    if pd.isna(val):
        return None, None, None, None
    s = str(val).strip()
    if not s or s == "-":
        return None, None, None, None

    pax: Optional[int] = None
    pax_match = re.search(r"PAX\s*=\s*(\d+)", s, flags=re.IGNORECASE)
    if pax_match:
        pax = int(pax_match.group(1))
        s = re.sub(r"\n?PAX\s*=\s*\d+", "", s, flags=re.IGNORECASE).strip()

    nama_pelanggan: Optional[str] = None
    area_lantai: Optional[str] = None
    nomor_meja: Optional[str] = None

    if "/" in s:
        before_slash, after_slash = s.rsplit("/", 1)
        after_clean = after_slash.strip()
        if after_clean.startswith(("Lantai ", "Teras ")) or "Meja" in after_clean:
            nama_raw = before_slash.strip()
            nama_pelanggan = None if nama_raw in ("", "-") else nama_raw
            if "Meja" in after_clean:
                idx_meja = after_clean.index("Meja")
                area_lantai = after_clean[:idx_meja].strip() or None
                nomor_meja = after_clean[idx_meja:].strip() or None
            else:
                area_lantai = after_clean
        else:
            nama_pelanggan = None if s in ("", "-") else s
    else:
        nama_pelanggan = None if s in ("", "-") else s

    return nama_pelanggan, area_lantai, nomor_meja, pax


def clean_text_field(val: object) -> Optional[str]:
    if pd.isna(val):
        return None
    s = re.sub(r"\s+", " ", str(val)).strip()
    return s if s else None


def classify_adjustment_row(item_raw: str, kategori: Optional[str]) -> Optional[str]:
    """Tentukan jenis penyesuaian jika baris bukan produk utama, else None."""
    it = item_raw.strip()
    if it == "Pajak Daerah":
        return "PAJAK_DAERAH"
    if it == "Pembulatan":
        return "PEMBULATAN"
    if it.startswith("Diskon Final"):
        return "DISKON_NOTA"
    if it.startswith("Voucher "):
        return "VOUCHER_NOTA"
    if kategori == "Perlengkapan" or it == "Biaya Pengemasan":
        return "BIAYA_PENGEMASAN"
    if kategori == "Alat Makan Tkw" or it == "Thinwal 450":
        return "ALAT_MAKAN_TKW"
    return None


def parse_item_and_discount(item_raw: str) -> tuple[str, int, Optional[str]]:
    """Pisahkan nama menu bersih dan label diskon ('Risol Dut\\n Diskon 100%' -> ('Risol Dut', 1, 'Diskon 100%'))."""
    if "\n" in item_raw:
        name_part, disc_part = item_raw.split("\n", 1)
        clean_name = re.sub(r"\s+", " ", name_part).strip()
        disc_label = re.sub(r"\s+", " ", disc_part).strip()
        return clean_name, 1, disc_label
    return re.sub(r"\s+", " ", item_raw).strip(), 0, None


def load_dim_menu() -> dict[str, tuple[int, str]]:
    """Load id_menu dan nama_menu dari dim_menu.csv (khusus sellable menu)."""
    lookup: dict[str, tuple[int, str]] = {}
    with open(BOM_DIR / "dim_menu.csv", "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["is_sellable"] == "1":
                lookup[r["nama_menu"].lower()] = (int(r["id_menu"]), r["nama_menu"])
    return lookup


def resolve_recipe_mapping(
    item_name: str, kategori: Optional[str], menu_lookup: dict[str, tuple[int, str]]
) -> tuple[Optional[int], Optional[str], str]:
    """Petakan item kasir ke dim_menu.id_menu beserta status pencocokan."""
    low = item_name.lower()
    if low in menu_lookup:
        mid, mname = menu_lookup[low]
        return mid, mname, "MAPPED_EXACT"

    if low in CASHIER_TO_RECIPE_ALIAS:
        target = CASHIER_TO_RECIPE_ALIAS[low].lower()
        if target in menu_lookup:
            mid, mname = menu_lookup[target]
            return mid, mname, "MAPPED_ALIAS"

    if low in AMBIGUOUS_ITEMS:
        return None, None, "AMBIGUOUS_VARIANT"

    if kategori == "Produk Pinnkishfun" or item_name == "Lip Vinyl OMG":
        return None, None, "UNMAPPED_NON_FNB_MERCH"

    return None, None, "UNMAPPED_FNB"


def process_sales_files() -> None:
    menu_lookup = load_dim_menu()
    files = sort_sales_files(glob.glob(str(SALES_DIR / "*.csv")))

    tx_records: dict[str, dict] = {}
    item_rows: list[dict] = []
    adj_rows: list[dict] = []

    line_pk = 1
    adj_pk = 1

    for fpath in files:
        df = pd.read_csv(fpath)
        df = df[~df["Nomor"].astype(str).str.contains("Grand Total", na=False)].copy()

        # Forward-fill header transaksi per file
        header_cols = [
            "Nomor",
            "Tanggal",
            "Pelayan",
            "Tipe Penjualan",
            "Metode Pembayaran",
            "Masuk ke Rekening",
            "Pelanggan",
            "Total",
            "Dibuat Oleh",
            "Diubah Oleh",
        ]
        for col in header_cols:
            df[col] = df[col].ffill()

        for _, row in df.iterrows():
            nomor_raw = str(row["Nomor"]).strip()
            if "\n" in nomor_raw:
                tx_id, catatan_nomor = [x.strip() for x in nomor_raw.split("\n", 1)]
                catatan_nomor = catatan_nomor or None
            else:
                tx_id, catatan_nomor = nomor_raw, None

            # Inisialisasi header transaksi jika baru ditemui
            if tx_id not in tx_records:
                waktu_tx = parse_indonesian_datetime(row["Tanggal"])
                pelayan_raw = clean_text_field(row["Pelayan"])
                pelayan = PELAYAN_ALIASES.get(pelayan_raw, pelayan_raw) if pelayan_raw else None

                tipe_raw = clean_text_field(row["Tipe Penjualan"]) or "Lainnya"
                channel, brand = CHANNEL_MAP.get(tipe_raw, (tipe_raw, "Ale's Place"))

                metode = clean_text_field(row["Metode Pembayaran"]) or ""
                is_split = 1 if metode.startswith("Campuran") else 0
                rekening = clean_text_field(row["Masuk ke Rekening"])

                nama_pel, lantai, meja, pax = parse_pelanggan(row["Pelanggan"])
                dibuat_oleh, waktu_dibuat = parse_user_timestamp(row["Dibuat Oleh"])
                diubah_oleh, waktu_diubah = parse_user_timestamp(row["Diubah Oleh"])

                grand_total = float(pd.to_numeric(row["Total"], errors="coerce") or 0.0)
                is_internal = 1 if (meja and any(k in meja.upper() for k in INTERNAL_TABLE_KEYWORDS)) else 0

                tx_records[tx_id] = {
                    "id_transaksi": tx_id,
                    "catatan_nomor": catatan_nomor,
                    "waktu_transaksi": waktu_tx,
                    "tanggal": waktu_tx[:10] if waktu_tx else None,
                    "jam": int(waktu_tx[11:13]) if waktu_tx else None,
                    "pelayan": pelayan,
                    "tipe_penjualan_raw": tipe_raw,
                    "channel_penjualan": channel,
                    "brand_store": brand,
                    "metode_pembayaran": metode,
                    "is_split_payment": is_split,
                    "masuk_ke_rekening": rekening,
                    "nama_pelanggan": nama_pel,
                    "area_lantai": lantai,
                    "nomor_meja": meja,
                    "pax": pax,
                    "is_internal_order": is_internal,
                    "subtotal_produk": 0.0,
                    "total_penyesuaian_diskon_nota": 0.0,
                    "pajak_daerah": 0.0,
                    "pembulatan": 0.0,
                    "biaya_pengemasan": 0.0,
                    "grand_total": round(grand_total, 2),
                    "dibuat_oleh": dibuat_oleh,
                    "waktu_dibuat": waktu_dibuat,
                    "diubah_oleh": diubah_oleh,
                    "waktu_diubah": waktu_diubah,
                    "source_file": fpath.name,
                }

            item_raw = str(row["Item"]) if pd.notna(row["Item"]) else ""
            kategori = clean_text_field(row["Kategori"])
            qty_val = pd.to_numeric(row["Qty"], errors="coerce")
            harga_val = pd.to_numeric(row["Harga Satuan"], errors="coerce")
            sub_val = float(pd.to_numeric(row["Sub Total"], errors="coerce") or 0.0)

            adj_type = classify_adjustment_row(item_raw, kategori)
            tx_rec = tx_records[tx_id]

            if adj_type is not None:
                clean_adj_name = re.sub(r"\s+", " ", item_raw).strip()
                if adj_type in ("DISKON_NOTA", "VOUCHER_NOTA") and any(
                    k in clean_adj_name.upper() for k in ("CREW", "OWNER")
                ):
                    tx_rec["is_internal_order"] = 1

                if adj_type == "PAJAK_DAERAH":
                    tx_rec["pajak_daerah"] += sub_val
                elif adj_type == "PEMBULATAN":
                    tx_rec["pembulatan"] += sub_val
                elif adj_type in ("DISKON_NOTA", "VOUCHER_NOTA"):
                    tx_rec["total_penyesuaian_diskon_nota"] += sub_val
                elif adj_type in ("BIAYA_PENGEMASAN", "ALAT_MAKAN_TKW"):
                    tx_rec["biaya_pengemasan"] += sub_val

                adj_rows.append(
                    {
                        "id_penyesuaian": adj_pk,
                        "id_transaksi": tx_id,
                        "jenis_penyesuaian": adj_type,
                        "nama_item": clean_adj_name,
                        "qty": None if pd.isna(qty_val) else float(qty_val),
                        "harga_satuan": None if pd.isna(harga_val) else float(harga_val),
                        "subtotal": round(sub_val, 2),
                    }
                )
                adj_pk += 1
            else:
                clean_name, has_disc_label, disc_label = parse_item_and_discount(item_raw)
                qty_num = 0.0 if pd.isna(qty_val) else float(qty_val)
                harga_num = 0.0 if pd.isna(harga_val) else float(harga_val)

                # Hitung selisih diskon di level item
                gross_line = qty_num * harga_num
                nominal_disc = max(0.0, round(gross_line - sub_val, 2)) if qty_num > 0 else 0.0
                is_diskon_item = 1 if (has_disc_label == 1 or nominal_disc > 0.0) else 0
                is_void = 1 if qty_num <= 0 else 0

                if kategori is None:
                    if clean_name == "Lip Vinyl OMG":
                        kategori = "Produk Pinnkishfun"
                    elif "Level " in clean_name:
                        kategori = "Ramen"

                id_menu_resep, nama_menu_resep, match_status = resolve_recipe_mapping(
                    clean_name, kategori, menu_lookup
                )

                tx_rec["subtotal_produk"] += sub_val

                item_rows.append(
                    {
                        "id_line": line_pk,
                        "id_transaksi": tx_id,
                        "waktu_transaksi": tx_rec["waktu_transaksi"],
                        "tanggal": tx_rec["tanggal"],
                        "nama_item_bersih": clean_name,
                        "id_menu_resep": id_menu_resep,
                        "kategori_kasir": kategori,
                        "varian": clean_text_field(row["Varian"]),
                        "pilihan_ekstra": clean_text_field(row["Pilihan Ekstra"]),
                        "notes": clean_text_field(row["Notes"]),
                        "qty": qty_num,
                        "harga_satuan": harga_num,
                        "is_diskon_item": is_diskon_item,
                        "label_diskon_item": disc_label,
                        "nominal_diskon_item": nominal_disc,
                        "subtotal_net": round(sub_val, 2),
                        "is_void_adjustment": is_void,
                    }
                )
                line_pk += 1

    # Bulatkan agregasi finansial di fact_transaksi
    df_tx = pd.DataFrame(tx_records.values())
    for col in (
        "subtotal_produk",
        "total_penyesuaian_diskon_nota",
        "pajak_daerah",
        "pembulatan",
        "biaya_pengemasan",
        "grand_total",
    ):
        df_tx[col] = df_tx[col].round(2)

    df_items = pd.DataFrame(item_rows)
    df_items["id_menu_resep"] = df_items["id_menu_resep"].astype("Int64")

    df_adj = pd.DataFrame(adj_rows)

    # Buat tabel bridge map_menu_kasir
    map_agg = (
        df_items.groupby(["nama_item_bersih", "kategori_kasir"], dropna=False)
        .agg(
            total_qty_terjual=("qty", "sum"),
            total_omzet_net=("subtotal_net", "sum"),
            id_menu_resep=("id_menu_resep", "first"),
        )
        .reset_index()
    )
    map_records = []
    for _, r in map_agg.iterrows():
        mid, mname, status = resolve_recipe_mapping(
            r["nama_item_bersih"], r["kategori_kasir"], menu_lookup
        )
        map_records.append(
            {
                "nama_item_kasir": r["nama_item_bersih"],
                "kategori_kasir": r["kategori_kasir"],
                "total_qty_terjual": round(float(r["total_qty_terjual"]), 2),
                "total_omzet_net": round(float(r["total_omzet_net"]), 2),
                "id_menu_resep": mid,
                "nama_menu_resep": mname,
                "match_status": status,
            }
        )
    df_map = pd.DataFrame(map_records).sort_values("total_qty_terjual", ascending=False)
    df_map["id_menu_resep"] = df_map["id_menu_resep"].astype("Int64")

    # Ekspor CSV
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df_tx.to_csv(OUT_DIR / "fact_transaksi.csv", index=False, encoding="utf-8")
    df_items.to_csv(OUT_DIR / "fact_penjualan_item.csv", index=False, encoding="utf-8")
    df_adj.to_csv(OUT_DIR / "fact_penyesuaian_transaksi.csv", index=False, encoding="utf-8")
    df_map.to_csv(OUT_DIR / "map_menu_kasir.csv", index=False, encoding="utf-8")

    # Bangun Data Warehouse SQLite Terpadu (ales_place_dwh.db)
    build_unified_dwh(df_tx, df_items, df_adj, df_map)

    print("=== NORMALISASI DATA PENJUALAN SELESAI ===")
    print(f"fact_transaksi.csv             : {len(df_tx):,} transaksi unik")
    print(f"fact_penjualan_item.csv        : {len(df_items):,} baris item terjual")
    print(f"fact_penyesuaian_transaksi.csv : {len(df_adj):,} baris penyesuaian")
    print(f"map_menu_kasir.csv             : {len(df_map):,} item unik")

    mapped_qty = df_map[df_map["match_status"].isin(["MAPPED_EXACT", "MAPPED_ALIAS"])]["total_qty_terjual"].sum()
    total_qty = df_map["total_qty_terjual"].sum()
    print(f"Cakupan mapping ke resep BOM   : {mapped_qty:,.0f} / {total_qty:,.0f} porsi ({mapped_qty/total_qty*100:.1f}%)")


def build_unified_dwh(
    df_tx: pd.DataFrame,
    df_items: pd.DataFrame,
    df_adj: pd.DataFrame,
    df_map: pd.DataFrame,
) -> None:
    """Salin inventory_resto.db menjadi ales_place_dwh.db dan tambahkan tabel penjualan + views."""
    src_db = BOM_DIR / "inventory_resto.db"
    dwh_db = OUT_DIR / "ales_place_dwh.db"
    shutil.copyfile(src_db, dwh_db)

    conn = sqlite3.connect(dwh_db)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS fact_transaksi (
                id_transaksi VARCHAR(50) PRIMARY KEY,
                catatan_nomor TEXT,
                waktu_transaksi DATETIME NOT NULL,
                tanggal DATE NOT NULL,
                jam INTEGER NOT NULL,
                pelayan VARCHAR(100),
                tipe_penjualan_raw VARCHAR(100),
                channel_penjualan VARCHAR(50) NOT NULL,
                brand_store VARCHAR(50) NOT NULL,
                metode_pembayaran VARCHAR(100),
                is_split_payment INTEGER NOT NULL DEFAULT 0,
                masuk_ke_rekening VARCHAR(150),
                nama_pelanggan VARCHAR(150),
                area_lantai VARCHAR(50),
                nomor_meja VARCHAR(100),
                pax INTEGER,
                is_internal_order INTEGER NOT NULL DEFAULT 0,
                subtotal_produk DECIMAL(14, 2) NOT NULL DEFAULT 0,
                total_penyesuaian_diskon_nota DECIMAL(14, 2) NOT NULL DEFAULT 0,
                pajak_daerah DECIMAL(14, 2) NOT NULL DEFAULT 0,
                pembulatan DECIMAL(14, 2) NOT NULL DEFAULT 0,
                biaya_pengemasan DECIMAL(14, 2) NOT NULL DEFAULT 0,
                grand_total DECIMAL(14, 2) NOT NULL DEFAULT 0,
                dibuat_oleh VARCHAR(100),
                waktu_dibuat DATETIME,
                diubah_oleh VARCHAR(100),
                waktu_diubah DATETIME,
                source_file VARCHAR(255)
            );

            CREATE TABLE IF NOT EXISTS fact_penjualan_item (
                id_line INTEGER PRIMARY KEY,
                id_transaksi VARCHAR(50) NOT NULL,
                waktu_transaksi DATETIME NOT NULL,
                tanggal DATE NOT NULL,
                nama_item_bersih VARCHAR(200) NOT NULL,
                id_menu_resep INTEGER,
                kategori_kasir VARCHAR(100),
                varian VARCHAR(150),
                pilihan_ekstra VARCHAR(200),
                notes TEXT,
                qty DECIMAL(12, 4) NOT NULL,
                harga_satuan DECIMAL(14, 2) NOT NULL,
                is_diskon_item INTEGER NOT NULL DEFAULT 0,
                label_diskon_item VARCHAR(100),
                nominal_diskon_item DECIMAL(14, 2) NOT NULL DEFAULT 0,
                subtotal_net DECIMAL(14, 2) NOT NULL,
                is_void_adjustment INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (id_transaksi) REFERENCES fact_transaksi(id_transaksi),
                FOREIGN KEY (id_menu_resep) REFERENCES dim_menu(id_menu)
            );

            CREATE TABLE IF NOT EXISTS fact_penyesuaian_transaksi (
                id_penyesuaian INTEGER PRIMARY KEY,
                id_transaksi VARCHAR(50) NOT NULL,
                jenis_penyesuaian VARCHAR(50) NOT NULL,
                nama_item VARCHAR(200) NOT NULL,
                qty DECIMAL(12, 4),
                harga_satuan DECIMAL(14, 2),
                subtotal DECIMAL(14, 2) NOT NULL,
                FOREIGN KEY (id_transaksi) REFERENCES fact_transaksi(id_transaksi)
            );

            CREATE TABLE IF NOT EXISTS map_menu_kasir (
                nama_item_kasir VARCHAR(200) NOT NULL,
                kategori_kasir VARCHAR(100),
                total_qty_terjual DECIMAL(14, 2),
                total_omzet_net DECIMAL(14, 2),
                id_menu_resep INTEGER,
                nama_menu_resep VARCHAR(150),
                match_status VARCHAR(50) NOT NULL,
                PRIMARY KEY (nama_item_kasir, kategori_kasir),
                FOREIGN KEY (id_menu_resep) REFERENCES dim_menu(id_menu)
            );
            """
        )

        df_tx.to_sql("fact_transaksi", conn, if_exists="append", index=False)
        df_items.to_sql("fact_penjualan_item", conn, if_exists="append", index=False)
        df_adj.to_sql("fact_penyesuaian_transaksi", conn, if_exists="append", index=False)
        df_map.to_sql("map_menu_kasir", conn, if_exists="append", index=False)

        conn.executescript(
            """
            CREATE INDEX IF NOT EXISTS idx_tx_tanggal ON fact_transaksi(tanggal);
            CREATE INDEX IF NOT EXISTS idx_item_tanggal ON fact_penjualan_item(tanggal);
            CREATE INDEX IF NOT EXISTS idx_item_menu ON fact_penjualan_item(id_menu_resep);

            CREATE VIEW IF NOT EXISTS v_pemakaian_bahan_harian AS
            SELECT
                p.tanggal,
                b.id_bahan,
                b.nama_bahan,
                b.satuan_dasar,
                ROUND(SUM(p.qty * r.jumlah_pemakaian), 4) AS total_pemakaian,
                ROUND(SUM(p.qty * r.estimasi_biaya_bahan), 2) AS estimasi_hpp
            FROM fact_penjualan_item p
            JOIN fact_resep_bom r ON p.id_menu_resep = r.id_menu
            JOIN dim_bahan_baku b ON r.id_bahan = b.id_bahan
            GROUP BY p.tanggal, b.id_bahan, b.nama_bahan, b.satuan_dasar;
            """
        )
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    process_sales_files()
