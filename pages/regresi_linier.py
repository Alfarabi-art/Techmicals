import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from io import BytesIO

def show_regresi_linier():
    st.title("📈 Kalkulator Regresi Linier")
    st.write("Hitung slope, intercept, persamaan garis regresi, dan tampilkan grafik.")

    # Pilih metode input data
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

            st.success(f"Persamaan: {y_label} = {slope:.3f}{x_label} + {intercept:.3f}")
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
