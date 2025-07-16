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

# --- KONTEN HALAMAN ---
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
    
    # Tombol untuk membuka sidebar
    if st.button("⚗ Mulai Hitung Sekarang"):
        st.session_state["open_sidebar"] = True
        st.experimental_rerun()

# --- CHECK SIDEBAR STATE ---
if "open_sidebar" in st.session_state and st.session_state["open_sidebar"]:
    # Memaksa pengguna ke sidebar (memilih menu selain Home)
    st.sidebar.success("👈 Pilih fitur dari menu sidebar di sebelah kiri!")
    st.sidebar.info("📌 Sidebar sudah terbuka, silakan pilih menu.")
    st.sidebar.markdown("---")
    st.session_state["open_sidebar"] = False  # Reset supaya tidak looping

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
    category = st.selectbox("Pilih Kategori Konversi", [
        "Mol ↔ Gram",
        "Mol ↔ Partikel",
        "Volume Gas STP (mol ↔ L)",
        "Tekanan (atm, mmHg, kPa)",
        "Energi (J ↔ cal)",
        "Suhu (°C, K, °F)",
        "Volume (mL ↔ L)"
    ])
    value = st.number_input("Masukkan Nilai", value=1.0)

    if category == "Mol ↔ Gram":
        formula = st.text_input("Rumus Kimia (contoh: H2O)")
        direction = st.radio("Konversi", ["Mol → Gram", "Gram → Mol"])
        if st.button("Hitung"):
            try:
                pattern = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
                molar_mass = 0
                for (element, count) in pattern:
                    element_mass = getattr(elements, element).mass
                    count = int(count) if count else 1
                    molar_mass += element_mass * count

                if direction == "Mol → Gram":
                    result = value * molar_mass
                    st.success(f"{value} mol {formula} = {result:.4f} gram")
                else:  # Gram → Mol
                    result = value / molar_mass
                    st.success(f"{value} gram {formula} = {result:.4f} mol")
            except Exception as e:
                st.error(f"⚠ Error: {e}")

    elif category == "Suhu (°C, K, °F)":
        from_unit = st.selectbox("Dari", ["°C", "K", "°F"])
        to_unit = st.selectbox("Ke", ["°C", "K", "°F"])
        if st.button("Konversi Suhu"):
            result = None
            if from_unit == to_unit:
                result = value
            elif from_unit == "°C" and to_unit == "K":
                result = value + 273.15
            elif from_unit == "°C" and to_unit == "°F":
                result = (value * 9/5) + 32
            elif from_unit == "K" and to_unit == "°C":
                result = value - 273.15
            elif from_unit == "K" and to_unit == "°F":
                result = ((value - 273.15) * 9/5) + 32
            elif from_unit == "°F" and to_unit == "°C":
                result = (value - 32) * 5/9
            elif from_unit == "°F" and to_unit == "K":
                result = ((value - 32) * 5/9) + 273.15
            st.success(f"Hasil: {result:.2f} {to_unit}")
