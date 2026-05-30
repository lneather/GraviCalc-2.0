import streamlit as st
import uuid
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="GraviCalc — Gravimetric Analysis",
    page_icon="⚗️",
    layout="wide",
)

# ── All text in both languages ───────────────────────────────────────────────
TEXT = {
    "English": {
        "app_caption": "v1.0.0 · ISO 9001",
        "app_note": "All calculations are performed locally. No data is transmitted.",
        "nav": ["Overview", "Assay / Purity", "Loss on Drying", "Residue on Ignition", "Gravimetric Factor", "History"],
        # Overview
        "overview_title": "Gravimetric Analysis Calculator",
        "overview_sub": "Select a calculation method from the sidebar to begin.",
        "card_assay_title": "Assay / Purity",
        "card_assay_desc": "Calculate percentage purity of a compound from gravimetric data.",
         "card_assay_formula": "Formula: % Purity = (Precipitate Wt × GF × PF / Sample Wt) × 100",
        "card_roi_title": "Residue on Ignition (ROI)",
        "card_roi_desc": "Calculate percentage ash or inorganic residue after ignition.",
        "card_roi_formula": "Formula: % ROI = (Residue Wt / Sample Wt) × 100",
        "card_lod_title": "Loss on Drying (LOD)",
        "card_lod_desc": "Determine percentage moisture or volatile content after drying.",
        "card_lod_formula": "Formula: % LOD = ((Wi − Wd) / (Wi − Wt)) × 100",
        "card_gf_title": "Gravimetric Factor",
        "card_gf_desc": "Calculate or look up standard gravimetric factors for analysis.",
        "card_gf_formula": "Formula: GF = (MW_analyte × n) / MW_precipitate",
        # Assay
        "assay_title": "Assay / Purity",
        "assay_sub": "Calculate percentage purity of a compound.",
        "ref_formula": "REFERENCE FORMULA",
        "assay_table": "| Symbol | Meaning |\n|--------|--------|\n| Wₚ | Precipitate weight (g) |\n| GF | Gravimetric Factor |\n| PF | Purity Factor (default 1) |\n| Wₛ | Sample weight (g) |",
        "label_sample_name": "Sample Name / ID",
        "placeholder_assay": "e.g. Batch #1234",
        "label_sample_wt": "Sample Weight (g)",
        "label_gf": "Gravimetric Factor (GF)",
        "label_ppt_wt": "Precipitate Weight (g)",
        "label_pf": "Purity Factor (PF)",
        "btn_calc_assay": "Calculate Purity",
        "err_name": "Sample name is required.",
        "err_sample_wt": "Sample weight must be greater than zero.",
        "err_ppt_wt": "Precipitate weight must be greater than zero.",
        "err_gf": "Gravimetric factor must be greater than zero.",
        "metric_sample_wt": "Sample Wt",
        "metric_ppt_wt": "Precipitate Wt",
        "metric_result": "Result",
        "btn_save": "Save to History",
        "saved_ok": "Saved to history.",
        # LOD
        "lod_title": "Loss on Drying (LOD)",
        "lod_sub": "Calculate percentage moisture and volatile content.",
        "lod_table": "| Symbol | Meaning |\n|--------|--------|\n| Wᵢ | Initial weight (g) |\n| W_d | Dried weight (g) |\n| W_t | Tare weight (g) |",
        "lod_info": "If no container is used, set Tare = 0.",
        "placeholder_lod": "e.g. API Batch #5678",
        "label_initial_wt": "Initial Weight (g)",
        "label_dried_wt": "Dried Weight (g)",
        "label_tare_wt": "Tare Weight (g)",
        "btn_calc_lod": "Calculate LOD",
        "err_initial_wt": "Initial weight must be greater than zero.",
        "err_dried_wt": "Dried weight must be greater than zero.",
        "err_dried_lt_initial": "Dried weight must be less than initial weight.",
        "metric_lod": "% LOD",
        "metric_water_lost": "Water Lost",
        "metric_dry_wt": "Dry Basis Wt",
        # ROI
        "roi_title": "Residue on Ignition (ROI)",
        "roi_sub": "Calculate percentage ash or inorganic residue content.",
        "roi_table": "| Symbol | Meaning |\n|--------|--------|\n| W_f | Final weight (g) |\n| W_t | Crucible tare (g) |\n| Wₛ | Sample weight (g) |",
        "placeholder_roi": "e.g. Excipient Lot #001",
        "label_crucible_tare": "Crucible Tare (g)",
        "label_final_wt": "Final Weight (g)",
        "btn_calc_roi": "Calculate ROI",
        "err_final_lt_tare": "Final weight must be greater than or equal to crucible tare.",
        "metric_residue_wt": "Residue Weight",
        # GF
        "gf_title": "Gravimetric Factor",
        "gf_sub": "Calculate GF and browse common reference values.",
        "gf_calc_sub": "Calculate GF",
        "label_mw_analyte": "MW of Analyte (g/mol)",
        "label_mw_ppt": "MW of Precipitate (g/mol)",
        "label_ratio": "Stoichiometric Ratio (n)",
        "btn_calc_gf": "Calculate GF",
        "err_mw_ppt": "MW of precipitate must be greater than zero.",
        "err_mw_analyte": "MW of analyte must be greater than zero.",
        "metric_gf": "Gravimetric Factor",
        "gf_ref_sub": "Common Reference Values",
        "gf_search": "Search by compound, precipitate, or analyte",
        "gf_search_placeholder": "e.g. BaSO4 or Chloride",
        "col_compound": "Compound",
        "col_precipitate": "Precipitate",
        "col_analyte": "Analyte",
        "gf_compounds": [
            {"Compound": "Sulfate (SO₄²⁻)",  "Precipitate": "BaSO₄",      "Analyte": "SO₃", "GF": 0.3430},
            {"Compound": "Sulfate (SO₄²⁻)",  "Precipitate": "BaSO₄",      "Analyte": "S",   "GF": 0.1374},
            {"Compound": "Chloride (Cl⁻)",   "Precipitate": "AgCl",        "Analyte": "Cl",  "GF": 0.2474},
            {"Compound": "Iron",             "Precipitate": "Fe₂O₃",       "Analyte": "Fe",  "GF": 0.6994},
            {"Compound": "Calcium",          "Precipitate": "CaO",         "Analyte": "Ca",  "GF": 0.7147},
            {"Compound": "Calcium",          "Precipitate": "CaCO₃",       "Analyte": "Ca",  "GF": 0.4004},
            {"Compound": "Magnesium",        "Precipitate": "MgO",         "Analyte": "Mg",  "GF": 0.6031},
            {"Compound": "Phosphorus",       "Precipitate": "Mg₂P₂O₇",    "Analyte": "P",   "GF": 0.2783},
            {"Compound": "Nickel",           "Precipitate": "Ni(DMGH)₂",  "Analyte": "Ni",  "GF": 0.2032},
            {"Compound": "Aluminum",         "Precipitate": "Al₂O₃",       "Analyte": "Al",  "GF": 0.5293},
        ],
        # History
        "history_title": "Calculation History",
        "history_sub": "All calculations saved this session.",
        "history_empty": "No calculations saved yet. Run a calculation and press **Save to History** to record it here.",
        "history_count": "record(s) this session",
        "btn_clear": "Clear All",
        "method_labels": {"Assay": "🔵 Assay", "LOD": "🟢 LOD", "ROI": "🟠 ROI"},
    },
    "Indonesia": {
        "app_caption": "v1.0.0 · ISO 9001",
        "app_note": "Semua perhitungan dilakukan secara lokal. Tidak ada data yang dikirim.",
        "nav": ["Beranda", "Kadar / Kemurnian", "Susut Pengeringan", "Sisa Pemijaran", "Faktor Gravimetri", "Riwayat"],
        # Overview
        "overview_title": "Kalkulator Analisis Gravimetri",
        "overview_sub": "Pilih metode perhitungan dari menu di samping untuk memulai.",
        "card_assay_title": "Kadar / Kemurnian",
        "card_assay_desc": "Hitung persentase kemurnian senyawa dari data gravimetri.",
        "card_assay_formula": "Rumus: % Kadar = (Berat Endapan × GF × PF / Berat Sampel) × 100",
        "card_roi_title": "Sisa Pemijaran (ROI)",
        "card_roi_desc": "Hitung persentase abu atau residu anorganik setelah pemijaran.",
        "card_roi_formula": "Rumus: % ROI = (Berat Residu / Berat Sampel) × 100",
        "card_lod_title": "Susut Pengeringan (LOD)",
        "card_lod_desc": "Tentukan persentase kadar air atau zat mudah menguap setelah pengeringan.",
        "card_lod_formula": "Rumus: % LOD = ((Ba − Bk) / (Ba − Bt)) × 100",
        "card_gf_title": "Faktor Gravimetri",
        "card_gf_desc": "Hitung atau cari faktor gravimetri standar untuk analisis.",
        "card_gf_formula": "Rumus: GF = (BM_analit × n) / BM_endapan",
        # Assay
        "assay_title": "Kadar / Kemurnian",
        "assay_sub": "Hitung persentase kemurnian suatu senyawa.",
        "ref_formula": "RUMUS REFERENSI",
        "assay_table": "| Simbol | Keterangan |\n|--------|------------|\n| Bₑ | Berat endapan (g) |\n| GF | Faktor Gravimetri |\n| PF | Faktor Kemurnian (default 1) |\n| Bₛ | Berat sampel (g) |",
        "label_sample_name": "Nama / ID Sampel",
        "placeholder_assay": "cth. Bets #1234",
        "label_sample_wt": "Berat Sampel (g)",
        "label_gf": "Faktor Gravimetri (GF)",
        "label_ppt_wt": "Berat Endapan (g)",
        "label_pf": "Faktor Kemurnian (PF)",
        "btn_calc_assay": "Hitung Kadar",
        "err_name": "Nama sampel wajib diisi.",
        "err_sample_wt": "Berat sampel harus lebih dari nol.",
        "err_ppt_wt": "Berat endapan harus lebih dari nol.",
        "err_gf": "Faktor gravimetri harus lebih dari nol.",
        "metric_sample_wt": "Berat Sampel",
        "metric_ppt_wt": "Berat Endapan",
        "metric_result": "Hasil",
        "btn_save": "Simpan ke Riwayat",
        "saved_ok": "Berhasil disimpan ke riwayat.",
        # LOD
        "lod_title": "Susut Pengeringan (LOD)",
        "lod_sub": "Hitung persentase kadar air dan zat mudah menguap.",
        "lod_table": "| Simbol | Keterangan |\n|--------|------------|\n| Bₐ | Berat awal (g) |\n| Bₖ | Berat kering (g) |\n| Bₜ | Berat tara (g) |",
        "lod_info": "Jika tidak menggunakan wadah, isi Tara = 0.",
        "placeholder_lod": "cth. Bets API #5678",
        "label_initial_wt": "Berat Awal (g)",
        "label_dried_wt": "Berat Kering (g)",
        "label_tare_wt": "Berat Tara (g)",
        "btn_calc_lod": "Hitung LOD",
        "err_initial_wt": "Berat awal harus lebih dari nol.",
        "err_dried_wt": "Berat kering harus lebih dari nol.",
        "err_dried_lt_initial": "Berat kering harus lebih kecil dari berat awal.",
        "metric_lod": "% LOD",
        "metric_water_lost": "Air yang Hilang",
        "metric_dry_wt": "Berat Kering Netto",
        # ROI
        "roi_title": "Sisa Pemijaran (ROI)",
        "roi_sub": "Hitung persentase abu atau residu anorganik.",
        "roi_table": "| Simbol | Keterangan |\n|--------|------------|\n| Bₐ | Berat akhir (g) |\n| Bₜ | Berat krus kosong (g) |\n| Bₛ | Berat sampel (g) |",
        "placeholder_roi": "cth. Eksipien Lot #001",
        "label_crucible_tare": "Berat Krus Kosong (g)",
        "label_final_wt": "Berat Akhir (g)",
        "btn_calc_roi": "Hitung ROI",
        "err_final_lt_tare": "Berat akhir harus lebih besar atau sama dengan berat krus kosong.",
        "metric_residue_wt": "Berat Residu",
        # GF
        "gf_title": "Faktor Gravimetri",
        "gf_sub": "Hitung GF dan lihat nilai referensi umum.",
        "gf_calc_sub": "Hitung GF",
        "label_mw_analyte": "BM Analit (g/mol)",
        "label_mw_ppt": "BM Endapan (g/mol)",
        "label_ratio": "Rasio Stoikiometri (n)",
        "btn_calc_gf": "Hitung GF",
        "err_mw_ppt": "BM endapan harus lebih dari nol.",
        "err_mw_analyte": "BM analit harus lebih dari nol.",
        "metric_gf": "Faktor Gravimetri",
        "gf_ref_sub": "Nilai Referensi Umum",
        "gf_search": "Cari berdasarkan senyawa, endapan, atau analit",
        "gf_search_placeholder": "cth. BaSO4 atau Klorida",
        "col_compound": "Senyawa",
        "col_precipitate": "Endapan",
        "col_analyte": "Analit",
        "gf_compounds": [
            {"Senyawa": "Sulfat (SO₄²⁻)",  "Endapan": "BaSO₄",      "Analit": "SO₃", "GF": 0.3430},
            {"Senyawa": "Sulfat (SO₄²⁻)",  "Endapan": "BaSO₄",      "Analit": "S",   "GF": 0.1374},
            {"Senyawa": "Klorida (Cl⁻)",   "Endapan": "AgCl",        "Analit": "Cl",  "GF": 0.2474},
            {"Senyawa": "Besi",            "Endapan": "Fe₂O₃",       "Analit": "Fe",  "GF": 0.6994},
        ]}}
# ── Session state for history ────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

def save_to_history(method, sample_name, result, unit, inputs):
    st.session_state.history.insert(0, {
        "id": str(uuid.uuid4())[:8],
        "method": method,
        "sample_name": sample_name,
        "result": result,
        "unit": unit,
        "inputs": inputs,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

# ── Sidebar navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚗ GraviCalc")
    st.caption("v1.0.0 · ISO 9001")
    st.divider()
    page = st.radio(
        "Navigation",
        ["Overview", "Assay / Purity", "Loss on Drying", "Residue on Ignition", "Gravimetric Factor", "History"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("All calculations are performed locally. No data is transmitted.")

# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.title("Gravimetric Analysis Calculator")
    st.markdown("Select a calculation method from the sidebar to begin.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("Assay / Purity")
            st.write("Calculate percentage purity of a compound from gravimetric data.")
            st.caption("Formula: % Purity = (Precipitate Wt × GF × PF / Sample Wt) × 100")

        with st.container(border=True):
            st.subheader("Residue on Ignition (ROI)")
            st.write("Calculate percentage ash or inorganic residue after ignition.")
            st.caption("Formula: % ROI = (Residue Wt / Sample Wt) × 100")

    with col2:
        with st.container(border=True):
            st.subheader("Loss on Drying (LOD)")
            st.write("Determine percentage moisture or volatile content after drying.")
            st.caption("Formula: % LOD = ((Wi − Wd) / (Wi − Wt)) × 100")

        with st.container(border=True):
            st.subheader("Gravimetric Factor")
            st.write("Calculate or look up standard gravimetric factors for analysis.")
            st.caption("Formula: GF = (MW_analyte × n) / MW_precipitate")

# ══════════════════════════════════════════════════════════════════════════════
# ASSAY / PURITY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Assay / Purity":
    st.title("Assay / Purity")
    st.markdown("Calculate percentage purity of a compound.")
    st.divider()

    col_form, col_ref = st.columns([2, 1])

    with col_ref:
        with st.container(border=True):
            st.caption("REFERENCE FORMULA")
            st.latex(r"\%\ Purity = \frac{W_p \times GF \times PF}{W_s} \times 100")
            st.markdown("""
| Symbol | Meaning |
|--------|---------|
| Wₚ | Precipitate weight (g) |
| GF | Gravimetric Factor |
| PF | Purity Factor (default 1) |
| Wₛ | Sample weight (g) |
""")

    with col_form:
        with st.form("assay_form"):
            sample_name = st.text_input("Sample Name / ID", placeholder="e.g. Batch #1234")
            c1, c2 = st.columns(2)
            with c1:
                sample_weight = st.number_input("Sample Weight (g)", min_value=0.0, format="%.4f", step=0.0001)
                gf = st.number_input("Gravimetric Factor", min_value=0.0, format="%.4f", step=0.0001, value=1.0)
            with c2:
                precipitate_weight = st.number_input("Precipitate Weight (g)", min_value=0.0, format="%.4f", step=0.0001)
                purity_factor = st.number_input("Purity Factor", min_value=0.0, format="%.4f", step=0.0001, value=1.0)
            submitted = st.form_submit_button("Calculate Purity", use_container_width=True, type="primary")

        if submitted:
            errors = []
            if not sample_name:
                errors.append("Sample name is required.")
            if sample_weight <= 0:
                errors.append("Sample weight must be greater than zero.")
            if precipitate_weight <= 0:
                errors.append("Precipitate weight must be greater than zero.")
            if gf <= 0:
                errors.append("Gravimetric factor must be greater than zero.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                purity = (precipitate_weight * gf * purity_factor / sample_weight) * 100
                st.success(f"**% Purity = {purity:.4g} %**")

                with st.container(border=True):
                    st.markdown(f"**Sample:** {sample_name}")
                    r1, r2, r3 = st.columns(3)
                    r1.metric("Sample Wt", f"{sample_weight:.4f} g")
                    r2.metric("Precipitate Wt", f"{precipitate_weight:.4f} g")
                    r3.metric("Result", f"{purity:.4g} %")

                    if st.button("Save to History", key="assay_save"):
                        save_to_history(
                            "Assay", sample_name, purity, "%",
                            {"Sample Wt (g)": sample_weight, "Precipitate Wt (g)": precipitate_weight, "GF": gf, "Purity Factor": purity_factor}
                        )
                        st.success("Saved to history.")

# ══════════════════════════════════════════════════════════════════════════════
# LOSS ON DRYING
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Loss on Drying":
    st.title("Loss on Drying (LOD)")
    st.markdown("Calculate percentage moisture and volatile content.")
    st.divider()

    col_form, col_ref = st.columns([2, 1])

    with col_ref:
        with st.container(border=True):
            st.caption("REFERENCE FORMULA")
            st.latex(r"\%\ LOD = \frac{W_i - W_d}{W_i - W_t} \times 100")
            st.markdown("""
| Symbol | Meaning |
|--------|---------|
| Wᵢ | Initial weight (g) |
| W_d | Dried weight (g) |
| W_t | Tare weight (g) |
""")
            st.info("If no container is used, set Tare = 0.")

    with col_form:
        with st.form("lod_form"):
            sample_name = st.text_input("Sample Name / ID", placeholder="e.g. API Batch #5678")
            c1, c2, c3 = st.columns(3)
            with c1:
                initial_weight = st.number_input("Initial Weight (g)", min_value=0.0, format="%.4f", step=0.0001)
            with c2:
                dried_weight = st.number_input("Dried Weight (g)", min_value=0.0, format="%.4f", step=0.0001)
            with c3:
                tare_weight = st.number_input("Tare Weight (g)", min_value=0.0, format="%.4f", step=0.0001, value=0.0)
            submitted = st.form_submit_button("Calculate LOD", use_container_width=True, type="primary")

        if submitted:
            errors = []
            if not sample_name:
                errors.append("Sample name is required.")
            if initial_weight <= 0:
                errors.append("Initial weight must be greater than zero.")
            if dried_weight <= 0:
                errors.append("Dried weight must be greater than zero.")
            if dried_weight >= initial_weight:
                errors.append("Dried weight must be less than initial weight.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                net_initial = initial_weight - tare_weight
                water_lost = initial_weight - dried_weight
                dry_weight = dried_weight - tare_weight
                lod = (water_lost / net_initial) * 100

                st.success(f"**% LOD = {lod:.4g} %**")

                with st.container(border=True):
                    st.markdown(f"**Sample:** {sample_name}")
                    r1, r2, r3 = st.columns(3)
                    r1.metric("% LOD", f"{lod:.4g} %")
                    r2.metric("Water Lost", f"{water_lost:.4f} g")
                    r3.metric("Dry Basis Wt", f"{dry_weight:.4f} g")

                    if st.button("Save to History", key="lod_save"):
                        save_to_history(
                            "LOD", sample_name, lod, "%",
                            {"Initial Wt (g)": initial_weight, "Dried Wt (g)": dried_weight, "Tare Wt (g)": tare_weight}
                        )
                        st.success("Saved to history.")

# ══════════════════════════════════════════════════════════════════════════════
# RESIDUE ON IGNITION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Residue on Ignition":
    st.title("Residue on Ignition (ROI)")
    st.markdown("Calculate percentage ash or inorganic residue content.")
    st.divider()

    col_form, col_ref = st.columns([2, 1])

    with col_ref:
        with st.container(border=True):
            st.caption("REFERENCE FORMULA")
            st.latex(r"\%\ ROI = \frac{W_f - W_t}{W_s} \times 100")
            st.markdown("""
| Symbol | Meaning |
|--------|---------|
| W_f | Final weight (g) |
| W_t | Crucible tare (g) |
| Wₛ | Sample weight (g) |
""")

    with col_form:
        with st.form("roi_form"):
            sample_name = st.text_input("Sample Name / ID", placeholder="e.g. Excipient Lot #001")
            c1, c2, c3 = st.columns(3)
            with c1:
                sample_weight = st.number_input("Sample Weight (g)", min_value=0.0, format="%.4f", step=0.0001)
            with c2:
                crucible_tare = st.number_input("Crucible Tare (g)", min_value=0.0, format="%.4f", step=0.0001)
            with c3:
                final_weight = st.number_input("Final Weight (g)", min_value=0.0, format="%.4f", step=0.0001)
            submitted = st.form_submit_button("Calculate ROI", use_container_width=True, type="primary")

        if submitted:
            errors = []
            if not sample_name:
                errors.append("Sample name is required.")
            if sample_weight <= 0:
                errors.append("Sample weight must be greater than zero.")
            if final_weight < crucible_tare:
                errors.append("Final weight must be greater than or equal to crucible tare.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                residue_weight = final_weight - crucible_tare
                roi = (residue_weight / sample_weight) * 100

                st.success(f"**% ROI = {roi:.4g} %**")

                with st.container(border=True):
                    st.markdown(f"**Sample:** {sample_name}")
                    r1, r2 = st.columns(2)
                    r1.metric("% ROI", f"{roi:.4g} %")
                    r2.metric("Residue Weight", f"{residue_weight:.4f} g")

                    if st.button("Save to History", key="roi_save"):
                        save_to_history(
                            "ROI", sample_name, roi, "%",
                            {"Sample Wt (g)": sample_weight, "Crucible Tare (g)": crucible_tare, "Final Wt (g)": final_weight}
                        )
                        st.success("Saved to history.")

# ══════════════════════════════════════════════════════════════════════════════
# GRAVIMETRIC FACTOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Gravimetric Factor":
    st.title("Gravimetric Factor")
    st.markdown("Calculate GF and browse common reference values.")
    st.divider()

    col_calc, col_table = st.columns([1, 1])

    with col_calc:
        with st.container(border=True):
            st.subheader("Calculate GF")
            with st.form("gf_form"):
                mw_analyte = st.number_input("MW of Analyte (g/mol)", min_value=0.0, format="%.4f", step=0.001)
                mw_precipitate = st.number_input("MW of Precipitate (g/mol)", min_value=0.0, format="%.4f", step=0.001)
                ratio = st.number_input("Stoichiometric Ratio (n)", min_value=0.0, format="%.4f", step=0.001, value=1.0)
                submitted = st.form_submit_button("Calculate GF", use_container_width=True, type="primary")

            if submitted:
                if mw_precipitate <= 0:
                    st.error("MW of precipitate must be greater than zero.")
                elif mw_analyte <= 0:
                    st.error("MW of analyte must be greater than zero.")
                else:
                    gf = (mw_analyte * ratio) / mw_precipitate
                    st.metric("Gravimetric Factor", f"{gf:.4f}")
                    st.latex(r"GF = \frac{MW_{analyte} \times n}{MW_{precipitate}}")

    with col_table:
        st.subheader("Common Reference Values")
        search = st.text_input("Search by compound, precipitate, or analyte", placeholder="e.g. BaSO4 or Chloride")

        common_factors = [
            {"Compound": "Sulfate (SO₄²⁻)", "Precipitate": "BaSO₄", "Analyte": "SO₃", "GF": 0.3430},
            {"Compound": "Sulfate (SO₄²⁻)", "Precipitate": "BaSO₄", "Analyte": "S",   "GF": 0.1374},
            {"Compound": "Chloride (Cl⁻)",   "Precipitate": "AgCl",  "Analyte": "Cl",  "GF": 0.2474},
            {"Compound": "Iron",              "Precipitate": "Fe₂O₃", "Analyte": "Fe",  "GF": 0.6994},
            {"Compound": "Calcium",           "Precipitate": "CaO",   "Analyte": "Ca",  "GF": 0.7147},
            {"Compound": "Calcium",           "Precipitate": "CaCO₃", "Analyte": "Ca",  "GF": 0.4004},
            {"Compound": "Magnesium",         "Precipitate": "MgO",   "Analyte": "Mg",  "GF": 0.6031},
            {"Compound": "Phosphorus",        "Precipitate": "Mg₂P₂O₇", "Analyte": "P","GF": 0.2783},
            {"Compound": "Nickel",            "Precipitate": "Ni(DMGH)₂", "Analyte": "Ni", "GF": 0.2032},
            {"Compound": "Aluminum",          "Precipitate": "Al₂O₃", "Analyte": "Al",  "GF": 0.5293},
        ]

        if search:
            s = search.lower()
            common_factors = [
                r for r in common_factors
                if s in r["Compound"].lower() or s in r["Precipitate"].lower() or s in r["Analyte"].lower()
            ]

        import pandas as pd
        df = pd.DataFrame(common_factors)
        if not df.empty:
            df["GF"] = df["GF"].apply(lambda x: f"{x:.4f}")
        st.dataframe(df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# HISTORY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "History":
    st.title("Calculation History")
    st.markdown("All calculations saved this session.")
    st.divider()

    if not st.session_state.history:
        st.info("No calculations saved yet. Run a calculation and press **Save to History** to record it here.")
    else:
        col_head, col_btn = st.columns([4, 1])
        with col_head:
            st.caption(f"{len(st.session_state.history)} record(s) this session")
        with col_btn:
            if st.button("Clear All", type="secondary"):
                st.session_state.history = []
                st.rerun()

        METHOD_COLORS = {"Assay": "🔵", "LOD": "🟢", "ROI": "🟠"}

        for entry in st.session_state.history:
            icon = METHOD_COLORS.get(entry["method"], "⚪")
            with st.expander(f"{icon} **{entry['method']}** — {entry['sample_name']}  ·  **{entry['result']:.4g}{entry['unit']}**  ·  {entry['timestamp']}"):
                cols = st.columns(len(entry["inputs"]))
                for col, (k, v) in zip(cols, entry["inputs"].items()):
                    col.metric(k, v)
