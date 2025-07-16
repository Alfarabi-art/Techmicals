import streamlit as st
from streamlit_option_menu import option_menu
from chempy import balance_stoichiometry
from periodictable import elements
import pandas as pd
import re

# --- CONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kalkulator Kimia Plus",
    page_icon="⚗",
    layout="wide"
)

# --- SESSION STATE UNTUK SIDEBAR & MENU ---
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False
if "menu_selected" not in st.session_state:
    st.session_state.menu_selected = "🏠 Home"

# --- SEMBUNYIKAN SIDEBAR DI AWAL ---
if not st.session_state.show_sidebar:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
if st.session_state.show_sidebar:
    with st.sidebar:
        menu = option_menu(
            menu_title="🌟 Kalkulator Kimia",
            options=[
                "🏠 Home",
                "⚗ Reaksi Kimia",
                "🧪 Stoikiometri",
                "🧫 Konsentrasi Larutan",
                "💧 pH dan pOH",
                "🧬 Tabel Periodik",
                "🔄 Konversi Satuan"
            ],
            icons=[
                "house", "flask", "calculator",
                "droplet-half", "thermometer-half",
                "grid-3x3-gap-fill", "repeat"
            ],
            menu_icon="chemistry",
            default_index=0
        )
        st.session_state.menu_selected = menu

# --- KONTEN HALAMAN ---
selected = st.session_state.menu_selected

if selected == "🏠 Home":
    st.title("🧪 Techmicals – Teman Asik Kimia-mu!")
    st.write("""
        Hai! 👋 Selamat datang di Techmicals, aplikasi kimia seru yang bikin hitung-hitungan jadi lebih gampang.  
        Mau setarakan reaksi? Hitung mol? Cari massa molar? Semua bisa kamu lakukan di sini, cepat dan praktis.  
        🚀 Yuk mulai bereksperimen tanpa ribet!
    """)
    st.image(
        "https://images.unsplash.com/photo-1581093588401-5fe04c98b778",
        use_container_width=True
    )
    if st.button("⚗ Mulai Hitung Sekarang"):
        st.session_state.show_sidebar = True
        st.session_state.menu_selected = "⚗ Reaksi Kimia"
        st.experimental_rerun()

elif selected == "⚗ Reaksi Kimia":
    st.title("⚗ Setarakan Reaksi Kimia")
    equation = st.text_input("Masukkan persamaan reaksi:", "H2 + O2 -> H2O")
    if st.button("Setarakan"):
        if "->" not in equation:
            st.error("⚠ Format reaksi harus mengandung '->'")
        else:
            try:
                reac, prod = equation.split("->")
                reac_set = set(reac.strip().split('+'))
                prod_set = set(prod.strip().split('+'))
                reac_bal, prod_bal = balance_stoichiometry(reac_set, prod_set)
                balanced_eq = " + ".join(f"{v} {k}" for k, v in reac_bal.items())
                balanced_eq += " → "
                balanced_eq += " + ".join(f"{v} {k}" for k, v in prod_bal.items())
                st.success(f"Persamaan Setara: {balanced_eq}")
            except Exception as e:
                st.error(f"⚠ Error: {e}")

elif selected == "🧪 Stoikiometri":
    st.title("🧪 Hitung Mol")
    formula = st.text_input("Rumus Kimia", "H2O")
    mass_input = st.text_input("Massa (gram)", "0.03").replace(",", ".")
    if st.button("Hitung Mol"):
        try:
            mass = float(mass_input)
            pattern = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
            molar_mass = 0
            for (element, count) in pattern:
                try:
                    element_mass = getattr(elements, element).mass
                    count = int(count) if count else 1
                    molar_mass += element_mass * count
                except AttributeError:
                    st.error(f"⚠ Unsur {element} tidak ditemukan.")
                    break
            else:
                if molar_mass == 0:
                    st.error("⚠ Rumus kimia tidak valid.")
                else:
                    moles = mass / molar_mass
                    st.success(f"{moles:.4f} mol dari {mass} g {formula} (Massa molar: {molar_mass:.2f} g/mol)")
        except ValueError:
            st.error("⚠ Masukkan angka yang valid.")

elif selected == "🧫 Konsentrasi Larutan":
    st.title("🧫 Hitung Konsentrasi Larutan")
    metode = st.selectbox("Pilih Metode", ["Molaritas", "Normalitas"])
    with st.form(key="konsentrasi_form"):
        if metode == "Molaritas":
            solute_mass = st.number_input("Massa zat terlarut (g)", min_value=0.0, key="mol_mass")
            volume = st.number_input("Volume larutan (L)", min_value=0.0, key="mol_vol")
            molar_mass = st.number_input("Massa molar zat (g/mol)", min_value=0.0, key="mol_molar_mass")
            hitung = st.form_submit_button("Hitung Molaritas")
            if hitung:
                try:
                    mol = solute_mass / molar_mass
                    molarity = mol / volume
                    st.success(f"Molaritas: {molarity:.4f} mol/L")
                except Exception as e:
                    st.error(f"⚠ Error: {e}")
        elif metode == "Normalitas":
            solute_mass = st.number_input("Massa zat terlarut (g)", min_value=0.0, key="norm_mass")
            eq_weight = st.number_input("Berat ekuivalen (g/eq)", min_value=0.0, key="norm_eq_weight")
            volume = st.number_input("Volume larutan (L)", min_value=0.0, key="norm_vol")
            hitung = st.form_submit_button("Hitung Normalitas")
            if hitung:
                try:
                    eq = solute_mass / eq_weight
                    normality = eq / volume
                    st.success(f"Normalitas: {normality:.4f} eq/L")
                except Exception as e:
                    st.error(f"⚠ Error: {e}")

elif selected == "💧 pH dan pOH":
    st.title("💧 Hitung pH dan pOH")
    conc = st.number_input("Konsentrasi (mol/L)", min_value=0.0, value=0.01)
    acid_base = st.selectbox("Jenis Larutan", ["Asam", "Basa"])
    if st.button("Hitung pH"):
        import math
        if conc > 0:
            if acid_base == "Asam":
                pH = -math.log10(conc)
                pOH = 14 - pH
            else:
                pOH = -math.log10(conc)
                pH = 14 - pOH
            st.success(f"pH: {pH:.2f}, pOH: {pOH:.2f}")
        else:
            st.error("Konsentrasi harus lebih dari 0.")

elif selected == "🧬 Tabel Periodik":
    st.title("🧬 Tabel Periodik Interaktif")
    periodic_data = [{"Symbol": el.symbol, "Name": el.name, "Atomic Number": el.number, "Atomic Mass": el.mass}
                     for el in elements if el.number <= 118]
    df = pd.DataFrame(periodic_data)
    st.dataframe(df, use_container_width=True)
    selected_element = st.selectbox("Pilih Unsur", [el.symbol for el in elements if el.number <= 118])
    if selected_element:
        el = getattr(elements, selected_element)
        st.write(f"{el.name} ({el.symbol})")
        st.write(f"Nomor Atom: {el.number}")
        st.write(f"Massa Atom: {el.mass} g/mol")

elif selected == "🔄 Konversi Satuan":
    st.title("🔄 Konversi Satuan Kimia")
    kategori = st.selectbox(
        "Pilih Kategori",
        [
            "Mol ↔ Gram",
            "Mol ↔ Partikel",
            "Volume Gas (STP)",
            "Tekanan",
            "Suhu",
            "Konsentrasi Larutan"
        ],
        key="konversi_kategori"
    )

    if kategori == "Mol ↔ Gram":
        with st.form(key="mol_gram_form"):
            nilai = st.number_input("Masukkan Nilai", value=1.0, key="mol_gram_nilai")
            molar_mass = st.number_input("Massa molar (g/mol)", value=18.0, key="mol_gram_molar_mass")
            arah = st.radio("Konversi", ["Mol → Gram", "Gram → Mol"], key="mol_gram_arah")
            hitung = st.form_submit_button("Hitung")
            if hitung:
                if arah == "Mol → Gram":
                    hasil = nilai * molar_mass
                    st.success(f"{hasil:.4f} gram")
                else:
                    hasil = nilai / molar_mass
                    st.success(f"{hasil:.4f} mol")

    elif kategori == "Konsentrasi Larutan":
        with st.form(key="konversi_konsentrasi_form"):
            nilai = st.number_input("Masukkan Nilai", value=1.0, key="konversi_konsentrasi_nilai")
            dari = st.selectbox("Dari", ["Molaritas (M)", "Normalitas (N)"], key="konversi_konsentrasi_dari")
            ke = st.selectbox("Ke", ["Normalitas (N)", "Molaritas (M)"], key="konversi_konsentrasi_ke")
            valensi = st.number_input("Valensi", min_value=1, key="konversi_konsentrasi_valensi")
            hitung = st.form_submit_button("Hitung Konsentrasi")
            if hitung:
                if dari == "Molaritas (M)" and ke == "Normalitas (N)":
                    normalitas = nilai * valensi
                    st.success(f"Normalitas: {normalitas:.4f} eq/L")
                elif dari == "Normalitas (N)" and ke == "Molaritas (M)":
                    molaritas = nilai / valensi
                    st.success(f"Molaritas: {molaritas:.4f} mol/L")
                else:
                    st.warning("Konversi ini belum didukung.")
