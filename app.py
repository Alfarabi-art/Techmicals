import streamlit as st
from streamlit_option_menu import option_menu
from chempy import balance_stoichiometry
from periodictable import elements
import re

# --- CONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Techmicals",
    page_icon="⚗",
    layout="wide"
)

# --- FIX: MEMAKSA LIGHT MODE ---
st.markdown("""
    <style>
    /* Memaksa background terang dan teks gelap */
    body, .main, .block-container, .stApp {
        background-color: #f5f5f5 !important;
        color: #000000 !important;
    }
    /* Memperbaiki sidebar */
    .css-1lcbmhc, .css-6qob1r {
        background-color: #ffffff !important;
    }
    .css-1d391kg, .css-18e3th9 {
        background-color: #ffffff !important;
    }
    /* Warna tombol aktif */
    .stButton>button {
        background-color: #1e90ff;
        color: white;
        border-radius: 8px;
        padding: 8px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #00bfff;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    selected = option_menu(
        menu_title="Techmicals",  # Judul menu
        options=["🏠 Home", "⚗ Reaksi Kimia", "🧪 Stoikiometri", "📐 Konversi"],
        icons=["house", "flask", "calculator", "repeat"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#f0f2f6"},
            "icon": {"color": "#1e90ff", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee"
            },
            "nav-link-selected": {
                "background-color": "#1e90ff",
                "color": "white"
            }
        }
    )

# --- KONTEN HALAMAN SESUAI MENU ---
if selected == "🏠 Home":
    st.title("🏠 Selamat Datang di Website Kami")
    st.write("Aplikasi interaktif untuk menghitung reaksi kimia, stoikiometri, dan konversi satuan.")
    st.image(
        "https://images.unsplash.com/photo-1581093588401-5fe04c98b778",
        use_container_width=True
    )

elif selected == "⚗ Reaksi Kimia":
    st.title("⚗ Setarakan Reaksi Kimia")
    equation = st.text_input("Masukkan persamaan reaksi:", "H2 + O2 -> H2O")
    if st.button("Setarakan"):
        try:
            reac, prod = equation.split("->")
            reac_set = set(reac.strip().split('+'))
            prod_set = set(prod.strip().split('+'))
            reac_bal, prod_bal = balance_stoichiometry(reac_set, prod_set)
            balanced_eq = " + ".join(f"{v} {k}" for k, v in reac_bal.items())
            balanced_eq += " → "
            balanced_eq += " + ".join(f"{v} {k}" for k, v in prod_bal.items())
            st.success(f"*Persamaan Setara:* {balanced_eq}")
        except Exception as e:
            st.error(f"⚠ Error: {e}")

elif selected == "🧪 Stoikiometri":
    st.title("🧪 Stoikiometri")
    formula = st.text_input("Rumus Kimia", "H2O")
    mass = st.number_input("Massa (gram)", min_value=0.0)
    if st.button("Hitung"):
        try:
            # Improved regex to correctly parse chemical formulas like H2O, NaCl, C6H12O6.
            # It captures an element symbol (e.g., H, Na, Cl) and an optional digit (subscript).
            # [A-Z][a-z]* matches an uppercase letter followed by zero or more lowercase letters for the symbol.
            # (\d*) matches the optional number (subscript), defaulting to 1 if not present.
            pattern = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
            
            molar_mass = 0.0 # Initialize as float
            
            if not pattern:
                st.error("⚠ Error: Rumus kimia tidak valid atau tidak dapat diuraikan. Pastikan formatnya benar (e.g., H2O, NaCl).")
            else:
                all_elements_valid = True
                for (element_symbol, count_str) in pattern:
                    if not element_symbol: # Skip empty matches if any
                        continue
                    try:
                        # Get element mass from periodictable library
                        element_mass = elements.symbol(element_symbol).mass
                        # Convert count string to integer, default to 1 if empty (no subscript)
                        count = int(count_str) if count_str else 1
                        molar_mass += element_mass * count
                    except Exception:
                        st.error(f"⚠ Error: Simbol elemen '{element_symbol}' tidak dikenal. Pastikan semua simbol elemen benar.")
                        all_elements_valid = False # Mark that an invalid element was found
                        break # Exit loop if an invalid element is found

                if all_elements_valid: # Only proceed if all elements were valid
                    if molar_mass > 0: # Ensure molar_mass is not zero before division
                        moles = mass / molar_mass
                        st.success(f"*Hasil:* {moles:.4f} mol dari {mass} g {formula} (Massa molar: {molar_mass:.2f} g/mol)")
                    else:
                        st.error("⚠ Error: Massa molar tidak dapat dihitung atau bernilai nol. Periksa rumus kimia Anda.")
        except Exception as e:
            st.error(f"⚠ Error umum: Terjadi masalah saat menghitung stoikiometri: {e}")

elif selected == "📐 Konversi":
    st.title("📐 Konversi Suhu")
    temp_value = st.number_input("Masukkan nilai suhu:", value=25.0)
    temp_from = st.selectbox("Dari:", ["C", "K", "F"])
    temp_to = st.selectbox("Ke:", ["C", "K", "F"])
    if st.button("Konversi"):
        result = None
        if temp_from == temp_to:
            result = temp_value
        elif temp_from == "C" and temp_to == "K":
            result = temp_value + 273.15
        elif temp_from == "C" and temp_to == "F":
            result = temp_value * 9/5 + 32
        elif temp_from == "K" and temp_to == "C":
            result = temp_value - 273.15
        elif temp_from == "K" and temp_to == "F":
            result = (temp_value - 273.15) * 9/5 + 32
        elif temp_from == "F" and temp_to == "C":
            result = (temp_value - 32) * 5/9
        elif temp_from == "F" and temp_to == "K":
            result = (temp_value - 32) * 5/9 + 273.15
        st.success(f"Hasil konversi: {result:.2f}°{temp_to}")
