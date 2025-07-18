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

# --- CONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Techmicals",
    page_icon="⚗",
    layout="wide",
)

# --- SESSION STATE ---
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False
if "menu_selected" not in st.session_state:
    st.session_state.menu_selected = "🏠 Home"

# --- SIDEBAR MENU ---
if st.session_state.show_sidebar:
    with st.sidebar:
        menu = option_menu(
            menu_title="🌟 Kebutuhan Kimia",
            options=[
                "🏠 Home", "⚗ Reaksi Kimia", "🧪 Stoikiometri",
                "🧫 Konsentrasi Larutan", "💧 pH dan pOH",
                "🧬 Tabel Periodik", "🔄 Konversi Satuan",
                "📈 Regresi Linier", "📖 About"
            ],
            icons=[
                "house", "flask", "calculator",
                "droplet-half", "thermometer-half",
                "grid-3x3-gap-fill", "repeat",
                "graph-up", "info-circle"
            ],
            default_index=0
        )
        st.session_state.menu_selected = menu

selected = st.session_state.menu_selected

# --- HOME ---
if selected == "🏠 Home":
    st.title("🧪 Techmicals")
    st.subheader("Teman Asik Kimia-mu – Seru, Modern, dan Mudah!")
    st.write("Selamat datang di **Techmicals**, aplikasi all-in-one untuk semua kebutuhan kimia kamu.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("⚗ **Reaksi Kimia**\n\nSetarakan reaksi dengan cepat dan akurat.")
        st.success("🧪 **Stoikiometri**\n\nHitung mol, massa molar, dan lainnya.")
    with col2:
        st.warning("📈 **Konsentrasi Larutan**\n\nHitung dan konversi konsentrasi larutan.")
        st.info("💧 **pH dan pOH**\n\nHitung pH dan pOH larutan.")
    with col3:
        st.success("🧬 **Tabel Periodik**\n\nLihat data unsur periodik.")
        st.warning("📈 **Regresi Linier**\n\nTampilkan grafik regresi data.")

    if st.button("⚗ Mulai Hitung Sekarang"):
        st.session_state.show_sidebar = True
        st.session_state.menu_selected = "⚗ Reaksi Kimia"

# --- ABOUT ---
elif selected == "📖 About":
    st.title("📖 Tentang Aplikasi")
    st.write("**Techmicals** adalah kalkulator kimia interaktif yang dibuat untuk mempermudah perhitungan kimia dalam dunia pendidikan dan praktikum.")
    st.write("💻 Dibuat oleh **Tim Techmicals**.")
    st.caption("“Sains itu seru kalau kamu punya alat yang tepat.”")
    st.header("👥 Anggota Tim")
    st.text("👩‍🔬 Azkia Nadira Azmi - 2460341")
    st.text("👨‍🔬 Hanif Zaki Abizar - 2460384")
    st.text("👨‍🔬 Muhammad Al Farabi - 2460430")
    st.text("👩‍🔬 Ovalia Kareva Betaubun - 2460478")
    st.text("👩‍🔬 Widya Aulia Putri - 2460534")

# --- FITUR REAKSI KIMIA ---
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

# --- Fitur Konsentrasi Larutan ---
elif menu == "🧫 Konsentrasi Larutan":
    st.header("🧫 Hitung Konsentrasi Larutan")
    metode = st.selectbox("Pilih metode", ["Molaritas", "Normalitas"])
    if metode == "Molaritas":
        massa = st.number_input("Massa zat terlarut (gram)", value=5.0)
        molar_mass = st.number_input("Massa molar (g/mol)", value=58.44)
        volume = st.number_input("Volume larutan (liter)", value=0.5)
        if st.button("Hitung Molaritas"):
            try:
                mol = massa / molar_mass
                molarity = mol / volume
                st.success(f"Molaritas: {molarity:.4f} mol/L")
            except:
                st.error("Periksa kembali input Anda.")
    else:  # Normalitas
        massa = st.number_input("Massa zat terlarut (gram)", value=5.0)
        eq_weight = st.number_input("Berat ekuivalen (g/eq)", value=58.44)
        volume = st.number_input("Volume larutan (liter)", value=0.5)
        if st.button("Hitung Normalitas"):
            try:
                eq = massa / eq_weight
                normality = eq / volume
                st.success(f"Normalitas: {normality:.4f} eq/L")
            except:
                st.error("Periksa kembali input Anda.")

# --- FITUR pH DAN pOH ---
elif selected == "💧 pH dan pOH":
    st.title("💧 Hitung pH dan pOH")
    conc = st.number_input("Konsentrasi (mol/L)", min_value=0.0, value=0.01)
    acid_base = st.radio("Jenis Larutan", ["Asam", "Basa"])
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

# ✅ --- Konversi Satuan ---
elif menu == "🔄 Konversi Satuan":
    st.header("🔄 Konversi Satuan Kimia")
    kategori = st.selectbox("Pilih Kategori", [
        "Mol ↔ Gram",
        "Mol ↔ Partikel",
        "Volume Gas (STP)",
        "Suhu",
        "Tekanan",
        "Konsentrasi Larutan"
    ])

    if kategori == "Mol ↔ Gram":
        mode = st.radio("Mode", ["Mol → Gram", "Gram → Mol"])
        massa_molar = st.number_input("Massa Molar (g/mol)", value=18.0)
        if mode == "Mol → Gram":
            mol = st.number_input("Jumlah Mol", value=1.0)
            if st.button("Hitung Massa"):
                mass = mol * massa_molar
                st.success(f"Massa: {mass:.4f} gram")
        else:
            mass = st.number_input("Massa (gram)", value=1.0)
            if st.button("Hitung Mol"):
                mol = mass / massa_molar
                st.success(f"Mol: {mol:.4f} mol")

    elif kategori == "Mol ↔ Partikel":
        mode = st.radio("Mode", ["Mol → Partikel", "Partikel → Mol"])
        if mode == "Mol → Partikel":
            mol = st.number_input("Jumlah Mol", value=1.0)
            if st.button("Hitung Partikel"):
                partikel = mol * 6.022e23
                st.success(f"Jumlah Partikel: {partikel:.2e}")
        else:
            partikel = st.number_input("Jumlah Partikel", value=6.022e23)
            if st.button("Hitung Mol"):
                mol = partikel / 6.022e23
                st.success(f"Mol: {mol:.4f} mol")

    elif kategori == "Volume Gas (STP)":
        mode = st.radio("Mode", ["Mol → Liter", "Liter → Mol"])
        if mode == "Mol → Liter":
            mol = st.number_input("Jumlah Mol", value=1.0)
            if st.button("Hitung Volume"):
                volume = mol * 22.4
                st.success(f"Volume Gas: {volume:.2f} L (STP)")
        else:
            volume = st.number_input("Volume Gas (L)", value=22.4)
            if st.button("Hitung Mol"):
                mol = volume / 22.4
                st.success(f"Mol: {mol:.4f} mol")

    elif kategori == "Suhu":
        suhu_awal = st.number_input("Nilai Suhu", value=25.0)
        dari = st.selectbox("Dari", ["C", "K", "F"])
        ke = st.selectbox("Ke", ["C", "K", "F"])
        if st.button("Konversi Suhu"):
            hasil = suhu_awal
            if dari != ke:
                if dari == "C" and ke == "K": hasil += 273.15
                elif dari == "C" and ke == "F": hasil = suhu_awal * 9/5 + 32
                elif dari == "K" and ke == "C": hasil -= 273.15
                elif dari == "K" and ke == "F": hasil = (suhu_awal - 273.15) * 9/5 + 32
                elif dari == "F" and ke == "C": hasil = (suhu_awal - 32) * 5/9
                elif dari == "F" and ke == "K": hasil = (suhu_awal - 32) * 5/9 + 273.15
            st.success(f"Hasil: {hasil:.2f}°{ke}")

    elif kategori == "Tekanan":
        tekanan_awal = st.number_input("Nilai Tekanan", value=1.0)
        dari = st.selectbox("Dari", ["atm", "Pa", "mmHg", "bar"])
        ke = st.selectbox("Ke", ["atm", "Pa", "mmHg", "bar"])
        konversi = {
            "atm": {"Pa": 101325, "mmHg": 760, "bar": 1.01325},
            "Pa": {"atm": 1/101325, "mmHg": 760/101325, "bar": 1e-5},
            "mmHg": {"atm": 1/760, "Pa": 133.322, "bar": 1.333e-3},
            "bar": {"atm": 0.98692, "Pa": 1e5, "mmHg": 750.062}
        }
        if st.button("Konversi Tekanan"):
            if dari == ke:
                hasil = tekanan_awal
            else:
                hasil = tekanan_awal * konversi[dari][ke]
            st.success(f"Hasil: {hasil:.4f} {ke}")

    elif kategori == "Konsentrasi Larutan":
        st.subheader("Konversi Konsentrasi Larutan")
        konversi_opsi = st.selectbox("Pilih Konversi", [
            "Molaritas → ppm",
            "Molaritas → % w/v",
            "Molaritas → Normalitas",
            "% w/v → ppm"
        ])

        nilai_awal = st.number_input("Nilai Konsentrasi", value=1.0, min_value=0.0)
        massa_molar = 0
        valensi = 1

        if konversi_opsi in ["Molaritas → ppm", "Molaritas → % w/v"]:
            massa_molar = st.number_input("Massa molar zat (g/mol)", value=58.44)
        if konversi_opsi == "Molaritas → Normalitas":
            valensi = st.number_input("Valensi / Faktor ekuivalen", value=1.0, min_value=0.1)

        if st.button("Hitung Konversi"):
            hasil = None
            if konversi_opsi == "Molaritas → ppm":
                hasil = nilai_awal * massa_molar * 1000
                st.success(f"{nilai_awal:.4f} mol/L = {hasil:.2f} ppm")
            elif konversi_opsi == "Molaritas → % w/v":
                hasil = nilai_awal * massa_molar / 10
                st.success(f"{nilai_awal:.4f} mol/L = {hasil:.2f}% w/v")
            elif konversi_opsi == "Molaritas → Normalitas":
                hasil = nilai_awal * valensi
                st.success(f"{nilai_awal:.4f} mol/L = {hasil:.2f} eq/L")
            elif konversi_opsi == "% w/v → ppm":
                hasil = nilai_awal * 10000
                st.success(f"{nilai_awal:.4f}% w/v = {hasil:.2f} ppm")

# --- FITUR REGRESI LINIER ---
elif selected == "📈 Regresi Linier":
    st.header("📈 Kalkulator Regresi Linier")
    st.write("Hitung slope, intercept, persamaan garis regresi, tampilkan grafik, dan download PDF.")

    metode_input = st.radio("Pilih metode input data:", ["Manual", "Upload CSV"])

    x_label = st.text_input("Judul Sumbu X", "X")
    y_label = st.text_input("Judul Sumbu Y", "Y")

    if metode_input == "Manual":
        x_vals = st.text_area("Masukkan nilai X (pisahkan dengan koma):", "1, 2, 3, 4, 5")
        y_vals = st.text_area("Masukkan nilai Y (pisahkan dengan koma):", "2, 4, 5, 4, 5")
        try:
            x = np.array([float(i.strip()) for i in x_vals.split(",")]).reshape(-1, 1)
            y = np.array([float(i.strip()) for i in y_vals.split(",")])
        except:
            st.error("⚠ Pastikan semua nilai valid.")
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

            st.success(f"Persamaan: *{y_label} = {slope:.3f}{x_label} + {intercept:.3f}*")
            st.info(f"R² (koefisien determinasi): {r_sq:.4f}")

            # Plot grafik regresi
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(x, y, color="blue", label="Data")
            ax.plot(x, model.predict(x), color="red", label="Garis Regresi")
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title("Grafik Regresi Linier")

            # Tambahkan hasil regresi ke grafik
            textstr = (
                f"Persamaan: {y_label} = {slope:.3f}{x_label} + {intercept:.3f}\n"
                f"Slope (m): {slope:.3f}\n"
                f"Intercept (b): {intercept:.3f}\n"
                f"R²: {r_sq:.4f}"
            )
            ax.text(
                0.05, 0.95, textstr,
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", edgecolor="gray")
            )

            ax.legend()
            st.pyplot(fig)

            # Tombol Download PDF
            from io import BytesIO
            buffer = BytesIO()
            fig.savefig(buffer, format="pdf")
            buffer.seek(0)
            st.download_button(
                label="📄 Download Grafik Regresi (PDF)",
                data=buffer.getvalue(),
                file_name="regresi_linier.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"⚠ Error saat menghitung regresi: {e}")


# --- Footer ---
st.write("---")
st.write("© 2025 Techmicals by Kelompok 10 | All rights reserved.")
