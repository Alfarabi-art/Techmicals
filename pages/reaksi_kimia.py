import streamlit as st
from chempy import balance_stoichiometry

def show_reaksi_kimia():
    st.title("⚗ Setarakan Reaksi Kimia")
    st.write("Masukkan persamaan reaksi untuk disetarakan:")

    equation = st.text_input("Persamaan Reaksi", "H2 + O2 -> H2O")

    if st.button("Setarakan"):
        if "->" not in equation:
            st.error("⚠ Format reaksi harus mengandung '->' sebagai pemisah pereaksi dan produk.")
        else:
            try:
                reactants, products = equation.split("->")
                reactants_set = set(reactants.strip().split('+'))
                products_set = set(products.strip().split('+'))
                reac_bal, prod_bal = balance_stoichiometry(reactants_set, products_set)
                balanced_eq = " + ".join(f"{v} {k}" for k, v in reac_bal.items())
                balanced_eq += " → "
                balanced_eq += " + ".join(f"{v} {k}" for k, v in prod_bal.items())
                st.success(f"✅ Persamaan Setara: {balanced_eq}")
            except Exception as e:
                st.error(f"❌ Error saat menyetarakan: {e}")
