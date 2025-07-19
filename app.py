import streamlit as st
from streamlit_option_menu import option_menu
from pages import (
    reaksi_kimia,
    stoikiometry,
    konsentrasi,
    ph_poh,
    tabel_periodik,
    konversi_satuan,
    regresi_linier
)

# Atur halaman
st.set_page_config(
    page_title="Techmicals",
    page_icon="⚗",
    layout="wide",
)

# Load style
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    menu = option_menu(
        menu_title="🌟 Kebutuhan Kimia",
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
        default_index=0
    )

# Routing
if menu == "🏠 Home":
    import home
    home.show()

elif menu == "📖 About":
    import about
    about.show()

elif menu == "⚗ Reaksi Kimia":
    reaksi_kimia.show()

elif menu == "🧪 Stoikiometri":
    stoikiometry.show()

elif menu == "🧫 Konsentrasi Larutan":
    konsentrasi.show()

elif menu == "💧 pH dan pOH":
    ph_poh.show()

elif menu == "🧬 Tabel Periodik":
    tabel_periodik.show()

elif menu == "🔄 Konversi Satuan":
    konversi_satuan.show()

elif menu == "📈 Regresi Linier":
    regresi_linier.show()
