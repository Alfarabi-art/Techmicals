import streamlit as st

def show_home():
    st.markdown("<h1 style='text-align:center;'>🧪 Techmicals</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#3f3d56;'>Teman Asik Kimia-mu – Seru, Modern, dan Mudah!</h3>", unsafe_allow_html=True)

    st.write("""
        <p style='text-align:center;'>Selamat datang di <b>Techmicals</b>, aplikasi all-in-one untuk semua kebutuhan kimia kamu.  
        🚀 Hitung reaksi, mol, konsentrasi, hingga regresi linier dengan mudah.</p>
    """, unsafe_allow_html=True)

    # Grid fitur
    st.markdown("""
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
        <div class="feature-card">
            <h3>🧬 Tabel Periodik</h3>
            <p>Lihat data unsur periodik.</p>
        </div>
        <div class="feature-card">
            <h3>📈 Regresi Linier</h3>
            <p>Tampilkan grafik regresi data.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚗ Mulai Hitung Sekarang"):
        st.session_state.show_sidebar = True
        st.session_state.menu_selected = "⚗ Reaksi Kimia"

        st.experimental_rerun()
