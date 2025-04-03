import streamlit as st
import requests
from app.cookie_controller.cookie_controller import CookieController
from app.utils.constants import API_URL
import requests
# Configurações do Streamlit

# Controlador de cookies
controller = CookieController()

# Função para autenticar o usuário
def login(email, password):
    url = f"{API_URL}/auth/token"
    data = {"username": email, "password": password}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json(), response.status_code == 200
    except requests.exceptions.RequestException as e:
        return None, False

# Função para registrar o usuário
def signup(name, email, password):
    url = f"{API_URL}/auth/signup"
    data = {"name": name, "email": email, "password": password}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True, "Usuário registrado com sucesso!"
    except requests.exceptions.RequestException as e:
        return False, f"Erro ao registrar: {str(e)}"

# Função para verificar autenticação
def is_authenticated():

    response = requests.get(f'http://localhost:5000/auth/get-cookie')

    url = f"{API_URL}/auth/verify"
    access_token = controller.get("access_token")
    print(">>>> get_cookie: ", response.json())
    
    if not access_token:
        return False
    
    # headers = {"Authorization": f"Bearer {access_token}"}
    cookies={"access_token": access_token}
    try:
        response = requests.get(url, cookies=cookies)
        # response = requests.post(url, headers=headers)
        return response.json().get("valid", False)
    except requests.RequestException:
        return False

# Função para realizar o logout
def logout():
    controller.remove("access_token")
    st.success("Você saiu com sucesso!")
    st.rerun()

# Interface principal do Streamlit
def main():
    # Cabeçalho principal
    st.title("🔒 Sistema de Autenticação")
    st.markdown(
        """
        Bem-vindo ao sistema de autenticação. Faça login ou registre-se para continuar.
        """
    )


    if is_authenticated():
        st.success("✅ Você já está autenticado!")
        if st.button("🔓 Sair"):
            logout()
        return

    # Abas para alternar entre Login e Cadastro
    tab = st.tabs(["🔑 Login", "📝 Cadastro"])
    
    # Aba de Login
    with tab[0]:
        st.header("Login")
        email = st.text_input("📧 Email", key="login_email")
        password = st.text_input("🔑 Senha", type="password", key="login_password")
        if st.button("Entrar", use_container_width=False, key="login_button"):
            token, success = login(email, password)
            if success:
                controller.set("access_token", token["access_token"])
                st.success("✅ Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Credenciais inválidas. Tente novamente.")

    # Aba de Cadastro
    with tab[1]:
        st.header("Cadastro")
        name = st.text_input("🧑 Nome completo", key="signup_name")
        email = st.text_input("📧 Email", key="signup_email")
        password = st.text_input("🔑 Senha", type="password", key="signup_password")
        if st.button("Registrar", use_container_width=False, key="signup_button"):
            success, message = signup(name, email, password)
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
