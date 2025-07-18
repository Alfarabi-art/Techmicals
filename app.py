import streamlit as st
from streamlit_option_menu import option_menu
from chempy import balance_stoichiometry
from periodictable import elements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import math
from sklearn.linear_model import LinearRegression
from io import BytesIO

# --- CONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Techmicals",
    page_icon="⚗",
    layout="wide"
)

# --- CUSTOM STYLE (GRADIENT BACKGROUND + FONT) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #d1f2eb, #fef9e7, #fde2e4, #e0f7fa);
        background-size: 400% 400%;
        animation: gradientFlow 15s ease infinite;
        color: #000000 !important;
    }

    @keyframes gradientFlow {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(6px);
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

# --- SESSION STATE ---
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False
if "menu_selected" not in st.session_state:
    st.session_state.menu_selected = "🏠 Home"

# --- SEMBUNYIKAN SIDEBAR DI AWAL ---
if not st.session_state.show_sidebar:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR MENU ---
if st.session_state.show_sidebar:
    with st.sidebar:
        menu = option_menu(
            menu_title="🌟 Kalkulator Kimia",
            options=[
                "🏠 Home",
                "⚗ Reaksi Kimia",
                "🧪 Stoikiometri",
                "🧫 Konsentrasi Larutan",
                "💧 pH dan pOH",
                "🧬 Tabel Periodik",
                "🔄 Konversi Satuan",
                "📈 Regresi Linier"
            ],
            icons=[
                "house", "flask", "calculator",
                "droplet-half", "thermometer-half",
                "grid-3x3-gap-fill", "repeat", "graph-up"
            ],
            menu_icon="chemistry",
            default_index=0
        )
        st.session_state.menu_selected = menu

# --- KONTEN HALAMAN UTAMA ---
selected = st.session_state.menu_selected

if selected == "🏠 Home":
    st.title("🧪 Techmicals – Teman Asik Kimia-mu!")
    st.write("""
        Hai! 👋 Selamat datang di *Techmicals*, aplikasi kimia seru yang bikin hitung-hitungan jadi lebih gampang.  
        Mau setarakan reaksi? Hitung mol? Cari massa molar? Semua bisa kamu lakukan di sini, cepat dan praktis.  
        🚀 Yuk mulai bereksperimen tanpa ribet!
    """)
    st.image(
        "https://images.unsplash.com/photo-1581093588401-5fe04c98b778",
        use_container_width=True
    )
    if st.button("⚗ Mulai Hitung Sekarang"):
        st.session_state.show_sidebar = True
        st.session_state.menu_selected = "⚗ Reaksi Kimia"

# --- FITUR REAKSI KIMIA ---
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

# --- FITUR STOIKIOMETRI ---
elif selected == "🧪 Stoikiometri":
    st.title("🧪 Hitung Mol")
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
                    st.error(f"⚠ Unsur {element} tidak ditemukan.")
                    break
            else:
                if molar_mass == 0:
                    st.error("⚠ Rumus kimia tidak valid.")
                else:
                    moles = mass / molar_mass
                    st.success(f"{moles:.4f} mol dari {mass} g {formula} (Massa molar: {molar_mass:.2f} g/mol)")
        except ValueError:
            st.error("⚠ Masukkan angka yang valid.")

# --- FITUR KONSENTRASI LARUTAN ---
elif selected == "🧫 Konsentrasi Larutan":
    st.title("🧫 Hitung Konsentrasi Larutan")
    metode = st.selectbox("Pilih Metode", ["Molaritas", "Normalitas"])
    with st.form(key="konsentrasi_form"):
        if metode == "Molaritas":
            solute_mass = st.number_input("Massa zat terlarut (g)", min_value=0.0)
            volume = st.number_input("Volume larutan (L)", min_value=0.0)
            molar_mass = st.number_input("Massa molar zat (g/mol)", min_value=0.0)
            hitung = st.form_submit_button("Hitung Molaritas")
            if hitung:
                mol = solute_mass / molar_mass
                molarity = mol / volume
                st.success(f"Molaritas: {molarity:.4f} mol/L")
        else:
            solute_mass = st.number_input("Massa zat terlarut (g)", min_value=0.0)
            eq_weight = st.number_input("Berat ekuivalen (g/eq)", min_value=0.0)
            volume = st.number_input("Volume larutan (L)", min_value=0.0)
            hitung = st.form_submit_button("Hitung Normalitas")
            if hitung:
                eq = solute_mass / eq_weight
                normality = eq / volume
                st.success(f"Normalitas: {normality:.4f} eq/L")

# --- FITUR pH DAN pOH ---
elif selected == "💧 pH dan pOH":
    st.title("💧 Hitung pH dan pOH")
    conc = st.number_input("Konsentrasi (mol/L)", min_value=0.0, value=0.01)
    acid_base = st.selectbox("Jenis Larutan", ["Asam", "Basa"])
    if st.button("Hitung pH dan pOH"):
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

# --- FITUR TABEL PERIODIK ---
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

# --- FITUR KONVERSI SATUAN ---
elif selected == "🔄 Konversi Satuan":
    st.title("🔄 Konversi Satuan Kimia")
    kategori = st.selectbox("Pilih Kategori", [
        "Mol ↔ Gram",
        "Mol ↔ Partikel",
        "Volume Gas (STP)",
        "Suhu",
        "Tekanan",
        "Konsentrasi Larutan"
    ])

    # --- Mol <-> Gram ---
    if kategori == "Mol ↔ Gram":
        with st.form(key="mol_gram_form"):
            mode = st.radio("Mode", ["Mol → Gram", "Gram → Mol"])
            molar_mass = st.number_input("Massa Molar (g/mol)", value=18.0)
            if mode == "Mol → Gram":
                mol = st.number_input("Jumlah Mol", value=1.0)
                hitung = st.form_submit_button("Hitung Massa")
                if hitung:
                    mass = mol * molar_mass
                    st.success(f"Massa: {mass:.4f} gram")
            else:
                mass = st.number_input("Massa (gram)", value=1.0)
                hitung = st.form_submit_button("Hitung Mol")
                if hitung:
                    mol = mass / molar_mass
                    st.success(f"Mol: {mol:.4f} mol")

    # --- Mol <-> Partikel ---
    elif kategori == "Mol ↔ Partikel":
        with st.form(key="mol_partikel_form"):
            mode = st.radio("Mode", ["Mol → Partikel", "Partikel → Mol"])
            if mode == "Mol → Partikel":
                mol = st.number_input("Jumlah Mol", value=1.0)
                hitung = st.form_submit_button("Hitung Partikel")
                if hitung:
                    partikel = mol * 6.022e23
                    st.success(f"Jumlah Partikel: {partikel:.2e}")
            else:
                partikel = st.number_input("Jumlah Partikel", value=6.022e23)
                hitung = st.form_submit_button("Hitung Mol")
                if hitung:
                    mol = partikel / 6.022e23
                    st.success(f"Mol: {mol:.4f} mol")

    # --- Volume Gas (STP) ---
    elif kategori == "Volume Gas (STP)":
        with st.form(key="volume_stp_form"):
            mode = st.radio("Mode", ["Mol → Liter", "Liter → Mol"])
            if mode == "Mol → Liter":
                mol = st.number_input("Jumlah Mol", value=1.0)
                hitung = st.form_submit_button("Hitung Volume")
                if hitung:
                    volume = mol * 22.4
                    st.success(f"Volume Gas: {volume:.2f} L (STP)")
            else:
                volume = st.number_input("Volume Gas (L)", value=22.4)
                hitung = st.form_submit_button("Hitung Mol")
                if hitung:
                    mol = volume / 22.4
                    st.success(f"Mol: {mol:.4f} mol")

    # --- Suhu ---
    elif kategori == "Suhu":
        with st.form(key="suhu_form"):
            suhu_awal = st.number_input("Nilai Suhu", value=25.0)
            dari_satuan = st.selectbox("Dari", ["C", "K", "F"])
            ke_satuan = st.selectbox("Ke", ["C", "K", "F"])
            hitung = st.form_submit_button("Konversi Suhu")
            if hitung:
                if dari_satuan == ke_satuan:
                    hasil = suhu_awal
                elif dari_satuan == "C" and ke_satuan == "K":
                    hasil = suhu_awal + 273.15
                elif dari_satuan == "C" and ke_satuan == "F":
                    hasil = suhu_awal * 9/5 + 32
                elif dari_satuan == "K" and ke_satuan == "C":
                    hasil = suhu_awal - 273.15
                elif dari_satuan == "K" and ke_satuan == "F":
                    hasil = (suhu_awal - 273.15) * 9/5 + 32
                elif dari_satuan == "F" and ke_satuan == "C":
                    hasil = (suhu_awal - 32) * 5/9
                elif dari_satuan == "F" and ke_satuan == "K":
                    hasil = (suhu_awal - 32) * 5/9 + 273.15
                st.success(f"Hasil: {hasil:.2f}°{ke_satuan}")

    # --- Tekanan ---
    elif kategori == "Tekanan":
        with st.form(key="tekanan_form"):
            tekanan_awal = st.number_input("Nilai Tekanan", value=1.0)
            dari_satuan = st.selectbox("Dari", ["atm", "Pa", "mmHg", "torr", "bar"])
            ke_satuan = st.selectbox("Ke", ["atm", "Pa", "mmHg", "torr", "bar"])
            hitung = st.form_submit_button("Konversi Tekanan")
            if hitung:
                konversi_tekanan = {
                    "atm": {"Pa": 101325, "mmHg": 760, "torr": 760, "bar": 1.01325},
                    "Pa": {"atm": 1/101325, "mmHg": 760/101325, "torr": 760/101325, "bar": 1/100000},
                    "mmHg": {"atm": 1/760, "Pa": 101325/760, "torr": 1, "bar": 1.01325/760},
                    "torr": {"atm": 1/760, "Pa": 101325/760, "mmHg": 1, "bar": 1.01325/760},
                    "bar": {"atm": 1/1.01325, "Pa": 100000, "mmHg": 760/1.01325, "torr": 760/1.01325}
                }
                if dari_satuan == ke_satuan:
                    hasil = tekanan_awal
                else:
                    hasil = tekanan_awal * konversi_tekanan[dari_satuan][ke_satuan]
                st.success(f"Hasil: {hasil:.4f} {ke_satuan}")

    # --- Konsentrasi Larutan ---
    elif kategori == "Konsentrasi Larutan":
        st.subheader("Konversi Konsentrasi")
        konversi_opsi = st.selectbox("Pilih Konversi", [
            "Molaritas ↔ ppm",
            "Molaritas ↔ % w/v",
            "Molaritas ↔ Normalitas",
            "% w/v ↔ ppm"
        ])

        with st.form(key="konversi_konsentrasi_form"):
            nilai_awal = st.number_input("Nilai Konsentrasi", value=1.0, min_value=0.0)
            if konversi_opsi in ["Molaritas ↔ ppm", "Molaritas ↔ % w/v"]:
                massa_molar = st.number_input("Massa molar zat (g/mol)", value=58.44)
            if konversi_opsi in ["Molaritas ↔ Normalitas"]:
                valensi = st.number_input("Valensi / Faktor ekuivalen", value=1.0, min_value=0.1)
            if konversi_opsi in ["% w/v ↔ ppm"]:
                densitas = st.number_input("Densitas larutan (g/mL)", value=1.0)

            hitung = st.form_submit_button("Hitung")

            if hitung:
                hasil = None
                if konversi_opsi == "Molaritas ↔ ppm":
                    hasil = nilai_awal * massa_molar * 1000
                    st.success(f"{nilai_awal:.4f} mol/L = {hasil:.2f} ppm")
                elif konversi_opsi == "Molaritas ↔ % w/v":
                    hasil = nilai_awal * massa_molar / 10
                    st.success(f"{nilai_awal:.4f} mol/L = {hasil:.2f}% w/v")
                elif konversi_opsi == "Molaritas ↔ Normalitas":
                    hasil = nilai_awal * valensi
                    st.success(f"{nilai_awal:.4f} mol/L = {hasil:.2f} eq/L")
                elif konversi_opsi == "% w/v ↔ ppm":
                    hasil = nilai_awal * 10000
                    st.success(f"{nilai_awal:.4f}% w/v = {hasil:.2f} ppm")

# --- FITUR REGRESI LINIER ---
elif selected == "📈 Regresi Linier":
    st.title("📈 Kalkulator Regresi Linier")
    st.write("Hitung slope, intercept, persamaan garis regresi, dan tampilkan grafik.")

    metode_input = st.radio("Pilih metode input data:", ["Manual", "Upload CSV"])

    # Input judul sumbu
    x_label = st.text_input("Judul Sumbu X", "X")
    y_label = st.text_input("Judul Sumbu Y", "Y")

    if metode_input == "Manual":
        x_vals = st.text_area("Masukkan nilai X (pisahkan dengan koma):", "1, 2, 3, 4, 5")
        y_vals = st.text_area("Masukkan nilai Y (pisahkan dengan koma):", "2, 4, 5, 4, 5")
        try:
            x = np.array([float(i.strip()) for i in x_vals.split(",")]).reshape(-1, 1)
            y = np.array([float(i.strip()) for i in y_vals.split(",")])
        except:
            st.error("⚠️ Pastikan semua nilai valid.")
            x, y = np.array([]), np.array([])
    else:
        uploaded_file = st.file_uploader("Upload file CSV dengan kolom X dan Y")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write(df)
            x = df["X"].values.reshape(-1, 1)
            y = df["Y"].values
        else:
            x, y = np.array([]), np.array([])

    if st.button("Hitung Regresi") and len(x) > 0 and len(y) > 0:
        try:
            model = LinearRegression().fit(x, y)
            slope = model.coef_[0]
            intercept = model.intercept_
            r_sq = model.score(x, y)

            st.success(f"Persamaan: **{y_label} = {slope:.3f}{x_label} + {intercept:.3f}**")
            st.info(f"R² (koefisien determinasi): {r_sq:.4f}")

            # Plot grafik regresi
            fig, ax = plt.subplots()
            ax.scatter(x, y, color="blue", label="Data")
            ax.plot(x, model.predict(x), color="red", label="Garis Regresi")
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title("Grafik Regresi Linier")
            ax.legend()
            st.pyplot(fig)

            # Tombol Download PDF
            from io import BytesIO
            buffer = BytesIO()
            fig.savefig(buffer, format="pdf")
            buffer.seek(0)  # Penting: kembalikan pointer ke awal
            st.download_button(
                label="📄 Download Grafik Regresi (PDF)",
                data=buffer.getvalue(),
                file_name="regresi_linier.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"⚠️ Error saat menghitung regresi: {e}")
