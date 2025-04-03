import streamlit as st
from app.auth import login_page
from app.perguntas_frequentes import perguntas_frequentes
import requests
from app.portfolio.block.render_carteiras import render_carteiras

def configure_menu():
    """Configura as opções do menu com base na autenticação do usuário."""
    menu_options = ["Carteiras", "Home", "Sobre", "Perguntas Frequentes", "Logout"]
    page = st.sidebar.radio("Navegar para:", menu_options, )

    # Navegação entre as páginas
    if page == "Carteiras":
        render_carteiras()
    if page == "Home":
        """Renderiza a página inicial."""
        st.title("Página Inicial")
    elif page == "Sobre":
        """Renderiza a página Sobre."""
        st.title("Sobre")
        st.write("Informações sobre o aplicativo.")
    elif page == "Perguntas Frequentes":
        """Renderiza a página de Perguntas Frequentes."""
        perguntas_frequentes()
    elif page == "Login":
        login_page.main()

def get_account_url():
    return "True"

def main():
    is_authenticated = login_page.is_authenticated()

    if is_authenticated:
        configure_menu()

    render_account_management(is_authenticated)

def render_account_management(is_authenticated:bool):
    """
    Renderiza a página de gerenciamento da conta no sidebar.
    Permite visualizar e alterar informações, além de realizar logout.
    """

    if not is_authenticated:
        login_page.main()
    else:
        st.sidebar.divider()
        st.sidebar.header("Gerenciamento da Conta")
        if st.sidebar.button("Configurações", use_container_width=True):
            login_page.logout()

        if st.sidebar.button("Log Out", disabled=False, use_container_width=True):
            login_page.logout()


if __name__ == "__main__":
    # Configurações da página
    # st.set_page_config(
    #     page_title="Finance Analyzer",
    #     page_icon="📊",
    #     layout="wide",
    #     initial_sidebar_state="collapsed",
    # )
    
    main()
    

##############################################################

# from streamlit_cookies_manager import EncryptedCookieManager

# # Configuração do gerenciador de cookies
# cookies = EncryptedCookieManager(
#     password="chave-secreta-para-encriptar2"  # Substitua por algo mais seguro
# )

# if not cookies.ready():
#     st.stop()

# cookies["access_token"] = "token2"
# cookies.save()  # Salva o cookie no navegador


# del cookies['access_token']
# print(cookies.get("access_token"))
# print("access_token" in cookies)

# login_page.login("guilherme@gmail.com", "#Gui12345678")

# st.write(login_page.cookies.get("access_token"))