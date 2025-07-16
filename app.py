import streamlit as st
from streamlit_option_menu import option_menu
from chempy import balance_stoichiometry
from periodictable import elements
import re

# --- CONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="TECHMICALS",
    page_icon="⚗",
    layout="wide"
)

# --- FIX: TEMA MODERN DAN LIGHT MODE ---
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    /* Font global */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Background aplikasi */
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #ffffff) !important;
        color: #000000 !important;
    }

    /* Sidebar transparan dengan efek glass */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(8px);
        border-radius: 10px;
    }

    /* Tombol menu aktif */
    .css-1d391kg, .css-18e3th9 {
        background-color: rgba(30, 144, 255, 0.1) !important;
        border-radius: 8px;
    }

    /* Tombol interaktif */
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

    /* Menu hover effect */
    .css-1lcbmhc a:hover {
        background-color: rgba(0, 191, 255, 0.2) !important;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    selected = option_menu(
        menu_title="🌟 TECHMICALS",  # Judul menu
        options=["🏠 Home", "⚗ Reaksi Kimia", "🧪 Stoikiometri", "📐 Konversi"],
        icons=["house", "flask", "calculator", "repeat"],
        menu_icon="chemistry",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "transparent"},
            "icon": {"color": "#1e90ff", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "2px",
                "transition": "all 0.3s ease-in-out"
            },
            "nav-link-selected": {
                "background-color": "#1e90ff",
                "color": "white",
                "border-radius": "8px",
                "box-shadow": "0 4px 15px rgba(30, 144, 255, 0.4)"
            }
        }
    )

# --- KONTEN HALAMAN SESUAI MENU ---
if selected == "🏠 Home":
    st.title("🏠 Selamat Datang di Website Kami!")
    st.write("✨ Aplikasi interaktif untuk menghitung reaksi kimia, stoikiometri, dan konversi satuan.")
    st.image(
        "https://images.unsplash.com/photo-1581093588401-5fe04c98b778",
        use_container_width=True
    )

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
                st.success(f"*Persamaan Setara:* {balanced_eq}")
            except Exception as e:
                st.error(f"⚠ Error: {e}")

elif selected == "🧪 Stoikiometri":
    st.title("🧪 Stoikiometri")
    formula = st.text_input("Rumus Kimia", "H2O")
    mass = st.number_input("Massa (gram)", min_value=0.0)
    if st.button("Hitung"):
        try:
            pattern = re.findall(r'([A-Z][a-z])(\d)', formula)
            molar_mass = 0
            for (element, count) in pattern:
                element_mass = getattr(elements, element).mass
                count = int(count) if count else 1
                molar_mass += element_mass * count
            if molar_mass == 0:
                st.error("⚠ Rumus kimia tidak valid.")
            else:
                moles = mass / molar_mass
                st.success(f"*Hasil:* {moles:.4f} mol dari {mass} g {formula} (Massa molar: {molar_mass:.2f} g/mol)")
        except Exception as e:
            st.error(f"⚠ Error: {e}")

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
