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
    selected = "🏠 Home"  # Default: hanya halaman Home tampil

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
        # Jangan set selected, biarkan user pilih menu
        st.experimental_rerun()  # reload tampilan supaya sidebar muncul
