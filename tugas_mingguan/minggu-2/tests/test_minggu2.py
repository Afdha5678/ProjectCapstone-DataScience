"""
Suite Pengujian Otomatis Minggu 2 (Data Science Scope - Tim A26-CS218):
1. Uji BoMEngine: konversi BoM, alias kasir, buffer waste, stock-in kemasan, stock opname, void lines,
   serta parsing file CSV mentah NutaCloud langsung.
2. Uji StockAnalytics: Daily Burn Rate, Safety Stock, ROP, DOI, & klasifikasi status kritis.
3. Uji Anti-Data-Leakage pada dataset AI (`tugas_mingguan/minggu-2/output/data_for_ai/`) untuk tim AE.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd

MINGGU_2_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = Path(__file__).resolve().parents[3]
if str(MINGGU_2_DIR) not in sys.path:
    sys.path.insert(0, str(MINGGU_2_DIR))

from src.bom_engine import BoMEngine
from src.stock_analytics import evaluate_inventory_health


class TestMinggu2DS(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = BoMEngine()
        cls.sim_stock = cls.engine.create_simulated_stock(coverage_days=7.0)

    def test_simulated_stock_labeling(self) -> None:
        """Pastikan stok simulasi awal memiliki label jelas sesuai rubrik AI #1 & Dasbor #4."""
        self.assertTrue(self.sim_stock["is_simulated_stock"].all())
        self.assertEqual(self.sim_stock["data_label"].iloc[0], "SIMULASI_7_HARI_HISTORIS")
        self.assertEqual(len(self.sim_stock), 178)

    def test_bom_deduction_exact_alias_and_buffer(self) -> None:
        """Uji pemotongan stok via alias ('Redhot Beef Ramen') & margin toleransi buffer 10%."""
        orders = [
            {"nama_item": "Redhot Beef Ramen", "qty": 2},
            {"nama_item": "Takoyaki Isi 6", "qty": 1},
            {"nama_item": "Menu Fiktif Baru", "qty": 3},
        ]
        res = self.engine.deduct_from_sales(orders, self.sim_stock, buffer_waste_pct=0.10)
        self.assertEqual(res.total_portions_processed, 3.0)
        self.assertEqual(res.total_portions_unmapped, 3.0)
        self.assertEqual(len(res.unmapped_items), 1)

        # Ramen Redhot Beef memakai 60g MIE per porsi -> 2 porsi = 120g teoritis + 10% buffer = 132g
        mie_row = res.deductions_df[res.deductions_df["nama_bahan"] == "MIE"].iloc[0]
        self.assertAlmostEqual(mie_row["pemakaian_teoritis"], 120.0, places=2)
        self.assertAlmostEqual(mie_row["buffer_waste"], 12.0, places=2)
        self.assertAlmostEqual(mie_row["total_pengurangan"], 132.0, places=2)
        self.assertAlmostEqual(
            mie_row["stok_sesudah"], mie_row["stok_sebelum"] - 132.0, places=2
        )

    def test_void_line_cancels_out(self) -> None:
        """Pastikan baris void (-1) membatalkan baris (+1) sehingga total pengurangan nol."""
        orders = [
            {"nama_item": "Ramen Soyu", "qty": 1},
            {"nama_item": "Ramen Soyu", "qty": -1},
        ]
        res = self.engine.deduct_from_sales(orders, self.sim_stock, buffer_waste_pct=0.05)
        self.assertTrue(res.deductions_df.empty)

    def test_stock_in_and_opname(self) -> None:
        """Uji konversi kemasan saat Stock-In dan selisih variance saat Stock Opname."""
        beras_id = int(self.sim_stock.loc[self.sim_stock["nama_bahan"] == "BERAS", "id_bahan"].iloc[0])
        before = float(self.sim_stock.loc[self.sim_stock["id_bahan"] == beras_id, "stok_saat_ini"].iloc[0])

        # Beli 2 sak beras (@25.000 gram) -> +50.000 gram
        upd, info = self.engine.apply_stock_in(self.sim_stock, beras_id, 2.0)
        self.assertAlmostEqual(info["added_base_qty"], 50000.0, places=2)
        self.assertAlmostEqual(info["stok_sesudah"], before + 50000.0, places=2)

        # Opname aktual misal 10.000 gram
        upd2, var_df = self.engine.apply_stock_opname(upd, {beras_id: 10000.0})
        self.assertAlmostEqual(var_df.iloc[0]["selisih_variance"], 10000.0 - (before + 50000.0), places=2)
        self.assertEqual(
            upd2.loc[upd2["id_bahan"] == beras_id, "data_label"].iloc[0], "ACTUAL_OPNAME"
        )

    def test_parse_real_nutacloud_raw_csv(self) -> None:
        """Uji parser CSV mentah NutaCloud pada file bulan Oktober 2026."""
        raw_oct26 = (
            WORKSPACE_DIR
            / "Data Penjualan"
            / "13. Laporan Penjualan Ale s Place 01 Oktober 2026 - 31 Oktober 2026.xlsx - Worksheet.csv"
        )
        parsed = self.engine.parse_nutacloud_csv(raw_oct26)
        self.assertFalse(parsed.empty)
        self.assertFalse(parsed["nama_item_bersih"].isin(["Pajak Daerah", "Pembulatan"]).any())
        res = self.engine.deduct_from_sales(parsed, self.sim_stock, buffer_waste_pct=0.05)
        self.assertGreater(res.total_portions_processed, 1000.0)
        self.assertFalse(res.deductions_df.empty)

    def test_inventory_health_safety_stock_and_doi(self) -> None:
        """Uji perhitungan Safety Stock, ROP, DOI, dan deteksi status KRITIS saat stok diturunkan."""
        test_stock = self.sim_stock.copy()
        # Turunkan stok DAGING SAPI menjadi 100 gram (burn rate ~685g/hari -> wajib KRITIS!)
        test_stock.loc[test_stock["nama_bahan"] == "DAGING SAPI", "stok_saat_ini"] = 100.0
        health = evaluate_inventory_health(test_stock, z_score=1.65, mode_hari="overall")

        sapi = health[health["nama_bahan"] == "DAGING SAPI"].iloc[0]
        self.assertEqual(sapi["status_stok"], "KRITIS")
        self.assertLess(sapi["days_of_inventory"], 1.0)
        self.assertGreater(sapi["safety_stock"], 0.0)
        self.assertGreater(sapi["saran_beli_kemasan"], 0)

    def test_ai_dataset_anti_leakage(self) -> None:
        """Pastikan train/test split untuk tim AE benar-benar bebas tumpang tindih & lag bersifat kausal."""
        ai_dir = MINGGU_2_DIR / "output" / "data_for_ai"
        train_df = pd.read_csv(ai_dir / "train_daily_usage.csv")
        test_df = pd.read_csv(ai_dir / "test_daily_usage.csv")

        self.assertLess(train_df["tanggal"].max(), test_df["tanggal"].min())
        self.assertEqual(train_df["tanggal"].max(), "2026-09-30")
        self.assertEqual(test_df["tanggal"].min(), "2026-10-01")

        # Cek kausalitas lag_1 untuk DAGING SAPI (id_bahan = 41) di hari pertama test (2026-10-01)
        last_train_val = train_df[
            (train_df["id_bahan"] == 41) & (train_df["tanggal"] == "2026-09-30")
        ]["total_pemakaian"].iloc[0]
        first_test_lag1 = test_df[
            (test_df["id_bahan"] == 41) & (test_df["tanggal"] == "2026-10-01")
        ]["lag_1"].iloc[0]
        self.assertAlmostEqual(last_train_val, first_test_lag1, places=4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
