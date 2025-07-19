import streamlit as st
from streamlit_option_menu import option_menu

# Import halaman
import home_page as home
import about

from pages import (
    reaksi_kimia,
    stoikiometry,
    konsentrasi,
    ph_poh,
    tabel_periodik,
    konversi_satuan,
    regresi_linier
)

# --- KONFIGURASI HALAMAN UTAMA ---
st.set_page_config(
    page_title="Techmicals",
    page_icon="⚗",
    layout="wide"
)

# --- CUSTOM CSS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- MENU NAVIGASI ---
selected = option_menu(
    menu_title="Techmicals Menu",
    options=[
        "🏠 Home", 
        "⚗ Reaksi Kimia", 
        "🧪 Stoikiometri",
        "🧫 Konsentrasi Larutan", 
        "💧 pH dan pOH",
        "🧬 Tabel Periodik", 
        "🔄 Konversi Satuan",
        "📈 Regresi Linier", 
        "📖 About"
    ],
    icons=[
        "house", "flask", "calculator",
        "droplet-half", "thermometer-half",
        "grid-3x3-gap-fill", "repeat",
        "graph-up", "info-circle"
    ],
    default_index=0,
    orientation="horizontal"
)

# --- LOAD HALAMAN BERDASARKAN MENU ---
if selected == "🏠 Home":
    home.show()
elif selected == "⚗ Reaksi Kimia":
    reaksi_kimia.show()
elif selected == "🧪 Stoikiometri":
    stoikiometry.show()
elif selected == "🧫 Konsentrasi Larutan":
    konsentrasi.show()
elif selected == "💧 pH dan pOH":
    ph_poh.show()
elif selected == "🧬 Tabel Periodik":
    tabel_periodik.show()
elif selected == "🔄 Konversi Satuan":
    konversi_satuan.show()
elif selected == "📈 Regresi Linier":
    regresi_linier.show()
elif selected == "📖 About":
    about.show()
