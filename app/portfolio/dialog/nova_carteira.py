import streamlit as st
from app.auth.login_page import cookies
import requests
from app.utils.api_client import make_request


@st.dialog("Nova Carteira")
def nova_carteira():
    access_token = cookies.get('access_token')
    st.text_input("  ", key="wallet_name")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Criar"):
            # Exemplo de salvamento (simplesmente imprime os dados por enquanto)
            data = {
                "name": st.session_state.get("wallet_name")
                }
            
            headers = {"Authorization": f"Bearer {access_token}"}
            response_json = make_request(method="POST", endpoint="/portfolio/create", 
                                    data=data, headers=headers,
                                    message_except="Erro em criar nova carteira")
            
            if not response_json:
                st.warning(response_json.get("detail", "Erro em criar nova carteira"))
                return 

            st.session_state.wallet_id = response_json.get("id", None)
            st.rerun()
                

    with col2:
        if st.button("Cancelar"):
            pass