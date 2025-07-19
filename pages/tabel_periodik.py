import streamlit as st
import pandas as pd
from periodictable import elements

def show_tabel_periodik():
    st.title("🧬 Tabel Periodik Interaktif")
    periodic_data = [{"Symbol": el.symbol, "Name": el.name, "Atomic Number": el.number, "Atomic Mass": el.mass}
                     for el in elements if el.number <= 118]
    df = pd.DataFrame(periodic_data)
    st.dataframe(df, use_container_width=True)

    selected_element = st.selectbox("Pilih Unsur", [el.symbol for el in elements if el.number <= 118])
    if selected_element:
        el = getattr(elements, selected_element)
        st.markdown(f"""
        <div class="feature-card">
            <h3>{el.name} ({el.symbol})</h3>
            <p>Nomor Atom: {el.number}</p>
            <p>Massa Atom: {el.mass} g/mol</p>
        </div>
        """, unsafe_allow_html=True)
