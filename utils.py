import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from chempy import balance_stoichiometry
from periodictable import elements
from sklearn.linear_model import LinearRegression
from io import BytesIO
import math

def fitur_home():
    st.title("🧪 Techmicals")
    st.markdown("Teman Asik Kimia-mu – Seru, Modern, dan Mudah!")

def fitur_about():
    st.title("📖 Tentang Aplikasi")
    st.write("Techmicals adalah kalkulator kimia interaktif ...")

def fitur_reaksi_kimia():
    st.title("⚗ Setarakan Reaksi Kimia")
    eq = st.text_input("Masukkan reaksi (contoh: H2 + O2 -> H2O)")
    if st.button("Setarakan"):
        try:
            reac, prod = eq.split("->")
            reac_set, prod_set = set(reac.split("+")), set(prod.split("+"))
            r, p = balance_stoichiometry(reac_set, prod_set)
            hasil = " + ".join([f"{v} {k}" for k,v in r.items()]) + " → " + \
                    " + ".join([f"{v} {k}" for k,v in p.items()])
            st.success(f"Persamaan setara: {hasil}")
        except Exception as e:
            st.error(f"Gagal: {e}")

def fitur_stoikiometri():
    st.title("🧪 Hitung Mol")
    formula = st.text_input("Rumus Kimia", "H2O")
    massa = st.number_input("Massa (gram)", min_value=0.0)
    if st.button("Hitung Mol"):
        try:
            molar_mass = sum(getattr(elements, el).mass * (int(n) if n else 1)
                             for el, n in re.findall(r"([A-Z][a-z]*)(\d*)", formula))
            mol = massa / molar_mass
            st.success(f"{mol:.4f} mol (Massa molar: {molar_mass:.2f} g/mol)")
        except:
            st.error("Rumus salah atau unsur tidak ditemukan")

def fitur_konsentrasi_larutan():
    st.title("🧫 Hitung Konsentrasi")
    metode = st.selectbox("Pilih Metode", ["Molaritas", "Normalitas"])
    massa = st.number_input("Massa zat terlarut (g)", min_value=0.0)
    volume = st.number_input("Volume larutan (L)", min_value=0.0)
    if metode == "Molaritas":
        molar_mass = st.number_input("Massa molar (g/mol)", min_value=0.0)
        if st.button("Hitung Molaritas"):
            mol = massa / molar_mass
            M = mol / volume
            st.success(f"Molaritas: {M:.4f} mol/L")
    else:
        eq_weight = st.number_input("Berat ekuivalen (g/eq)", min_value=0.0)
        if st.button("Hitung Normalitas"):
            eq = massa / eq_weight
            N = eq / volume
            st.success(f"Normalitas: {N:.4f} eq/L")

def fitur_ph_poh():
    st.title("💧 Hitung pH dan pOH")
    conc = st.number_input("Konsentrasi (mol/L)", min_value=0.0)
    tipe = st.selectbox("Larutan", ["Asam", "Basa"])
    if st.button("Hitung"):
        if conc > 0:
            pH = -math.log10(conc) if tipe=="Asam" else 14 + math.log10(conc)
            st.success(f"pH: {pH:.2f}")

def fitur_tabel_periodik():
    st.title("🧬 Tabel Periodik")
    df = pd.DataFrame({
        "Symbol": [el.symbol for el in elements],
        "Name": [el.name for el in elements],
        "Mass": [el.mass for el in elements]
    })
    st.dataframe(df)

def fitur_konversi_satuan():
    st.title("🔄 Konversi Satuan")
    # buat logika konversi seperti mol↔gram, suhu, dll

def fitur_regresi_linier():
    st.title("📈 Regresi Linier")
    x_vals = st.text_area("X (pisahkan koma):", "1,2,3,4,5")
    y_vals = st.text_area("Y (pisahkan koma):", "2,4,5,4,5")
    if st.button("Hitung Regresi"):
        x = np.array([float(i) for i in x_vals.split(",")]).reshape(-1,1)
        y = np.array([float(i) for i in y_vals.split(",")])
        model = LinearRegression().fit(x,y)
        slope, intercept = model.coef_[0], model.intercept_
        st.success(f"y = {slope:.3f}x + {intercept:.3f}")
        fig, ax = plt.subplots()
        ax.scatter(x, y)
        ax.plot(x, model.predict(x), color='red')
        st.pyplot(fig)
