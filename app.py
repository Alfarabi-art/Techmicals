import streamlit as st
from streamlit_option_menu import option_menu

# Import semua halaman
from home import show_home
from about import show_about

# Import semua fitur dari folder pages
from pages import (
    reaksi_kimia,
    stoikiometri,
    konsentrasi,
    ph_poh,
    tabel_periodik,
    konversi_satuan,
    regresi_linier
)

# --- CONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Techmicals",
    page_icon="⚗",
    layout="wide",
)

# --- LOAD CUSTOM STYLE ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- SIDEBAR MENU ---
menu = option_menu(
    menu_title="🌟 Menu Utama",
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
        "house", "flask", "calculator", "droplet-half",
        "thermometer-half", "grid-3x3-gap-fill",
        "repeat", "graph-up", "info-circle"
    ],
    default_index=0,
    orientation="vertical",
)

# --- LOGIC UNTUK MEMANGGIL HALAMAN ---
if menu == "🏠 Home":
    show_home()
elif menu == "⚗ Reaksi Kimia":
    reaksi_kimia.show_reaksi_kimia()
elif menu == "🧪 Stoikiometri":
    stoikiometri.show_stoikiometri()
elif menu == "🧫 Konsentrasi Larutan":
    konsentrasi.show_konsentrasi()
elif menu == "💧 pH dan pOH":
    ph_poh.show_ph_poh()
elif menu == "🧬 Tabel Periodik":
    tabel_periodik.show_tabel_periodik()
elif menu == "🔄 Konversi Satuan":
    konversi_satuan.show_konversi_satuan()
elif menu == "📈 Regresi Linier":
    regresi_linier.show_regresi_linier()
elif menu == "📖 About":
    show_about()

# --- FOOTER ---
st.markdown("<footer style='text-align:center; color:#555; margin-top: 40px;'>© 2025 Techmicals by Kelompok 10 | All rights reserved.</footer>", unsafe_allow_html=True)
