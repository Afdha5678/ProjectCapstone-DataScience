"""
Prototipe Dasbor Monitoring & Analisis Stok Bahan Baku — Ale's Place Cipoho (Tim A26-CS218).
Lingkup Kerja: Data Science Specialist (Minggu 2 — Rubrik Dasbor #1 s.d. #4).

Jalankan dengan:
    streamlit run tugas_mingguan/minggu-2/app/dashboard_streamlit.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

MINGGU_2_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = Path(__file__).resolve().parents[3]
if str(MINGGU_2_DIR) not in sys.path:
    sys.path.insert(0, str(MINGGU_2_DIR))

from src.bom_engine import BoMEngine
from src.stock_analytics import evaluate_inventory_health

DWH_PATH = WORKSPACE_DIR / "tugas_mingguan" / "minggu-1" / "output" / "data_penjualan" / "ales_place_dwh.db"
BURN_SUMMARY_PATH = MINGGU_2_DIR / "output" / "data_for_ai" / "ingredient_burn_rate_summary.csv"
FULL_FEATURES_PATH = MINGGU_2_DIR / "output" / "data_for_ai" / "daily_usage_full_features.csv"

st.set_page_config(
    page_title="Ale's Place — Monitoring Stok Bahan Baku (DS Prototype)",
    page_icon="🍜",
    layout="wide",
)


@st.cache_resource
def get_engine() -> BoMEngine:
    return BoMEngine(DWH_PATH)


@st.cache_data
def load_historical_usage() -> pd.DataFrame:
    if FULL_FEATURES_PATH.exists():
        return pd.read_csv(FULL_FEATURES_PATH)
    return pd.DataFrame()


def init_session_state(engine: BoMEngine) -> None:
    if "stock_df" not in st.session_state:
        st.session_state["stock_df"] = engine.create_simulated_stock(
            burn_summary_path=BURN_SUMMARY_PATH, coverage_days=7.0
        )
    if "mutation_logs" not in st.session_state:
        st.session_state["mutation_logs"] = []


def main() -> None:
    engine = get_engine()
    init_session_state(engine)

    st.title("🍜 Prototipe Dasbor Monitoring Stok Bahan Baku — Ale's Place Cipoho")
    st.caption(
        "Tim Capstone A26-CS218 (Data Science) | Berbasis data primer NutaCloud (Okt 2025 – Okt 2026) "
        "& Master Resep BoM (2018)"
    )

    # Sidebar parameter operasional & label data
    with st.sidebar:
        st.header("⚙️ Parameter Analitik Stok")
        mode_hari = st.selectbox(
            "Basis Laju Pemakaian (Burn Rate)",
            options=["overall", "weekend", "weekday", "recent_30d"],
            format_func=lambda x: {
                "overall": "Rata-Rata Keseluruhan (395 Hari Aktif)",
                "weekend": "Akhir Pekan (Jumat–Minggu)",
                "weekday": "Hari Kerja (Senin–Kamis)",
                "recent_30d": "Tren 30 Hari Terakhir (Okt 2026)",
            }[x],
        )
        z_score = st.slider("Tingkat Layanan Safety Stock (Z-Score)", 1.0, 2.33, 1.65, 0.05)
        buffer_waste = st.slider("Margin Toleransi Waste Dapur (%)", 0, 15, 5, 1) / 100.0
        sim_days = st.number_input("Reset Saldo Simulasi Awal (Hari Stok)", min_value=1, max_value=30, value=7)
        if st.button("🔄 Reset ke Saldo Simulasi Awal"):
            st.session_state["stock_df"] = engine.create_simulated_stock(
                burn_summary_path=BURN_SUMMARY_PATH, coverage_days=float(sim_days)
            )
            st.session_state["mutation_logs"] = []
            st.success(f"Saldo stok direset ke simulasi kebutuhan {sim_days} hari.")

    health_df = evaluate_inventory_health(
        st.session_state["stock_df"],
        burn_summary_path=BURN_SUMMARY_PATH,
        z_score=z_score,
        mode_hari=mode_hari,
    )

    # Peringatan transparan sesuai Rubrik Dasbor #4 & AI #1
    if st.session_state["stock_df"]["is_simulated_stock"].any():
        st.info(
            "ℹ️ **Label Data Simulasi:** Saldo awal gudang saat ini menggunakan **simulasi kebutuhan historis "
            "(menunggu data stok fisik awal dari Owner)**, sedangkan *Daily Burn Rate* & *Safety Stock* dihitung "
            "langsung dari **data primer transaksi NutaCloud** (cakupan resep 2018 = 59,0% porsi)."
        )

    # KPI Ringkas
    kritis_cnt = int((health_df["status_stok"] == "KRITIS").sum())
    menipis_cnt = int((health_df["status_stok"] == "MENIPIS").sum())
    aman_cnt = int((health_df["status_stok"] == "AMAN").sum())
    nonaktif_cnt = int((health_df["status_stok"] == "TIDAK_AKTIF").sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 Stok KRITIS", f"{kritis_cnt} bahan")
    c2.metric("🟡 Stok MENIPIS", f"{menipis_cnt} bahan")
    c3.metric("🟢 Stok AMAN", f"{aman_cnt} bahan")
    c4.metric("⚪ Tidak Aktif di BoM Penjualan", f"{nonaktif_cnt} bahan")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Monitoring Stok & Alert",
        "🧾 Upload NutaCloud / Simulasi BoM",
        "📦 Barang Masuk & Opname Malam",
        "📈 Analisis Burn Rate Historis",
    ])

    # TAB 1: Monitoring Stok & Filter
    with tab1:
        st.subheader("Status Persediaan & Ambang Batas Kritis (Safety Stock / DOI)")
        col_f1, col_f2, col_f3 = st.columns(3)
        selected_status = col_f1.multiselect(
            "Filter Status",
            options=["KRITIS", "MENIPIS", "AMAN", "TIDAK_AKTIF"],
            default=["KRITIS", "MENIPIS", "AMAN"],
        )
        vendors = sorted(health_df["kategori_vendor"].dropna().unique().tolist())
        selected_vendor = col_f2.multiselect("Filter Supplier/Kategori", options=vendors, default=vendors)
        search_q = col_f3.text_input("Cari Nama Bahan Baku", "")

        filtered = health_df[
            health_df["status_stok"].isin(selected_status)
            & health_df["kategori_vendor"].isin(selected_vendor)
        ]
        if search_q.strip():
            filtered = filtered[filtered["nama_bahan"].str.contains(search_q.strip(), case=False, na=False)]

        display_cols = [
            "status_stok",
            "nama_bahan",
            "kategori_vendor",
            "stok_saat_ini",
            "satuan_dasar",
            "daily_burn_rate",
            "safety_stock",
            "reorder_point",
            "days_of_inventory",
            "saran_beli_kemasan",
            "estimasi_biaya_beli",
            "data_label",
        ]
        st.dataframe(filtered[display_cols], hide_index=True)

        restock_need = filtered[filtered["saran_beli_kemasan"] > 0]
        if not restock_need.empty:
            st.warning(
                f"🛒 **Rekomendasi Belanja Minimum (Berdasarkan ROP):** "
                f"Ada **{len(restock_need)}** bahan perlu dibeli dengan estimasi modal "
                f"**Rp {restock_need['estimasi_biaya_beli'].sum():,.0f}**."
            )

    # TAB 2: Upload File NutaCloud / Simulasi Potong Stok
    with tab2:
        st.subheader("Otomatisasi Konversi Penjualan NutaCloud ke Pengurangan Stok (BoM)")
        col_up, col_sim = st.columns(2)

        with col_up:
            st.markdown("#### 1. Unggah Rekap Laporan CSV NutaCloud")
            uploaded = st.file_uploader(
                "Pilih file CSV laporan kasir NutaCloud (mentah atau bersih)", type=["csv"]
            )
            if uploaded is not None:
                try:
                    parsed_df = engine.parse_nutacloud_csv(uploaded)
                    st.write(f"Terbaca **{len(parsed_df):,}** baris item produk (`Qty`: {parsed_df['qty'].sum():,.0f}).")
                    if st.button("⚡ Potong Stok dari File CSV Ini"):
                        res = engine.deduct_from_sales(
                            parsed_df, st.session_state["stock_df"], buffer_waste_pct=buffer_waste
                        )
                        st.session_state["stock_df"] = res.updated_stock_df
                        st.session_state["mutation_logs"].append(
                            f"Upload CSV ({uploaded.name}): {res.total_portions_processed:,.0f} porsi terkonversi, "
                            f"{len(res.deductions_df)} bahan terpotong."
                        )
                        st.success(
                            f"Berhasil memotong **{len(res.deductions_df)}** bahan baku dari "
                            f"**{res.total_portions_processed:,.0f}** porsi menu!"
                        )
                        if res.unmapped_items:
                            st.warning(
                                f"Ada {res.total_portions_unmapped:,.0f} porsi belum punya resep "
                                f"({len(res.unmapped_items)} item unik)."
                            )
                        st.dataframe(res.deductions_df.head(20), hide_index=True)
                except Exception as exc:
                    st.error(f"Gagal memproses CSV: {exc}")

        with col_sim:
            st.markdown("#### 2. Simulasi Input Pesanan Menu Manual")
            sellable_names = sorted(engine.kasir_lookup.keys())
            menu_choice = st.selectbox(
                "Pilih Nama Menu Kasir (yang sudah punya resep)",
                options=[m.title() for m in sellable_names if engine.kasir_lookup[m][0] is not None],
            )
            order_qty = st.number_input("Jumlah Porsi Terjual", min_value=1, max_value=500, value=5)
            if st.button("🍜 Simulasikan Pemotongan Stok Menu"):
                res = engine.deduct_from_sales(
                    [{"nama_item": menu_choice, "qty": order_qty}],
                    st.session_state["stock_df"],
                    buffer_waste_pct=buffer_waste,
                )
                st.session_state["stock_df"] = res.updated_stock_df
                st.session_state["mutation_logs"].append(
                    f"Order Manual: {order_qty}x {menu_choice} (buffer {buffer_waste*100:.0f}%)"
                )
                st.success(f"Stok dipotong untuk {order_qty}x {menu_choice}!")
                st.dataframe(res.deductions_df, hide_index=True)

        if st.session_state["mutation_logs"]:
            st.markdown("#### 📜 Riwayat Simulasi Pemotongan Sesi Ini")
            for log in reversed(st.session_state["mutation_logs"][-10:]):
                st.write(f"- {log}")

    # TAB 3: Barang Masuk & Opname Malam
    with tab3:
        col_in, col_op = st.columns(2)
        ing_options = dict(
            zip(st.session_state["stock_df"]["nama_bahan"], st.session_state["stock_df"]["id_bahan"])
        )

        with col_in:
            st.subheader("📥 Input Pembelian Bahan (Per Kemasan)")
            with st.form("form_stock_in"):
                chosen_in = st.selectbox("Pilih Bahan Baku", options=sorted(ing_options.keys()), key="in_ing")
                packs = st.number_input("Jumlah Kemasan Beli", min_value=0.5, max_value=100.0, value=1.0, step=0.5)
                submit_in = st.form_submit_button("Tambah ke Stok")
                if submit_in:
                    upd, info = engine.apply_stock_in(
                        st.session_state["stock_df"], ing_options[chosen_in], packs
                    )
                    st.session_state["stock_df"] = upd
                    st.success(
                        f"Ditambahkan +{info['added_base_qty']:,.2f} {info['satuan_dasar']} "
                        f"untuk {info['nama_bahan']} (Stok kini: {info['stok_sesudah']:,.2f})."
                    )

        with col_op:
            st.subheader("📋 Validasi Fisik Gudang (*Stock Opname* Malam)")
            with st.form("form_opname"):
                chosen_op = st.selectbox("Pilih Bahan untuk Opname", options=sorted(ing_options.keys()), key="op_ing")
                iid_op = ing_options[chosen_op]
                cur_row = st.session_state["stock_df"][st.session_state["stock_df"]["id_bahan"] == iid_op].iloc[0]
                st.caption(f"Stok Tercatat di Sistem: **{cur_row['stok_saat_ini']:,.2f} {cur_row['satuan_dasar']}**")
                actual_val = st.number_input(
                    f"Hasil Hitung Fisik Gudang ({cur_row['satuan_dasar']})",
                    min_value=0.0,
                    value=float(cur_row["stok_saat_ini"]),
                )
                submit_op = st.form_submit_button("Simpan Hasil Opname")
                if submit_op:
                    upd, var_df = engine.apply_stock_opname(
                        st.session_state["stock_df"], {iid_op: actual_val}
                    )
                    st.session_state["stock_df"] = upd
                    st.success("Stok aktual berhasil diperbarui!")
                    st.dataframe(var_df, hide_index=True)

    # TAB 4: Analisis Historis
    with tab4:
        st.subheader("Pola Pemakaian Bahan Baku Historis (Data Primer 396 Hari)")
        hist_df = load_historical_usage()
        if not hist_df.empty:
            active_names = sorted(
                hist_df.groupby("nama_bahan")["total_pemakaian"].sum().loc[lambda s: s > 0].index.tolist()
            )
            chosen_hist = st.selectbox("Pilih Bahan untuk Lihat Tren Harian", options=active_names)
            sub_hist = hist_df[hist_df["nama_bahan"] == chosen_hist].copy()
            sub_hist["tanggal"] = pd.to_datetime(sub_hist["tanggal"])
            unit_lbl = sub_hist["satuan_dasar"].iloc[0]

            c_a, c_b = st.columns([2, 1])
            with c_a:
                st.markdown(f"**Tren Pemakaian Harian `{chosen_hist}` ({unit_lbl})**")
                st.line_chart(sub_hist.set_index("tanggal")["total_pemakaian"])
            with c_b:
                st.markdown("**Rata-Rata Weekday vs Weekend**")
                wk_comp = (
                    sub_hist[sub_hist["is_store_closed"] == 0]
                    .groupby("is_weekend")["total_pemakaian"]
                    .mean()
                    .rename(index={0: "Weekday (Sen-Kam)", 1: "Weekend (Jum-Min)"})
                )
                st.bar_chart(wk_comp)
        else:
            st.warning("Dataset `daily_usage_full_features.csv` belum ditemukan.")


if __name__ == "__main__":
    main()
