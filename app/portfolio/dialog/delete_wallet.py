import streamlit as st
import requests
from app.utils.constants import API_URL

@st.dialog("Opções")
def delete_wallet(wallet_id):
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(f"Deletar {wallet_id}"):

            response = requests.delete(f"{API_URL}/portfolio/wallet/delete/{wallet_id}")

            if response.status_code != 200:
                response_json = response.json()
                st.warning(response_json.get("detail", "Erro ao deletar carteira"))
            else:
                st.rerun()
    with col2:
        if st.button("Editar"):
            pass
    with col3:
        if st.button("Cancelar"):
            pass