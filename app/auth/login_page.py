import streamlit as st
from app.utils.constants import API_URL
import requests
# Configurações do Streamlit
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    password="chave-secreta-para-encriptar2"  # Substitua por algo mais seguro
)

if not cookies.ready():
    print(">>>>> Cookies não inicializados ❌")
    st.spinner()
    st.stop()
else:
    print(">>>>> Cookies inicializados ✅")

# Função para autenticar o usuário
def login(email, password):
    url = f"{API_URL}/auth/token"
    data = {"username": email, "password": password}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        response_json = response.json()

        if response.status_code == 200:
            cookies["access_token"] = response_json.get("access_token", None)
            cookies.save()
            st.success("✅ Login realizado com sucesso!")
            st.rerun()
    except requests.exceptions.RequestException as e:
        st.error("❌ Credenciais inválidas. Tente novamente.")


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

    # if not "access_token" in cookies:
        # return False
    
    access_token = cookies.get("access_token", None)
    
    # headers = {"Authorization": f"Bearer {access_token}"}
    access_cookies={"access_token": access_token}
    try:
        response = requests.get(url, cookies=access_cookies)
        # response = requests.post(url, headers=headers)
        return response.json().get("valid", False)
    except requests.RequestException:
        return False

# Função para realizar o logout
def logout():
    del cookies["access_token"] # Apaga cookie
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

    #if is_authenticated():
    #    st.success("✅ Você já está autenticado!")
    #    if st.button("🔓 Sair"):
    #        logout()
    #    return

    # Abas para alternar entre Login e Cadastro
    tab = st.tabs(["🔑 Login", "📝 Cadastro"])
    
    # Aba de Login
    with tab[0]:
        st.header("Login")
        email = st.text_input("📧 Email", key="login_email")
        password = st.text_input("🔑 Senha", type="password", key="login_password")
        if st.button("Entrar", use_container_width=False, key="login_button"):
            login(email, password)

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
