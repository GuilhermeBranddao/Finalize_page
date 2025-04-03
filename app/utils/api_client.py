import requests
from app.utils.constants import API_URL
import streamlit as st
from datetime import datetime
import logging
import requests
import streamlit as st
from app.auth.login_page import cookies

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def make_request(
    method: str,
    endpoint: str,
    data=None,
    headers=None,
    message_except: str = "Ocorreu um erro inesperado.",
    log_level: str = "ERROR",
):
    """
    Faz uma requisição à API.

    Args:
        method (str): Método HTTP (GET, POST, PUT, DELETE, etc.).
        endpoint (str): Endpoint da API.
        data (dict, optional): Dados a serem enviados na requisição. Default é None.
        headers (dict, optional): Headers HTTP da requisição. Default é None.
        message_except (str, optional): Mensagem de exceção personalizada. Default é "Ocorreu um erro inesperado.".
        log_level (str, optional): Nível do log (INFO, WARNING, ERROR). Default é "ERROR".

    Returns:
        dict | None: Resposta da API em formato JSON, ou None em caso de falha.
    """
    url = f"{API_URL}{endpoint}"
    try:
        # Seleção do método HTTP
        if method.upper() == "GET":
            response = requests.get(url, params=data, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, data=data)
        else:
            raise ValueError(f"Método HTTP inválido: {method}")

        # Levanta exceções para status HTTP 4xx/5xx
        response.raise_for_status()

        # Verifica se há resposta JSON
        if response.status_code == 200:
            logging.info(f"Requisição bem-sucedida: {method} {url}")
            return response.json()
        else:
            if log_level.upper() == "WARNING":
                st.warning(f"Resposta recebida, mas sem conteúdo esperado: {response.status_code}")
                logging.warning(f"Resposta inesperada: {method} {url} - Status: {response.status_code}")
            return None

    except requests.exceptions.HTTPError as http_err:
        st.error(f"{message_except} - Erro HTTP: {http_err}")
        logging.error(f"Erro HTTP: {method} {url} - {http_err}")
        return None

    except requests.exceptions.ConnectionError as conn_err:
        st.error(f"{message_except} - Erro de conexão: {conn_err}")
        logging.error(f"Erro de conexão: {method} {url} - {conn_err}")
        return None

    except requests.exceptions.Timeout as timeout_err:
        st.error(f"{message_except} - Timeout: {timeout_err}")
        logging.error(f"Timeout: {method} {url} - {timeout_err}")
        return None

    except requests.exceptions.RequestException as req_err:
        st.error(f"{message_except} - Erro inesperado: {req_err}")
        logging.error(f"Erro inesperado: {method} {url} - {req_err}")
        return None

    except ValueError as val_err:
        st.error(f"Erro: {val_err}")
        logging.error(f"Erro no método: {val_err}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return None
    

def get_asset_list():
    """Obtém a lista de ativos."""
    return make_request("GET", "/portfolio/asset/list")

# Função para buscar o preço de fechamento médio previsto
def get_pred_price_close(asset_id: int, date: str = datetime.now().strftime("%Y-%m-%d")) -> float:
    response_json = make_request("GET", 
                                    f"/portfolio/get-price-class/?asset_id={asset_id}&date={date}",
                                    message_except=f"Erro ao buscar preço para o ativo {asset_id}.", 
                                    log_level="ERROR")
    if not response_json:
        return 
    return response_json.get("average_close", None)
    

def get_wallets():
    """Obtém a lista de carteiras da API."""
    access_token = cookies.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    response_json = make_request(method="GET", endpoint="/portfolio/list", headers=headers)
    if not response_json:
        return []

    return response_json