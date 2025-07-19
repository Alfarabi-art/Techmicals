import streamlit as st

def show():
    st.title("🏠 Selamat Datang di Techmicals")
    st.markdown("""
    <h3 style='text-align:center; color:#3f3d56;'>
        Teman Asik Kimia-mu – Seru, Modern, dan Mudah!
    </h3>
    """, unsafe_allow_html=True)

    st.write("""
    Selamat datang di **Techmicals**, aplikasi all-in-one untuk semua kebutuhan kimia kamu. 🚀
    Hitung reaksi, mol, konsentrasi, hingga regresi linier dengan mudah.
    """)

    st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
        transition: 0.3s;
    }
    .feature-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    </style>

    <div class="grid-container">
        <div class="feature-card">
            <h3>⚗ Reaksi Kimia</h3>
            <p>Setarakan reaksi dengan cepat dan akurat.</p>
        </div>
        <div class="feature-card">
            <h3>🧪 Stoikiometri</h3>
            <p>Hitung mol, massa molar, dan lainnya.</p>
        </div>
        <div class="feature-card">
            <h3>📈 Konsentrasi Larutan</h3>
            <p>Hitung dan konversi konsentrasi larutan.</p>
        </div>
        <div class="feature-card">
            <h3>💧 pH dan pOH</h3>
            <p>Hitung pH dan pOH larutan.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚗ Mulai Hitung Sekarang"):
        st.experimental_r_
