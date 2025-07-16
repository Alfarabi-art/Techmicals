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

# --- FIX: TEMA MODERN DAN LIGHT MODE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #ffffff) !important;
        color: #000000 !important;
    }

    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(8px);
        border-radius: 10px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #1e90ff, #00bfff);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 16px;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #00bfff, #1e90ff);
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    selected = option_menu(
        menu_title="🌟 Kalkulator Kimia",  # Judul menu
        options=[
            "🏠 Home",
            "⚗ Reaksi Kimia",
            "🧪 Stoikiometri",
            "🧫 Konsentrasi Larutan",
            "💧 pH dan pOH",
            "📊 Persentase Yield",
            "🧬 Tabel Periodik"
        ],
        icons=["house", "flask", "calculator", "droplet-half", "thermometer-half", "percent", "grid-3x3-gap-fill"],
        menu_icon="chemistry",
        default_index=0
    )

# --- KONTEN HALAMAN SESUAI MENU ---
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
        selected = "⚗ Reaksi Kimia"  # langsung alihkan ke menu Reaksi Kimia
        st.experimental_rerun()  # ✅ dipanggil sebagai fungsi

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
    st.title("🧪 Kalkulator Massa Molar")
    formula = st.text_input("Rumus Kimia", "H2O")
    mass_input = st.text_input("Massa (gram)", "0.03").replace(",", ".")  # Ganti koma jadi titik
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
                    st.error(f"⚠ Unsur {element} tidak ditemukan dalam tabel periodik.")
                    break
            else:
                if molar_mass == 0:
                    st.error("⚠ Rumus kimia tidak valid.")
                else:
                    moles = mass / molar_mass
                    st.success(f"Hasil: {moles:.4f} mol dari {mass} g {formula} (Massa molar: {molar_mass:.2f} g/mol)")
        except ValueError:
            st.error("⚠ Masukkan massa dalam angka yang valid.")

elif selected == "🧫 Konsentrasi Larutan":
    st.title("🧫 Hitung Konsentrasi Larutan")
    solute_mass = st.number_input("Massa zat terlarut (g)", min_value=0.0)
    volume = st.number_input("Volume larutan (L)", min_value=0.0)
    molar_mass = st.number_input("Massa molar zat (g/mol)", min_value=0.0)
    if st.button("Hitung Konsentrasi"):
        try:
            mol = solute_mass / molar_mass
            molarity = mol / volume
            st.success(f"Molaritas (M): {molarity:.4f} mol/L")
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

elif selected == "📊 Persentase Yield":
    st.title("📊 Hitung Persentase Yield")
    teoritis = st.number_input("Hasil Teoritis (gram)", min_value=0.0)
    aktual = st.number_input("Hasil Aktual (gram)", min_value=0.0)
    if st.button("Hitung Yield"):
        try:
            yield_percent = (aktual / teoritis) * 100
            st.success(f"Persentase Yield: {yield_percent:.2f}%")
        except Exception as e:
            st.error(f"⚠ Error: {e}")

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
