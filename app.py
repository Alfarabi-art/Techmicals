import streamlit as st
from streamlit_option_menu import option_menu
from utils import (
    fitur_reaksi_kimia, fitur_stoikiometri, fitur_konsentrasi_larutan,
    fitur_ph_poh, fitur_tabel_periodik, fitur_konversi_satuan, fitur_regresi_linier,
    fitur_home, fitur_about
)

# --- LOAD STYLE ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- CONFIGURASI HALAMAN ---
st.set_page_config(page_title="Techmicals", page_icon="⚗", layout="wide")

# --- SIDEBAR MENU ---
menu = option_menu(
    menu_title="🌟 Kebutuhan Kimia",
    options=[
        "🏠 Home", "⚗ Reaksi Kimia", "🧪 Stoikiometri", "🧫 Konsentrasi Larutan",
        "💧 pH dan pOH", "🧬 Tabel Periodik", "🔄 Konversi Satuan",
        "📈 Regresi Linier", "📖 About"
    ],
    icons=[
        "house", "flask", "calculator", "droplet-half", "thermometer-half",
        "grid-3x3-gap-fill", "repeat", "graph-up", "info-circle"
    ],
    default_index=0
)

# --- FITUR MAP ---
fitur_map = {
    "🏠 Home": fitur_home,
    "⚗ Reaksi Kimia": fitur_reaksi_kimia,
    "🧪 Stoikiometri": fitur_stoikiometri,
    "🧫 Konsentrasi Larutan": fitur_konsentrasi_larutan,
    "💧 pH dan pOH": fitur_ph_poh,
    "🧬 Tabel Periodik": fitur_tabel_periodik,
    "🔄 Konversi Satuan": fitur_konversi_satuan,
    "📈 Regresi Linier": fitur_regresi_linier,
    "📖 About": fitur_about
}

# --- JALANKAN FITUR SESUAI MENU ---
fitur_map.get(menu, fitur_home)()
