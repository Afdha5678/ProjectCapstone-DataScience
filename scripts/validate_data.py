"""Script validasi & audit integritas hasil normalisasi Data Bahan Makanan."""

import sqlite3
from pathlib import Path

DB_PATH = Path(r"D:\0. Dokumen Kuliah\Semester 5\0. Project Capstone\processed_data\inventory_resto.db")


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # 1. Foreign key integrity check
    fk_errors = conn.execute("PRAGMA foreign_key_check;").fetchall()
    print(f"FK Errors: {len(fk_errors)}")
    assert len(fk_errors) == 0, f"Found FK errors: {fk_errors}"

    # 2. Check ingredients with 0 price or unusual units
    zero_price = conn.execute(
        "SELECT id_bahan, nama_bahan, satuan_dasar, harga_satuan_dasar FROM dim_bahan_baku WHERE harga_satuan_dasar <= 0"
    ).fetchall()
    print(f"\nBahan dengan harga 0 ({len(zero_price)}):")
    for r in zero_price:
        print(dict(r))

    units = conn.execute(
        "SELECT satuan_dasar, COUNT(*) as cnt FROM dim_bahan_baku GROUP BY satuan_dasar"
    ).fetchall()
    print("\nDistribusi satuan dasar:", [dict(u) for u in units])

    # 3. Check menus with 0 BOM rows
    empty_menus = conn.execute(
        """
        SELECT m.id_menu, m.nama_menu
        FROM dim_menu m
        LEFT JOIN fact_resep_bom r ON m.id_menu = r.id_menu
        WHERE r.id_resep IS NULL
        """
    ).fetchall()
    print(f"\nMenu tanpa bahan ({len(empty_menus)}):", [dict(x) for x in empty_menus])

    # 4. Check HPP discrepancies vs raw Excel
    menus = conn.execute(
        """
        SELECT k.nama_kategori, m.nama_menu, m.porsi_standar, m.is_sellable,
               m.total_hpp_standar, m.total_hpp_excel_raw,
               ABS(m.total_hpp_standar - COALESCE(m.total_hpp_excel_raw, m.total_hpp_standar)) AS diff
        FROM dim_menu m
        JOIN dim_kategori_menu k ON m.id_kategori = k.id_kategori
        ORDER BY diff DESC
        """
    ).fetchall()

    missing_raw = [dict(m) for m in menus if m["total_hpp_excel_raw"] is None]
    print(f"\nMenu tanpa total_hpp_excel_raw ({len(missing_raw)}):")
    for m in missing_raw:
        print(f"  [{m['nama_kategori']}] {m['nama_menu']}: std={m['total_hpp_standar']}")

    big_diff = [dict(m) for m in menus if m["diff"] > 500]
    print(f"\nMenu dengan selisih HPP > Rp 500 ({len(big_diff)}):")
    for m in big_diff:
        print(
            f"  [{m['nama_kategori']}] {m['nama_menu']} ({m['porsi_standar']}): "
            f"std={m['total_hpp_standar']} vs excel={m['total_hpp_excel_raw']} (diff={m['diff']:.2f})"
        )

    # 5. Sample flattened & batch recipes
    samples = [
        "takoyaki isi 6",
        "Cah jamur",
        "Cau katsu Chocomaltine",
        "Miruku Bath",
        "Silky pudding Coklat",
        "Sweet Takoyaki Greentea",
        "Omurice",
    ]
    for s in samples:
        rows = conn.execute(
            """
            SELECT nama_bahan, jumlah_pemakaian, satuan_pemakaian, estimasi_biaya_bahan, total_hpp_standar
            FROM v_resep_lengkap
            WHERE LOWER(nama_menu) = LOWER(?)
            ORDER BY id_bahan
            """,
            (s,),
        ).fetchall()
        print(f"\n--- Sample BOM: {s} ({len(rows)} bahan) ---")
        for r in rows[:6]:
            print(f"  {r['nama_bahan']}: {r['jumlah_pemakaian']} {r['satuan_pemakaian']} (Rp {r['estimasi_biaya_bahan']})")
        if len(rows) > 6:
            print(f"  ... (+{len(rows) - 6} bahan lainnya), Total HPP Std: Rp {rows[0]['total_hpp_standar']}")

    conn.close()


if __name__ == "__main__":
    main()
