import streamlit as st

def show_konsentrasi():
    st.title("🧫 Hitung Konsentrasi Larutan")
    metode = st.selectbox("Pilih Metode", ["Molaritas", "Normalitas"])

    with st.form("konsentrasi_form"):
        if metode == "Molaritas":
            solute_mass = st.number_input("Massa zat terlarut (g)", min_value=0.0)
            volume = st.number_input("Volume larutan (L)", min_value=0.0)
            molar_mass = st.number_input("Massa molar zat (g/mol)", min_value=0.0)
            hitung = st.form_submit_button("Hitung Molaritas")
            if hitung and volume > 0 and molar_mass > 0:
                mol = solute_mass / molar_mass
                molarity = mol / volume
                st.success(f"✅ Molaritas: {molarity:.4f} mol/L")
        else:
            solute_mass = st.number_input("Massa zat terlarut (g)", min_value=0.0)
            eq_weight = st.number_input("Berat ekuivalen (g/eq)", min_value=0.0)
            volume = st.number_input("Volume larutan (L)", min_value=0.0)
            hitung = st.form_submit_button("Hitung Normalitas")
            if hitung and volume > 0 and eq_weight > 0:
                eq = solute_mass / eq_weight
                normality = eq / volume
                st.success(f"✅ Normalitas: {normality:.4f} eq/L")
