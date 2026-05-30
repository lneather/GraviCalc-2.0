import streamlit as st
import uuid
from datetime import datetime

st.set_page_config(
    page_title="GraviCalc — Analisis Gravimetri",
    page_icon="⚗",
    layout="wide",
)

if "history" not in st.session_state:
    st.session_state.history = []

def simpan_ke_riwayat(metode, nama_sampel, hasil, satuan, input_data):
    st.session_state.history.insert(0, {
        "id": str(uuid.uuid4())[:8],
        "metode": metode,
        "nama_sampel": nama_sampel,
        "hasil": hasil,
        "satuan": satuan,
        "input_data": input_data,
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

with st.sidebar:
    st.markdown("## ⚗ GraviCalc")
    st.caption("v1.0.0 · ISO 9001")
    st.divider()
    halaman = st.radio(
        "Navigasi",
        ["Beranda", "Kadar / Kemurnian", "Susut Pengeringan", "Sisa Pemijaran", "Faktor Gravimetri", "Riwayat"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Semua perhitungan dilakukan secara lokal. Tidak ada data yang dikirim.")

if halaman == "Beranda":
    st.title("Kalkulator Analisis Gravimetri")
    st.markdown("Pilih metode perhitungan dari menu di samping untuk memulai.")
    st.divider()
    kol1, kol2 = st.columns(2)
    with kol1:
        with st.container(border=True):
            st.subheader("Kadar / Kemurnian")
            st.write("Hitung persentase kemurnian senyawa dari data gravimetri.")
            st.caption("Rumus: % Kadar = (Berat Endapan × GF × PF / Berat Sampel) × 100")
        with st.container(border=True):
            st.subheader("Sisa Pemijaran (ROI)")
            st.write("Hitung persentase abu atau residu anorganik setelah pemijaran.")
            st.caption("Rumus: % ROI = (Berat Residu / Berat Sampel) × 100")
    with kol2:
        with st.container(border=True):
            st.subheader("Susut Pengeringan (LOD)")
            st.write("Tentukan persentase kadar air atau zat mudah menguap setelah pengeringan.")
            st.caption("Rumus: % LOD = ((Ba − Bk) / (Ba − Bt)) × 100")
        with st.container(border=True):
            st.subheader("Faktor Gravimetri")
            st.write("Hitung atau cari faktor gravimetri standar untuk analisis.")
            st.caption("Rumus: GF = (BM_analit × n) / BM_endapan")

elif halaman == "Kadar / Kemurnian":
    st.title("Kadar / Kemurnian")
    st.markdown("Hitung persentase kemurnian suatu senyawa.")
    st.divider()
    kol_form, kol_ref = st.columns([2, 1])
    with kol_ref:
        with st.container(border=True):
            st.caption("RUMUS REFERENSI")
            st.latex(r"\%\ Kadar = \frac{B_e \times GF \times PF}{B_s} \times 100")
            st.markdown("""
| Simbol | Keterangan |
|--------|------------|
| Bₑ | Berat endapan (g) |
| GF | Faktor Gravimetri |
| PF | Faktor Kemurnian (default 1) |
| Bₛ | Berat sampel (g) |
""")
    with kol_form:
        with st.form("form_kadar"):
            nama_sampel = st.text_input("Nama / ID Sampel", placeholder="cth. Bets #1234")
            k1, k2 = st.columns(2)
            with k1:
                berat_sampel = st.number_input("Berat Sampel (g)", min_value=0.0, format="%.4f", step=0.0001)
                gf = st.number_input("Faktor Gravimetri (GF)", min_value=0.0, format="%.4f", step=0.0001, value=1.0)
            with k2:
                berat_endapan = st.number_input("Berat Endapan (g)", min_value=0.0, format="%.4f", step=0.0001)
                faktor_kemurnian = st.number_input("Faktor Kemurnian (PF)", min_value=0.0, format="%.4f", step=0.0001, value=1.0)
            dikirim = st.form_submit_button("Hitung Kadar", use_container_width=True, type="primary")
        if dikirim:
            kesalahan = []
            if not nama_sampel:
                kesalahan.append("Nama sampel wajib diisi.")
            if berat_sampel <= 0:
                kesalahan.append("Berat sampel harus lebih dari nol.")
            if berat_endapan <= 0:
                kesalahan.append("Berat endapan harus lebih dari nol.")
            if gf <= 0:
                kesalahan.append("Faktor gravimetri harus lebih dari nol.")
            if kesalahan:
                for e in kesalahan:
                    st.error(e)
            else:
                kadar = (berat_endapan * gf * faktor_kemurnian / berat_sampel) * 100
                st.success(f"**% Kadar = {kadar:.4g} %**")
                with st.container(border=True):
                    st.markdown(f"**Sampel:** {nama_sampel}")
                    r1, r2, r3 = st.columns(3)
                    r1.metric("Berat Sampel", f"{berat_sampel:.4f} g")
                    r2.metric("Berat Endapan", f"{berat_endapan:.4f} g")
                    r3.metric("Hasil", f"{kadar:.4g} %")
                    if st.button("Simpan ke Riwayat", key="simpan_kadar"):
                        simpan_ke_riwayat("Kadar", nama_sampel, kadar, "%",
                            {"Berat Sampel (g)": berat_sampel, "Berat Endapan (g)": berat_endapan, "GF": gf, "Faktor Kemurnian": faktor_kemurnian})
                        st.success("Berhasil disimpan ke riwayat.")

elif halaman == "Susut Pengeringan":
    st.title("Susut Pengeringan (LOD)")
    st.markdown("Hitung persentase kadar air dan zat mudah menguap.")
    st.divider()
    kol_form, kol_ref = st.columns([2, 1])
    with kol_ref:
        with st.container(border=True):
            st.caption("RUMUS REFERENSI")
            st.latex(r"\%\ LOD = \frac{B_a - B_k}{B_a - B_t} \times 100")
            st.markdown("""
| Simbol | Keterangan |
|--------|------------|
| Bₐ | Berat awal (g) |
| Bₖ | Berat kering (g) |
| Bₜ | Berat tara (g) |
""")
            st.info("Jika tidak menggunakan wadah, isi Tara = 0.")
    with kol_form:
        with st.form("form_lod"):
            nama_sampel = st.text_input("Nama / ID Sampel", placeholder="cth. Bets API #5678")
            k1, k2, k3 = st.columns(3)
            with k1:
                berat_awal = st.number_input("Berat Awal (g)", min_value=0.0, format="%.4f", step=0.0001)
            with k2:
                berat_kering = st.number_input("Berat Kering (g)", min_value=0.0, format="%.4f", step=0.0001)
            with k3:
                berat_tara = st.number_input("Berat Tara (g)", min_value=0.0, format="%.4f", step=0.0001, value=0.0)
            dikirim = st.form_submit_button("Hitung LOD", use_container_width=True, type="primary")
        if dikirim:
            kesalahan = []
            if not nama_sampel:
                kesalahan.append("Nama sampel wajib diisi.")
            if berat_awal <= 0:
                kesalahan.append("Berat awal harus lebih dari nol.")
            if berat_kering <= 0:
                kesalahan.append("Berat kering harus lebih dari nol.")
            if berat_kering >= berat_awal:
                kesalahan.append("Berat kering harus lebih kecil dari berat awal.")
            if kesalahan:
                for e in kesalahan:
                    st.error(e)
            else:
                berat_awal_netto = berat_awal - berat_tara
                air_hilang = berat_awal - berat_kering
                berat_kering_netto = berat_kering - berat_tara
                lod = (air_hilang / berat_awal_netto) * 100
                st.success(f"**% LOD = {lod:.4g} %**")
                with st.container(border=True):
                    st.markdown(f"**Sampel:** {nama_sampel}")
                    r1, r2, r3 = st.columns(3)
                    r1.metric("% LOD", f"{lod:.4g} %")
                    r2.metric("Air yang Hilang", f"{air_hilang:.4f} g")
                    r3.metric("Berat Kering Netto", f"{berat_kering_netto:.4f} g")
                    if st.button("Simpan ke Riwayat", key="simpan_lod"):
                        simpan_ke_riwayat("LOD", nama_sampel, lod, "%",
                            {"Berat Awal (g)": berat_awal, "Berat Kering (g)": berat_kering, "Berat Tara (g)": berat_tara})
                        st.success("Berhasil disimpan ke riwayat.")

elif halaman == "Sisa Pemijaran":
    st.title("Sisa Pemijaran (ROI)")
    st.markdown("Hitung persentase abu atau residu anorganik.")
    st.divider()
    kol_form, kol_ref = st.columns([2, 1])
    with kol_ref:
        with st.container(border=True):
            st.caption("RUMUS REFERENSI")
            st.latex(r"\%\ ROI = \frac{B_a - B_t}{B_s} \times 100")
            st.markdown("""
| Simbol | Keterangan |
|--------|------------|
| Bₐ | Berat akhir (g) |
| Bₜ | Berat krus kosong (g) |
| Bₛ | Berat sampel (g) |
""")
    with kol_form:
        with st.form("form_roi"):
            nama_sampel = st.text_input("Nama / ID Sampel", placeholder="cth. Eksipien Lot #001")
            k1, k2, k3 = st.columns(3)
            with k1:
                berat_sampel = st.number_input("Berat Sampel (g)", min_value=0.0, format="%.4f", step=0.0001)
            with k2:
                berat_krus = st.number_input("Berat Krus Kosong (g)", min_value=0.0, format="%.4f", step=0.0001)
            with k3:
                berat_akhir = st.number_input("Berat Akhir (g)", min_value=0.0, format="%.4f", step=0.0001)
            dikirim = st.form_submit_button("Hitung ROI", use_container_width=True, type="primary")
        if dikirim:
            kesalahan = []
            if not nama_sampel:
                kesalahan.append("Nama sampel wajib diisi.")
            if berat_sampel <= 0:
                kesalahan.append("Berat sampel harus lebih dari nol.")
            if berat_akhir < berat_krus:
                kesalahan.append("Berat akhir harus lebih besar atau sama dengan berat krus kosong.")
            if kesalahan:
                for e in kesalahan:
                    st.error(e)
            else:
                berat_residu = berat_akhir - berat_krus
                roi = (berat_residu / berat_sampel) * 100
                st.success(f"**% ROI = {roi:.4g} %**")
                with st.container(border=True):
                    st.markdown(f"**Sampel:** {nama_sampel}")
                    r1, r2 = st.columns(2)
                    r1.metric("% ROI", f"{roi:.4g} %")
                    r2.metric("Berat Residu", f"{berat_residu:.4f} g")
                    if st.button("Simpan ke Riwayat", key="simpan_roi"):
                        simpan_ke_riwayat("ROI", nama_sampel, roi, "%",
                            {"Berat Sampel (g)": berat_sampel, "Berat Krus (g)": berat_krus, "Berat Akhir (g)": berat_akhir})
                        st.success("Berhasil disimpan ke riwayat.")

elif halaman == "Faktor Gravimetri":
    st.title("Faktor Gravimetri")
    st.markdown("Hitung GF dan lihat nilai referensi umum.")
    st.divider()
    kol_hitung, kol_tabel = st.columns([1, 1])
    with kol_hitung:
        with st.container(border=True):
            st.subheader("Hitung GF")
            with st.form("form_gf"):
                bm_analit = st.number_input("BM Analit (g/mol)", min_value=0.0, format="%.4f", step=0.001)
                bm_endapan = st.number_input("BM Endapan (g/mol)", min_value=0.0, format="%.4f", step=0.001)
                rasio = st.number_input("Rasio Stoikiometri (n)", min_value=0.0, format="%.4f", step=0.001, value=1.0)
                dikirim = st.form_submit_button("Hitung GF", use_container_width=True, type="primary")
            if dikirim:
                if bm_endapan <= 0:
                    st.error("BM endapan harus lebih dari nol.")
                elif bm_analit <= 0:
                    st.error("BM analit harus lebih dari nol.")
                else:
                    gf = (bm_analit * rasio) / bm_endapan
                    st.metric("Faktor Gravimetri", f"{gf:.4f}")
                    st.latex(r"GF = \frac{BM_{analit} \times n}{BM_{endapan}}")
    with kol_tabel:
        st.subheader("Nilai Referensi Umum")
        cari = st.text_input("Cari berdasarkan senyawa, endapan, atau analit", placeholder="cth. BaSO4 atau Klorida")
        faktor_umum = [
            {"Senyawa": "Sulfat (SO₄²⁻)",  "Endapan": "BaSO₄",     "Analit": "SO₃", "GF": 0.3430},
            {"Senyawa": "Sulfat (SO₄²⁻)",  "Endapan": "BaSO₄",     "Analit": "S",   "GF": 0.1374},
            {"Senyawa": "Klorida (Cl⁻)",   "Endapan": "AgCl",       "Analit": "Cl",  "GF": 0.2474},
            {"Senyawa": "Besi",            "Endapan": "Fe₂O₃",      "Analit": "Fe",  "GF": 0.6994},
            {"Senyawa": "Kalsium",         "Endapan": "CaO",        "Analit": "Ca",  "GF": 0.7147},
            {"Senyawa": "Kalsium",         "Endapan": "CaCO₃",      "Analit": "Ca",  "GF": 0.4004},
            {"Senyawa": "Magnesium",       "Endapan": "MgO",        "Analit": "Mg",  "GF": 0.6031},
            {"Senyawa": "Fosfor",          "Endapan": "Mg₂P₂O₇",   "Analit": "P",   "GF": 0.2783},
            {"Senyawa": "Nikel",           "Endapan": "Ni(DMGH)₂", "Analit": "Ni",  "GF": 0.2032},
            {"Senyawa": "Aluminium",       "Endapan": "Al₂O₃",      "Analit": "Al",  "GF": 0.5293},
        ]
        if cari:
            s = cari.lower()
            faktor_umum = [r for r in faktor_umum if s in r["Senyawa"].lower() or s in r["Endapan"].lower() or s in r["Analit"].lower()]
        import pandas as pd
        df = pd.DataFrame(faktor_umum)
        if not df.empty:
            df["GF"] = df["GF"].apply(lambda x: f"{x:.4f}")
        st.dataframe(df, use_container_width=True, hide_index=True)

elif halaman == "Riwayat":
    st.title("Riwayat Perhitungan")
    st.markdown("Semua perhitungan yang disimpan pada sesi ini.")
    st.divider()
    if not st.session_state.history:
        st.info("Belum ada perhitungan yang disimpan. Lakukan perhitungan lalu tekan **Simpan ke Riwayat**.")
    else:
        kol_info, kol_tombol = st.columns([4, 1])
        with kol_info:
            st.caption(f"{len(st.session_state.history)} data tersimpan pada sesi ini")
        with kol_tombol:
            if st.button("Hapus Semua", type="secondary"):
                st.session_state.history = []
                st.rerun()
        WARNA_METODE = {"Kadar": "🔵", "LOD": "🟢", "ROI": "🟠"}
        for entri in st.session_state.history:
            ikon = WARNA_METODE.get(entri["metode"], "⚪")
            with st.expander(f"{ikon} **{entri['metode']}** — {entri['nama_sampel']}  ·  **{entri['hasil']:.4g}{entri['satuan']}**  ·  {entri['waktu']}"):
                kols = st.columns(len(entri["input_data"]))
                for kol, (k, v) in zip(kols, entri["input_data"].items()):
                    kol.metric(k, v)
