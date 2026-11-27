"""
Pipeline Normalisasi Data Bahan Makanan & Resep (Bill of Materials / BOM)
Restoran Ale's Place - Untuk Sistem Manajemen Stok Terintegrasi Kasir.

Input  : 9 file CSV mentah di folder `Data Bahan Makanan/`
Output :
  - tugas_mingguan/minggu-1/output/data_bahan_makanan/dim_kategori_menu.csv
  - tugas_mingguan/minggu-1/output/data_bahan_makanan/dim_bahan_baku.csv
  - tugas_mingguan/minggu-1/output/data_bahan_makanan/dim_menu.csv
  - tugas_mingguan/minggu-1/output/data_bahan_makanan/fact_resep_bom.csv
  - tugas_mingguan/minggu-1/output/data_bahan_makanan/inventory_resto.db (SQLite + Views + FK)
  - tugas_mingguan/minggu-1/output/data_bahan_makanan/schema_and_seed.sql
"""

from __future__ import annotations

import csv
import glob
import os
import re
import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

MINGGU_1_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = Path(__file__).resolve().parents[3]
RAW_DIR = WORKSPACE_DIR / "Data Bahan Makanan"
OUT_DIR = MINGGU_1_DIR / "output" / "data_bahan_makanan"

# Pemetaan nama bahan baku mentah (UPPERCASE) -> nama kanonikal standar
INGREDIENT_ALIASES: dict[str, str] = {
    "AIR": "AIR GALON",
    "AIR PANAS/ES": "AIR GALON",
    "GALON": "AIR GALON",
    "BACKING POWDER": "BAKING POWDER",
    "BEEF BURGER": "DAGING BURGER",
    "BOMBAY": "BAWANG BOMBAY",
    "BUBLE": "BUBBLE TAPIOCA",
    "CUKA 1/4 SDT": "CUKA",
    "ES": "ES BATU",
    "GULA": "GULA PASIR",
    "ICE CREAM MANNGO": "ICE CREAM MANGO",
    "KALDU 3,5 CENTONG": "KALDU",
    "KEJU CEDAR": "KEJU CHEDDAR",
    "KEJU MOZARELLA": "KEJU MOZZARELLA",
    "LETUCE": "LETTUCE",
    "MACHA FURE": "MATCHA PURE",
    "MAIZENA 2 1/2 SDM": "MAIZENA",
    "MARGARINE": "MARGARIN",
    "MAYONASIE": "MAYONAISE",
    "PAKCOY": "PAKCOY HIDROPONIK",
    "PAKCOY HIDROFONIK": "PAKCOY HIDROPONIK",
    "PAPER BOX": "PAPER BOX",
    "PUDING MANGGO": "PUDING MANGO",
    "ROYKO AYAM": "ROYCO AYAM",
    "SALADA": "SELADA",
    "SAOS SACSET CABE": "SAOS SACHET CABE",
    "SAOS SACSET TOMAT": "SAOS SACHET TOMAT",
    "SAOS TERIAKI": "SAOS TERIYAKI",
    "SAUS KEJU": "SAOS KEJU",
    "SEDOTAN": "SEDOTAN HITAM BESAR",
    "STICER ALES": "STIKER ALES",
    "STIKER ALES": "STIKER ALES",
    "SUSU KENTAL DAIRY CHAM": "DAIRY CHARM",
    "SUSU KENTAL/DAIRY": "DAIRY CHARM",
    "SUSUS DANCOW FULL CREAM": "SUSU DANCOW FULL CREAM",
    "THAUSAND ISLAND": "THOUSAND ISLAND",
    "TIMUN": "MENTIMUN",
}

# Penyeragaman satuan dasar fisik (Base Unit of Measure): hanya 'gram', 'ml', atau 'pcs'
BASE_UNIT_OVERRIDES: dict[str, str] = {
    "AIR GALON": "ml",
    "AIR MINERAL": "pcs",
    "BUAH MANGGA": "gram",
    "BUMBU CABE": "ml",
    "BUMBU KERING": "gram",
    "BUMBU MINYAK": "gram",
    "CETAKAN PUDING": "pcs",
    "CUKA": "ml",
    "CUKA BERAS": "ml",
    "DAIRY CHARM": "gram",
    "ES BATU": "gram",
    "FN": "gram",
    "GARPU PLASTIK": "pcs",
    "ICE CREAM GREENTEA": "ml",
    "ICE CREAM MANGO": "ml",
    "ICE CREAM VANILA": "ml",
    "KALDU": "ml",
    "KECAP MANIS": "ml",
    "KIWI KONSENTRAT": "ml",
    "MAIZENA": "gram",
    "MARGARIN": "gram",
    "MINYAK GORENG": "ml",
    "PAPER BOX": "pcs",
    "PEWARNA BIRU": "ml",
    "PEWARNA HIJAU": "ml",
    "PEWARNA MERAH": "ml",
    "POWDER GREENTEA": "gram",
    "POWDER PINK VELVET": "gram",
    "ROTI BURGER": "pcs",
    "ROTI TAWAR": "pcs",
    "SAMBEL": "ml",
    "SANQUIK LEMON": "ml",
    "SANQUIK MANGGA": "ml",
    "SAOS TERIYAKI": "ml",
    "SAUS TAKOYAKI": "ml",
    "SEDOTAN HITAM BESAR": "pcs",
    "SENDOK MIRUKU": "pcs",
    "SOYU": "ml",
    "SPRITE": "ml",
    "STIKER ALES": "pcs",
    "STRAWBERRY BUAH": "pcs",
    "TELUR": "pcs",
    "TULANG BALUNG": "gram",
    "VANILLA": "gram",
    "WADAH MIRUKU": "pcs",
    "YAKULT": "pcs",
}

# Bahan kemasan/perlengkapan non-pangan
PACKAGING_KEYWORDS = (
    "BOX",
    "CETAKAN",
    "CUP",
    "GARPU",
    "GAS",
    "HI COOK",
    "KERTAS",
    "PLASTIK",
    "SEDOTAN",
    "SENDOK",
    "STIKER",
    "TUSUK",
    "WADAH",
)

# Resep dasar / kuah / batch yang tidak dijual langsung di kasir sebagai menu utama
SUB_RECIPE_NAMES = {
    "Kuah Hotplate",
    "SAUS SIRAM",
    "Kuah Asam Manis",
    "Saus Pedas Redhot",
    "Black Pepper",
    "Takoyaki",
}

# Daftar menu batch yang pemakaian bahannya di CSV ditulis untuk >1 porsi
# Format: prefix/exact_name -> (jumlah_yield_batch, porsi_jual_per_serving, label_porsi)
BATCH_MENU_RULES: list[tuple[str, float, float, str]] = [
    ("Sweet Takoyaki", 12.0, 6.0, "1 porsi (isi 6)"),
    ("Silky pudding", 12.0, 1.0, "1 cup"),
    ("Cau katsu", 15.0, 1.0, "1 porsi"),
    ("Miruku Bath", 16.0, 1.0, "1 porsi"),
    ("Takoyaki", 42.0, 1.0, "1 pcs (batch 42)"),
]


@dataclass
class IngredientRecord:
    nama_bahan: str
    nama_bahan_raw: set[str] = field(default_factory=set)
    kategori_vendor: str = "LAINNYA"
    satuan_dasar: str = "gram"
    isi_kemasan_beli: float = 1.0
    harga_beli_kemasan: float = 0.0
    harga_satuan_dasar: float = 0.0
    is_packaging: bool = False


@dataclass
class RecipeLine:
    raw_name: str
    canonical_name: str
    qty: float
    unit_raw: str
    harga_kemasan: float
    isi_kemasan: float
    harga_excel: float
    is_packaging_after_total: bool = False


@dataclass
class MenuRecipe:
    nama_menu: str
    kategori_menu: str
    porsi_standar: str
    batch_yield: float
    serving_yield: float
    is_sub_recipe: bool
    total_excel_raw: Optional[float]
    lines: list[RecipeLine] = field(default_factory=list)


def parse_number(val: str) -> Optional[float]:
    """Konversi string angka berformat koma ribuan (misal '  30,000 ') menjadi float."""
    if val is None:
        return None
    cleaned = val.strip().replace('"', "").replace(",", "")
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def canonicalize_ingredient(raw_name: str) -> str:
    """Bersihkan spasi ganda dan petakan sinonim/typo ke nama kanonikal."""
    clean = re.sub(r"\s+", " ", raw_name.strip()).upper()
    return INGREDIENT_ALIASES.get(clean, clean)


def normalize_unit(unit_raw: str, canonical_name: str, kemasan_qty: Optional[float] = None) -> str:
    """Tentukan satuan dasar baku ('gram', 'ml', 'pcs') untuk suatu bahan."""
    if canonical_name in BASE_UNIT_OVERRIDES:
        return BASE_UNIT_OVERRIDES[canonical_name]

    u = unit_raw.strip().lower()
    if u in ("gr", "gram", "g"):
        return "gram"
    if u in ("ml", "mililiter", "liter", "l"):
        # Pada DATA BASE.csv, item berlabel 'liter' (e.g. Minyak 2,000 / Sprite 1,500) sudah dalam ml
        return "ml"
    if u in ("pcs", "pc", "butir", "bottle", "botol", "porsi", "lembar"):
        return "pcs"
    return "gram"


def load_master_database(db_csv: Path) -> dict[str, IngredientRecord]:
    """Parse DATA BASE.csv menjadi dictionary master bahan baku terstandarisasi."""
    master: dict[str, IngredientRecord] = {}
    current_vendor = "UMUM"

    with open(db_csv, "r", encoding="utf-8", errors="ignore") as f:
        rows = list(csv.reader(f))

    for row in rows:
        c0 = row[0].strip() if len(row) > 0 else ""
        c1 = row[1].strip() if len(row) > 1 else ""
        c2 = row[2].strip() if len(row) > 2 else ""
        c3 = row[3].strip() if len(row) > 3 else ""
        c4 = row[4].strip() if len(row) > 4 else ""
        c5 = row[5].strip() if len(row) > 5 else ""

        # Header vendor berdiri sendiri
        if not c0 and c1 and not any(x.strip() for x in row[2:]):
            current_vendor = re.sub(r"\s+", " ", c1).upper()
            continue
        if c0.upper() == "NO":
            if c1 and c1.upper() != "BAHAN":
                current_vendor = re.sub(r"\s+", " ", c1).upper()
            elif not c1:
                current_vendor = "SUPPLIER LAINNYA"
            continue

        if c0.isdigit() and c1:
            canon = canonicalize_ingredient(c1)
            harga = parse_number(c2) or 0.0
            kemasan = parse_number(c3) or 1.0
            harga_satuan_file = parse_number(c5)
            unit = normalize_unit(c4, canon, kemasan)

            # Hitung harga satuan per base unit secara konsisten
            calc_unit_price = round(harga / kemasan, 4) if kemasan > 0 and harga > 0 else (harga_satuan_file or 0.0)
            is_pkg = any(kw in canon for kw in PACKAGING_KEYWORDS)

            # Penanganan khusus duplikat MISO di DATA BASE.csv:
            # Baris 50 (165,000) adalah harga lama; baris 115 (60,000) adalah yang dipakai di resep Ramen.
            if canon == "MISO" and canon in master and harga < master[canon].harga_beli_kemasan:
                master[canon].harga_beli_kemasan = harga
                master[canon].isi_kemasan_beli = kemasan
                master[canon].harga_satuan_dasar = calc_unit_price
                master[canon].nama_bahan_raw.add(c1.strip())
                continue

            if canon not in master:
                master[canon] = IngredientRecord(
                    nama_bahan=canon,
                    nama_bahan_raw={c1.strip()},
                    kategori_vendor=current_vendor,
                    satuan_dasar=unit,
                    isi_kemasan_beli=kemasan,
                    harga_beli_kemasan=harga,
                    harga_satuan_dasar=calc_unit_price,
                    is_packaging=is_pkg,
                )
            else:
                master[canon].nama_bahan_raw.add(c1.strip())

    # Override harga Paper Box yang kosong di DATA BASE.csv menggunakan harga di resep Cau Katsu (Rp1.500/pcs)
    if "PAPER BOX" in master and master["PAPER BOX"].harga_satuan_dasar == 0.0:
        master["PAPER BOX"].harga_beli_kemasan = 1500.0
        master["PAPER BOX"].isi_kemasan_beli = 1.0
        master["PAPER BOX"].harga_satuan_dasar = 1500.0

    return master


def normalize_menu_name(raw_name: str) -> str:
    """Rapikan kapitalisasi dan typo ringan pada nama menu untuk tampilan web UI."""
    clean = re.sub(r"\s+", " ", raw_name.strip())
    words = clean.split(" ")
    formatted: list[str] = []
    for w in words:
        up = w.upper()
        if up in ("HP", "BP"):
            formatted.append(up)
        elif up == "SMOOKED":
            formatted.append("Smoked")
        elif up == "OTAK2":
            formatted.append("Otak-Otak")
        elif (len(w) > 1 and w.isupper()) or w.islower():
            formatted.append(w.capitalize())
        else:
            formatted.append(w)
    return " ".join(formatted)


def get_batch_config(menu_name: str) -> tuple[float, float, str]:
    """Tentukan (batch_yield, serving_yield, porsi_standar) untuk suatu menu."""
    for prefix, batch_y, serve_y, label in BATCH_MENU_RULES:
        if prefix == "Takoyaki":
            if menu_name.strip().lower() == "takoyaki":
                return batch_y, serve_y, label
        elif menu_name.lower().startswith(prefix.lower()):
            return batch_y, serve_y, label
    return 1.0, 1.0, "1 porsi"


def is_header_row(rows: list[list[str]], idx: int) -> bool:
    """Cek apakah baris idx adalah nama menu karena baris idx+1 adalah header tabel 'No, Bahan'."""
    if idx + 1 >= len(rows):
        return False
    next_row = rows[idx + 1]
    n0 = next_row[0].strip().upper() if len(next_row) > 0 else ""
    n1 = next_row[1].strip().upper() if len(next_row) > 1 else ""
    return n0 == "NO" and n1 == "BAHAN"


def parse_recipe_file(fpath: Path, master: dict[str, IngredientRecord]) -> list[MenuRecipe]:
    """Parse satu file CSV resep kategori menu menjadi daftar objek MenuRecipe."""
    kategori = (
        fpath.name.replace("Data Bahan Baku Menu (2018).xlsx - ", "")
        .replace(".csv", "")
        .strip()
        .upper()
    )
    if kategori == "NASI GORENG":
        # Isi file NASI GORENG.csv seluruhnya adalah varian Omurice
        kategori = "NASI GORENG / OMURICE"

    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        rows = list(csv.reader(f))

    # Deteksi apakah file punya kolom 'satuan' (HOTPLATE dan RAMEN hanya 6 kolom)
    has_satuan_col = not any(k in fpath.name.upper() for k in ("HOTPLATE", "RAMEN"))

    menus: list[MenuRecipe] = []
    current_menu: Optional[MenuRecipe] = None
    passed_first_total = False

    i = 0
    while i < len(rows):
        row = rows[i]
        c0 = row[0].strip() if len(row) > 0 else ""
        c1 = row[1].strip() if len(row) > 1 else ""

        # 1. Cek awal blok menu baru
        if is_header_row(rows, i):
            menu_name = normalize_menu_name(c0 or c1)
            batch_y, serve_y, porsi_label = get_batch_config(menu_name)
            is_sub = menu_name.lower() in {s.lower() for s in SUB_RECIPE_NAMES}

            current_menu = MenuRecipe(
                nama_menu=menu_name,
                kategori_menu=kategori,
                porsi_standar=porsi_label,
                batch_yield=batch_y,
                serving_yield=serve_y,
                is_sub_recipe=is_sub,
                total_excel_raw=None,
            )
            menus.append(current_menu)
            passed_first_total = False
            i += 2  # Lewati baris header 'No, Bahan, ...'
            continue

        if current_menu is None:
            i += 1
            continue

        # 2. Deteksi baris TOTAL / summary angka
        is_total_keyword = c0.upper() == "TOTAL"
        col_harga_idx = 6 if has_satuan_col else 5
        col_harga_val = parse_number(row[col_harga_idx]) if len(row) > col_harga_idx else None
        col_unit_val = row[col_harga_idx + 1].strip().lower() if len(row) > col_harga_idx + 1 else ""

        # Baris grand total tanpa kata 'TOTAL' (misal Donburi Mozaru Katsu atau baris bawah Cau Katsu/Miruku)
        is_summary_row = (
            not c0
            and not c1
            and col_harga_val is not None
            and col_unit_val != "satuan"
        )

        if is_total_keyword or is_summary_row:
            if not passed_first_total:
                passed_first_total = True
                if current_menu.batch_yield == 1.0 and col_harga_val is not None:
                    current_menu.total_excel_raw = col_harga_val
                elif col_harga_val is not None and current_menu.batch_yield > 1.0:
                    # Untuk batch (e.g. Sweet Takoyaki isi 6 atau Cau Katsu /15), cek apakah ada total per porsi di kolom sebelah
                    if "sweet takoyaki" in current_menu.nama_menu.lower() and len(row) > 8 and parse_number(row[8]) is not None:
                        current_menu.total_excel_raw = parse_number(row[8])
                    else:
                        current_menu.total_excel_raw = round(col_harga_val / current_menu.batch_yield, 2)
            else:
                # Untuk Cau katsu & Miruku Bath, baris paling bawah (setelah Total packaging) adalah grand total per porsi
                if col_harga_val is not None and not is_total_keyword:
                    current_menu.total_excel_raw = col_harga_val
            i += 1
            continue

        # Baris sub-header satuan di Silky Pudding (`1,288.89, satuan`)
        if not c0 and not c1 and col_unit_val == "satuan" and col_harga_val is not None:
            current_menu.total_excel_raw = col_harga_val
            i += 1
            continue

        # 3. Deteksi baris item bahan (nomor digit atau tanpa nomor seperti LEMON BUAH di Leci Mint tea)
        usage_val = parse_number(row[4]) if len(row) > 4 else None
        if c1 and (c0.isdigit() or (not c0 and usage_val is not None)):
            raw_ing = c1.strip()
            canon_ing = canonicalize_ingredient(raw_ing)
            harga_k = parse_number(row[2]) or 0.0
            isi_k = parse_number(row[3]) or 1.0
            qty = usage_val or 0.0
            unit_raw = row[5].strip() if (has_satuan_col and len(row) > 5) else ""
            harga_line = col_harga_val or 0.0

            # Jangan daftarkan sub-resep (KUAH HOTPLATE / TAKOYAKI / MIRUKU 1) sebagai bahan baku gudang
            if canon_ing not in ("KUAH HOTPLATE", "TAKOYAKI", "MIRUKU 1"):
                if canon_ing not in master:
                    unit_std = normalize_unit(unit_raw, canon_ing, isi_k)
                    unit_price = round(harga_k / isi_k, 4) if isi_k > 0 and harga_k > 0 else round(harga_line / qty, 4) if qty > 0 else 0.0
                    is_pkg = any(kw in canon_ing for kw in PACKAGING_KEYWORDS)
                    master[canon_ing] = IngredientRecord(
                        nama_bahan=canon_ing,
                        nama_bahan_raw={raw_ing},
                        kategori_vendor="TAMBAHAN DARI RESEP",
                        satuan_dasar=unit_std,
                        isi_kemasan_beli=isi_k if harga_k > 0 else 1.0,
                        harga_beli_kemasan=harga_k if harga_k > 0 else unit_price,
                        harga_satuan_dasar=unit_price,
                        is_packaging=is_pkg,
                    )
                else:
                    master[canon_ing].nama_bahan_raw.add(raw_ing)

            current_menu.lines.append(
                RecipeLine(
                    raw_name=raw_ing,
                    canonical_name=canon_ing,
                    qty=qty,
                    unit_raw=unit_raw,
                    harga_kemasan=harga_k,
                    isi_kemasan=isi_k,
                    harga_excel=harga_line,
                    is_packaging_after_total=passed_first_total,
                )
            )

        i += 1

    return menus


def resolve_bom_lines(
    menus: list[MenuRecipe],
) -> tuple[list[MenuRecipe], dict[str, dict[str, float]]]:
    """
    Hitung kuantitas per 1 porsi jual, ratakan (flatten) sub-resep (Kuah Hotplate & Takoyaki),
    dan gabungkan bahan duplikat dalam satu menu yang sama.
    """
    menu_lookup = {m.nama_menu.lower(): m for m in menus}
    final_menus: list[MenuRecipe] = []
    bom_map: dict[str, dict[str, float]] = {}

    for m in menus:
        # Skip stub circular 'Miruku 1'
        if m.nama_menu.strip().lower() == "miruku 1":
            continue

        scale = m.serving_yield / m.batch_yield
        agg: dict[str, float] = defaultdict(float)

        for line in m.lines:
            qty_scaled = line.qty if line.is_packaging_after_total else line.qty * scale

            # Flatten sub-recipe KUAH HOTPLATE di Cah jamur
            if line.canonical_name == "KUAH HOTPLATE" and "kuah hotplate" in menu_lookup:
                sub = menu_lookup["kuah hotplate"]
                for sub_line in sub.lines:
                    agg[sub_line.canonical_name] += sub_line.qty * qty_scaled
            # Flatten sub-recipe TAKOYAKI di takoyaki isi 6 / 9 / 12
            elif line.canonical_name == "TAKOYAKI" and "takoyaki" in menu_lookup:
                sub = menu_lookup["takoyaki"]
                sub_scale = qty_scaled / sub.batch_yield
                for sub_line in sub.lines:
                    agg[sub_line.canonical_name] += sub_line.qty * sub_scale
            else:
                agg[line.canonical_name] += qty_scaled

        final_menus.append(m)
        bom_map[m.nama_menu] = {k: round(v, 4) for k, v in agg.items() if v > 0}

    return final_menus, bom_map


def export_outputs(
    master: dict[str, IngredientRecord],
    menus: list[MenuRecipe],
    bom_map: dict[str, dict[str, float]],
) -> None:
    """Ekspor 4 tabel ternormalisasi ke CSV, SQLite (.db), dan script SQL."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. dim_kategori_menu
    categories = sorted({m.kategori_menu for m in menus})
    cat_id_map = {cat: idx + 1 for idx, cat in enumerate(categories)}

    with open(OUT_DIR / "dim_kategori_menu.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id_kategori", "nama_kategori"])
        for cat, cid in cat_id_map.items():
            w.writerow([cid, cat])

    # 2. dim_bahan_baku
    sorted_ings = sorted(master.keys())
    ing_id_map = {name: idx + 1 for idx, name in enumerate(sorted_ings)}

    with open(OUT_DIR / "dim_bahan_baku.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "id_bahan",
            "nama_bahan",
            "alias_mentah",
            "kategori_vendor",
            "satuan_dasar",
            "isi_kemasan_beli",
            "harga_beli_kemasan",
            "harga_satuan_dasar",
            "stok_saat_ini",
            "stok_minimum",
            "is_packaging",
        ])
        for name in sorted_ings:
            rec = master[name]
            aliases = " | ".join(sorted(rec.nama_bahan_raw))
            w.writerow([
                ing_id_map[name],
                rec.nama_bahan,
                aliases,
                rec.kategori_vendor,
                rec.satuan_dasar,
                rec.isi_kemasan_beli,
                rec.harga_beli_kemasan,
                rec.harga_satuan_dasar,
                0.0,  # Saldo awal stok di gudang (diisi user/admin di web)
                0.0,  # Batas minimum reorder point
                int(rec.is_packaging),
            ])

    # 3. dim_menu & 4. fact_resep_bom
    menu_id_map = {m.nama_menu: idx + 1 for idx, m in enumerate(menus)}
    menu_rows = []
    bom_rows = []
    resep_pk = 1

    for m in menus:
        mid = menu_id_map[m.nama_menu]
        cid = cat_id_map[m.kategori_menu]
        ingredients = bom_map[m.nama_menu]

        hpp_std = 0.0
        for ing_name, qty in ingredients.items():
            iid = ing_id_map[ing_name]
            rec = master[ing_name]
            cost = round(qty * rec.harga_satuan_dasar, 2)
            hpp_std += cost
            bom_rows.append([
                resep_pk,
                mid,
                iid,
                qty,
                rec.satuan_dasar,
                cost,
            ])
            resep_pk += 1

        menu_rows.append([
            mid,
            cid,
            m.nama_menu,
            m.porsi_standar,
            int(m.is_sub_recipe),
            int(not m.is_sub_recipe),
            round(hpp_std, 2),
            m.total_excel_raw if m.total_excel_raw is not None else "",
        ])

    with open(OUT_DIR / "dim_menu.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "id_menu",
            "id_kategori",
            "nama_menu",
            "porsi_standar",
            "is_sub_recipe",
            "is_sellable",
            "total_hpp_standar",
            "total_hpp_excel_raw",
        ])
        w.writerows(menu_rows)

    with open(OUT_DIR / "fact_resep_bom.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "id_resep",
            "id_menu",
            "id_bahan",
            "jumlah_pemakaian",
            "satuan_pemakaian",
            "estimasi_biaya_bahan",
        ])
        w.writerows(bom_rows)

    # 5. SQLite Database & 6. SQL Script
    build_sqlite_and_sql(cat_id_map, sorted_ings, ing_id_map, master, menu_rows, bom_rows)


def sql_escape(text: str) -> str:
    return text.replace("'", "''")


def build_sqlite_and_sql(
    cat_id_map: dict[str, int],
    sorted_ings: list[str],
    ing_id_map: dict[str, int],
    master: dict[str, IngredientRecord],
    menu_rows: list[list],
    bom_rows: list[list],
) -> None:
    """Bangun database SQLite dan file schema_and_seed.sql yang kompatibel lintas RDBMS."""
    db_path = OUT_DIR / "inventory_resto.db"
    sql_path = OUT_DIR / "schema_and_seed.sql"

    if db_path.exists():
        db_path.unlink()

    ddl_statements = [
        """-- Skema Database Manajemen Stok & Resep (BOM) Ale's Place
CREATE TABLE IF NOT EXISTS dim_kategori_menu (
    id_kategori INTEGER PRIMARY KEY,
    nama_kategori VARCHAR(100) NOT NULL UNIQUE
);""",
        """CREATE TABLE IF NOT EXISTS dim_bahan_baku (
    id_bahan INTEGER PRIMARY KEY,
    nama_bahan VARCHAR(150) NOT NULL UNIQUE,
    alias_mentah TEXT,
    kategori_vendor VARCHAR(100),
    satuan_dasar VARCHAR(20) NOT NULL,
    isi_kemasan_beli DECIMAL(12, 4) NOT NULL DEFAULT 1,
    harga_beli_kemasan DECIMAL(14, 2) NOT NULL DEFAULT 0,
    harga_satuan_dasar DECIMAL(14, 4) NOT NULL DEFAULT 0,
    stok_saat_ini DECIMAL(14, 4) NOT NULL DEFAULT 0,
    stok_minimum DECIMAL(14, 4) NOT NULL DEFAULT 0,
    is_packaging INTEGER NOT NULL DEFAULT 0
);""",
        """CREATE TABLE IF NOT EXISTS dim_menu (
    id_menu INTEGER PRIMARY KEY,
    id_kategori INTEGER NOT NULL,
    nama_menu VARCHAR(150) NOT NULL UNIQUE,
    porsi_standar VARCHAR(50) NOT NULL DEFAULT '1 porsi',
    is_sub_recipe INTEGER NOT NULL DEFAULT 0,
    is_sellable INTEGER NOT NULL DEFAULT 1,
    total_hpp_standar DECIMAL(14, 2) NOT NULL DEFAULT 0,
    total_hpp_excel_raw DECIMAL(14, 2),
    FOREIGN KEY (id_kategori) REFERENCES dim_kategori_menu(id_kategori)
);""",
        """CREATE TABLE IF NOT EXISTS fact_resep_bom (
    id_resep INTEGER PRIMARY KEY,
    id_menu INTEGER NOT NULL,
    id_bahan INTEGER NOT NULL,
    jumlah_pemakaian DECIMAL(12, 4) NOT NULL,
    satuan_pemakaian VARCHAR(20) NOT NULL,
    estimasi_biaya_bahan DECIMAL(14, 2) NOT NULL DEFAULT 0,
    UNIQUE (id_menu, id_bahan),
    FOREIGN KEY (id_menu) REFERENCES dim_menu(id_menu),
    FOREIGN KEY (id_bahan) REFERENCES dim_bahan_baku(id_bahan)
);""",
        """CREATE VIEW IF NOT EXISTS v_resep_lengkap AS
SELECT
    m.id_menu,
    k.nama_kategori,
    m.nama_menu,
    m.porsi_standar,
    m.is_sellable,
    b.id_bahan,
    b.nama_bahan,
    r.jumlah_pemakaian,
    r.satuan_pemakaian,
    r.estimasi_biaya_bahan,
    m.total_hpp_standar
FROM fact_resep_bom r
JOIN dim_menu m ON r.id_menu = m.id_menu
JOIN dim_kategori_menu k ON m.id_kategori = k.id_kategori
JOIN dim_bahan_baku b ON r.id_bahan = b.id_bahan;""",
    ]

    sql_lines: list[str] = list(ddl_statements)
    sql_lines.append("\n-- Seed: dim_kategori_menu")
    for cat, cid in cat_id_map.items():
        sql_lines.append(
            f"INSERT INTO dim_kategori_menu (id_kategori, nama_kategori) VALUES ({cid}, '{sql_escape(cat)}');"
        )

    sql_lines.append("\n-- Seed: dim_bahan_baku")
    for name in sorted_ings:
        rec = master[name]
        aliases = " | ".join(sorted(rec.nama_bahan_raw))
        sql_lines.append(
            "INSERT INTO dim_bahan_baku (id_bahan, nama_bahan, alias_mentah, kategori_vendor, satuan_dasar, "
            "isi_kemasan_beli, harga_beli_kemasan, harga_satuan_dasar, stok_saat_ini, stok_minimum, is_packaging) "
            f"VALUES ({ing_id_map[name]}, '{sql_escape(rec.nama_bahan)}', '{sql_escape(aliases)}', "
            f"'{sql_escape(rec.kategori_vendor)}', '{rec.satuan_dasar}', {rec.isi_kemasan_beli}, "
            f"{rec.harga_beli_kemasan}, {rec.harga_satuan_dasar}, 0, 0, {int(rec.is_packaging)});"
        )

    sql_lines.append("\n-- Seed: dim_menu")
    for r in menu_rows:
        raw_hpp = "NULL" if r[7] == "" else str(r[7])
        sql_lines.append(
            "INSERT INTO dim_menu (id_menu, id_kategori, nama_menu, porsi_standar, is_sub_recipe, is_sellable, "
            "total_hpp_standar, total_hpp_excel_raw) "
            f"VALUES ({r[0]}, {r[1]}, '{sql_escape(r[2])}', '{sql_escape(r[3])}', {r[4]}, {r[5]}, {r[6]}, {raw_hpp});"
        )

    sql_lines.append("\n-- Seed: fact_resep_bom")
    for r in bom_rows:
        sql_lines.append(
            "INSERT INTO fact_resep_bom (id_resep, id_menu, id_bahan, jumlah_pemakaian, satuan_pemakaian, estimasi_biaya_bahan) "
            f"VALUES ({r[0]}, {r[1]}, {r[2]}, {r[3]}, '{r[4]}', {r[5]});"
        )

    full_sql = "\n".join(sql_lines)
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write(full_sql)

    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(full_sql)
        conn.commit()
    finally:
        conn.close()


def main() -> None:
    db_csv = RAW_DIR / "Data Bahan Baku Menu (2018).xlsx - DATA BASE.csv"
    master = load_master_database(db_csv)

    all_menus: list[MenuRecipe] = []
    for fpath in sorted(glob.glob(str(RAW_DIR / "*.csv"))):
        p = Path(fpath)
        if "DATA BASE" in p.name.upper():
            continue
        all_menus.extend(parse_recipe_file(p, master))

    clean_menus, bom_map = resolve_bom_lines(all_menus)
    export_outputs(master, clean_menus, bom_map)

    print("=== NORMALISASI SELESAI ===")
    print(f"Kategori Menu    : {len({m.kategori_menu for m in clean_menus})}")
    print(f"Master Bahan Baku: {len(master)}")
    print(f"Total Menu Resep : {len(clean_menus)} (Sellable: {sum(1 for m in clean_menus if not m.is_sub_recipe)})")
    print(f"Total Baris BOM  : {sum(len(v) for v in bom_map.values())}")
    print(f"Output Folder    : {OUT_DIR}")


if __name__ == "__main__":
    main()
