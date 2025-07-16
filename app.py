
import streamlit as st
from chempy import balance_stoichiometry
from periodictable import elements
import math
import re

st.set_page_config(page_title="Techmicals", page_icon="⚗️", layout="wide")

st.markdown("""
<style>
body {
    background: linear-gradient(to bottom right, #00bfff, #1e90ff);
    color: #fff;
}

.stButton>button {
    background-color: #ff6347;
    color: white;
    border-radius: 8px;
    font-size: 16px;
    padding: 10px 20px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #ffffff33;
    color: #333;
    border-radius: 6px;
    padding: 10px;
}

.stTabs [aria-selected="true"] {
    background-color: #1e90ff !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("⚗️ Techmicals")

tabs = st.tabs(["⚖️ Setarakan Reaksi", "🧪 Stoikiometri", "📏 Ketidakpastian", "📐 Konversi"])

def molar_mass(formula):
    pattern = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    mass = 0
    for (element, count) in pattern:
        try:
            element_mass = elements.symbol(element).mass
            count = int(count) if count else 1
            mass += element_mass * count
        except:
            pass
    return mass

with tabs[0]:
    st.header("⚖️ Setarakan Reaksi")
    equation = st.text_input("Masukkan Persamaan Reaksi", "CH4 + O2 -> CO2 + H2O")
    if st.button("Setarakan"):
        try:
            reac, prod = equation.split("->")
            reac_set = set(reac.strip().split('+'))
            prod_set = set(prod.strip().split('+'))
            reac_bal, prod_bal = balance_stoichiometry(reac_set, prod_set)
            balanced_eq = " + ".join(f"{v} {k}" for k, v in reac_bal.items())
            balanced_eq += " → "
            balanced_eq += " + ".join(f"{v} {k}" for k, v in prod_bal.items())
            st.success(f"**Persamaan Setara:** {balanced_eq}")
            st.write("**Massa Molar (g/mol):**")
            for sub in reac_bal.keys() | prod_bal.keys():
                mm = molar_mass(sub)
                st.write(f"- {sub.strip()}: {mm:.2f} g/mol")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

with tabs[1]:
    st.header("🧪 Stoikiometri")
    formula = st.text_input("Rumus Kimia", "H2O")
    mass = st.number_input("Massa (gram)", min_value=0.0)
    if st.button("Hitung Stoikiometri"):
        try:
            mm = molar_mass(formula)
            moles = mass / mm
            particles = moles * 6.022e23
            st.success(f"{mass} g {formula} = {moles:.4f} mol = {particles:.2e} partikel")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

with tabs[2]:
    st.header("📏 Ketidakpastian")
    nilai = st.number_input("Nilai (x)", min_value=0.0)
    delta = st.number_input("Δx", min_value=0.0)
    if st.button("Hitung Ketidakpastian"):
        try:
            rel_unc = (delta / nilai) * 100 if nilai != 0 else 0
            st.success(f"**Hasil:** {nilai} ± {delta} (Relatif: {rel_unc:.2f}%)")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

with tabs[3]:
    st.header("📐 Konversi Suhu")
    temp_value = st.number_input("Nilai Suhu", value=25.0)
    temp_from = st.selectbox("Dari", ["C", "K", "F"])
    temp_to = st.selectbox("Ke", ["C", "K", "F"])
    if st.button("Konversi Suhu"):
        if temp_from == temp_to:
            st.success(f"Hasil: {temp_value:.2f}°{temp_to}")
        else:
            if temp_from == "C":
                if temp_to == "K":
                    result = temp_value + 273.15
                elif temp_to == "F":
                    result = temp_value * 9/5 + 32
            elif temp_from == "K":
                if temp_to == "C":
                    result = temp_value - 273.15
                elif temp_to == "F":
                    result = (temp_value - 273.15) * 9/5 + 32
            elif temp_from == "F":
                if temp_to == "C":
                    result = (temp_value - 32) * 5/9
                elif temp_to == "K":
                    result = (temp_value - 32) * 5/9 + 273.15
            st.success(f"Hasil: {result:.2f}°{temp_to}")
