import streamlit as st

def show_konversi_satuan():
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
