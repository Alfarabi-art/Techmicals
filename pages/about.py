import streamlit as st

def show_about():
    st.markdown("<h1 style='text-align:center;'>📖 Tentang Aplikasi</h1>", unsafe_allow_html=True)

    st.write("""
        <div style='text-align:center;'>
        <p><b>Techmicals</b> adalah kalkulator kimia interaktif yang dibuat untuk mempermudah perhitungan kimia dalam dunia pendidikan dan praktikum.</p>
        <p>💻 Dibuat oleh <b>Tim Techmicals</b> dengan ❤️ untuk para siswa dan mahasiswa.</p>
        <p style='font-style:italic; color:#555;'>“Sains itu seru kalau kamu punya alat yang tepat.”</p>
        <img src="https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif" width="250">
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center;'>👥 Anggota Tim</h3>", unsafe_allow_html=True)

    # Grid anggota tim
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='feature-card'><h4>👩‍🔬 Azkia Nadira Azmi</h4><p>NIM - 2460341</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><h4>👨‍🔬 Hanif Zaki Abizar</h4><p>NIM - 2460384</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-card'><h4>👨‍🔬 Muhammad Al Farabi</h4><p>NIM - 2460430</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='feature-card'><h4>👩‍🔬 Ovalia Kareva Betaubun</h4><p>NIM - 2460478</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><h4>👩‍🔬 Widya Aulia Putri</h4><p>NIM - 2460534</p></div>", unsafe_allow_html=True)

    st.markdown("<footer>© 2025 Techmicals by Kelompok 10 | All rights reserved.</footer>", unsafe_allow_html=True)
