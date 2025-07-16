import streamlit as st
from streamlit_option_menu import option_menu
from chempy import balance_stoichiometry
from periodictable import elements
import pandas as pd
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kalkulator Kimia Plus",
    page_icon="⚗",
    layout="wide"
)

# --- SESSION STATE UNTUK SIDEBAR ---
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False  # default: sidebar tersembunyi

# --- CSS UNTUK SEMBUNYIKAN SIDEBAR ---
if not st.session_state.show_sidebar:
    hide_sidebar = """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION (akan muncul jika tombol ditekan) ---
if st.session_state.show_sidebar:
    with st.sidebar:
        selected = option_menu(
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
else:
    selected = "🏠 Home"

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
    if st.button("⚗ Mulai Hitung Sekarang"):
        st.session_state.show_sidebar = True  # aktifkan sidebar
        selected = "⚗ Reaksi Kimia"  # langsung arahkan ke fitur pertama

# --- HALAMAN-HALAMAN ---
if selected == "⚗ Reaksi Kimia":
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
    st.info("Fitur konversi akan dihitung setelah kamu pilih kategori dan tekan tombol.")
