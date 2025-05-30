import streamlit as st
from app.auth import login_page
import requests
from app.portfolio.block.render_carteiras import render_carteiras

from app.pages import home, sobre, perguntas_frequentes

# st.set_page_config(
#     page_title="Meu Projeto",
#     page_icon="💼",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

def configure_menu():
    """Configura as opções do menu com base na autenticação do usuário."""
    # menu_options = ["Carteiras", "Home", "Sobre", "Perguntas Frequentes", "Logout"]
    menu_options = {
    "🏠 Home": home.show,
    "💼 Carteiras": render_carteiras,
    "ℹ️ Sobre": sobre.show,
    "❓ Perguntas Frequentes": perguntas_frequentes.show,
    "🔒 Logout": login_page.logout
}   
    page = st.sidebar.radio("Navegar para:", list(menu_options.keys()))
    # page = st.sidebar.radio("Navegar para:", menu_options, )
    
    menu_options[page]()

def main():
    if login_page.is_authenticated():
        configure_menu()
        render_account_management(True)
    else:
        login_page.show_login()

def render_account_management(is_authenticated:bool):
    """
    Renderiza a página de gerenciamento da conta no sidebar.
    Permite visualizar e alterar informações, além de realizar logout.
    """

    if not is_authenticated:
        login_page.main()
    else:
        st.sidebar.divider()
        # st.sidebar.header("Gerenciamento da Conta")
        st.sidebar.subheader("Gerenciar Conta")
        if st.sidebar.button("🔧 Configurações", use_container_width=True):
            st.info("Página de configurações em construção...")

        if st.sidebar.button("🔒 Logout", disabled=False, use_container_width=True):
            login_page.logout()

if __name__ == "__main__":
    main()
 