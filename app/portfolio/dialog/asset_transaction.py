import streamlit as st
from datetime import datetime
from app.auth.login_page import cookies
from app.utils.date_utils import is_valid_date, format_date
from app.utils.api_client import get_asset_list, get_pred_price_close, make_request
from typing import Dict

#### Utils
def handle_api_response(response, success_message):
    if not response:
        st.error("Erro: Nenhuma resposta recebida.")
        return False
    if "error" in response:
        st.error(f"Erro: {response['error']}")
        return False
    st.success(success_message)
    return True

def add_transaction(data):
    access_token = cookies.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response_json = make_request(method="POST", endpoint="/portfolio/transaction/add", data=data, headers=headers)
    if handle_api_response(response_json, "Transação salva com sucesso!"):
        st.rerun()

def edit_transaction(data):
    response_json = make_request("PUT", f"/portfolio/asset-transaction/edit", data)
    display_response_message(response_json, "Transação salva com sucesso!")
    st.rerun()


def asset_list():
    response_json = make_request(method="GET", endpoint="/portfolio/asset/list")
    return response_json

def get_pred_price_close(asset_id:int, date:str):
    """/portfolio/get-price-class/?asset_id=1&date=2023-01-01"""
    response_json = make_request(method="GET", endpoint=f"/portfolio/get-price-class/?asset_id={asset_id}&date={date}")
    return response_json

# Função para obter os ativos disponíveis e organizá-los
def get_assets_with_options(default_selection="Selecione um ativo"):
    list_assets = get_asset_list()
    if not list_assets or "error" in list_assets:
        st.error("Erro ao carregar ativos.")
        return {}, [default_selection], {}, {}

    asset_dict = {asset["symbol"]: asset["id"] for asset in list_assets}
    asset_dict_start_date = {asset["symbol"]: asset.get("start_date", None) for asset in list_assets}
    asset_dict_end_date = {asset["symbol"]: asset.get("end_date", None) for asset in list_assets}

    asset_options = [default_selection] + list(asset_dict.keys())
    return asset_dict, asset_options, asset_dict_start_date, asset_dict_end_date

def calculate_total_value(quantity, unit_price, additional_costs):
    quantity = quantity or 0
    unit_price = unit_price or 0
    additional_costs = additional_costs or 0
    return quantity * unit_price + additional_costs

# Função para exibir mensagens de erro ou sucesso
def display_response_message(response, success_message):
    if "error" in response:
        st.error(f"Erro: {response['error']}")
    else:
        st.success(success_message)

##### FIM

### Campos
def op_date(label="Data da transação", 
            default_date=datetime.now().date(), 
            max_date=datetime.now().date(),
            min_date=None):

    """Input para seleção de data com validação."""
    date_selected = st.date_input(label, value=default_date, 
                                  max_value=max_date, 
                                  key="data",
                                  min_value=min_date
                                  )
    if not is_valid_date(date_selected):
        st.error("⚠️ Data inválida! Escolha um dia útil.")
    return date_selected

# Função para exibir e selecionar o tipo de transação
def exibir_tipo_transacao(tipo_transacao_atual=None):
    return st.radio(
        "Tipo de transação",
        ["Compra", "Venda"],
        index=0 if tipo_transacao_atual == 0 else 1 if tipo_transacao_atual == 1 else 0,
        horizontal=True
    )

# Função para exibir e selecionar um ativo
def selecionar_ativo(asset_dict, asset_options, asset_atual=None):
    if asset_atual:
        index_inicial = asset_options.index(next(key for key, value in asset_dict.items() if value == asset_atual))
    else:
        index_inicial = 0
    return st.selectbox(
        "Código do Ativo",
        asset_options,
        index=index_inicial,
        key="nome_ativo"
    )

# Função para entrada de quantidade e valores
def entrada_valores(asset_id, transaction:Dict={}, start_date=None, end_date=datetime.now().date()):
    col1, col2 = st.columns(2)
    with col1:
        date = op_date(
            default_date= transaction.get("date", end_date),
            max_date=end_date,
            min_date=start_date
        )
    with col2:
        quantidade = st.number_input("Quantidade", 
                                     min_value=1, 
                                     step=1, 
                                     key="quantidade", 
                                     value=transaction.get("quantity", 1),
                                     help="Digite a quantidade de ativos comprados.")

    col3, col4 = st.columns(2)
    with col3:
        # Obtendo preço previsto
        value = get_pred_price_close(asset_id=asset_id, date=format_date(date))
        if value and "average_close" in value:
            preco = st.number_input(
                "Valor Unitário R$", 
                min_value=0.0,
                key="preco",
                value=transaction.get("unit_value", value["average_close"]),
                help="Valor unitario por ativo."
            )
        else:
            st.warning("Valor previsto não disponível.")
            preco = st.number_input("Valor Unitário R$", min_value=0.0,
                                    key="preco",
                                    value=transaction.get("unit_value", 0.0),
                                    help="Preço sugerido com base no fechamento mais recente.")
    with col4:
        custos = st.number_input("Outros custos", 
                                min_value=0.0, 
                                step=0.50, 
                                key="custos", 
                                value=transaction.get("additional_costs", 0.0),
                                help="Informe custos adicionais relacionados à compra.")

    valor_total = calculate_total_value(quantidade, preco, custos)
    st.markdown(f"**Valor total: R$ {valor_total:,.2f}**")

    return {"quantidade":quantidade, 
            "preco":preco,
            "custos":custos, 
            "valor_total":valor_total, 
            "date":date}
####

# Modal para adicionar ativo
@st.dialog("Adicionar Ativo")
def adicionar_ativo(wallet_id, asset_transaction_id=None):
    """
    Modal para adicionar transações de ativos.
    
    Exibe campos para seleção de tipo de transação, ativo, data, quantidade, 
    valores e custos, com validações e integração de API.
    """

    transaction = {}
    if asset_transaction_id:
        transaction = make_request("GET", f"/portfolio/get-asset-transaction/{asset_transaction_id}")

    asset_dict, asset_options, asset_dict_start_date, asset_dict_end_date = get_assets_with_options()

    tipo_transacao = exibir_tipo_transacao(tipo_transacao_atual=transaction.get("transaction_type_id", None))
    selected_asset = selecionar_ativo(asset_dict, asset_options, asset_atual=transaction.get("asset_id", None))

    if selected_asset == "Selecione um ativo":
        st.warning("Por favor, selecione um ativo.")
        return

    asset_category = "FII"  # Adapte para obter dinamicamente, se necessário
    st.info(f"**Tipo do ativo:** {asset_category}")
    
    result = entrada_valores(asset_id=asset_dict[selected_asset],
                    start_date=asset_dict_start_date[selected_asset],
                    end_date=asset_dict_end_date[selected_asset])

    if st.button(f"Salvar"):
        data = {
            "quantity": result.get("quantidade", None),
            "unit_value": result.get("preco", None),
            "purchase_value": result.get("valor_total", None),
            "date": format_date(result.get("date", None)),
            "portfolio_id": wallet_id,
            "transaction_type_id": 0 if tipo_transacao == "Compra" else 1,
            "asset_id": asset_dict[selected_asset],
        }  
        add_transaction(data)
        

@st.dialog("Editar Ativo")
def editar_ativo(wallet_id, asset_transaction_id=None):
    """
    Modal para adicionar transações de ativos.
    
    Exibe campos para seleção de tipo de transação, ativo, data, quantidade, 
    valores e custos, com validações e integração de API.
    """

    transaction = {}
    if asset_transaction_id:
        transaction = make_request("GET", f"/portfolio/get-asset-transaction/{asset_transaction_id}")
    else:
        st.error("⚠️ asset_transaction_id ausente")

    asset_dict, asset_options, asset_dict_start_date, asset_dict_end_date = get_assets_with_options()

    tipo_transacao = exibir_tipo_transacao(tipo_transacao_atual=transaction.get("transaction_type_id", None))
    selected_asset = selecionar_ativo(asset_dict, asset_options, asset_atual=transaction.get("asset_id", None))

    if selected_asset == "Selecione um ativo":
        st.warning("Por favor, selecione um ativo.")
        return

    asset_category = "FII"  # Adapte para obter dinamicamente, se necessário
    st.info(f"**Tipo do ativo:** {asset_category}")
    
    result = entrada_valores(asset_id=asset_dict[selected_asset],
                    start_date=asset_dict_start_date[selected_asset],
                    end_date=asset_dict_end_date[selected_asset], 
                    transaction=transaction)

    if st.button("Salvar"):
        updated_data = {
            'id': asset_transaction_id,
            "quantity": result.get("quantidade", None),
            "unit_value": result.get("preco", None),
            "purchase_value": result.get("valor_total", None),
            "date": format_date(result.get("date", None)),
            'portfolio_id': wallet_id,
            'transaction_type_id': 0 if tipo_transacao == "Compra" else 1,
            'asset_id': asset_dict[selected_asset],
        }
        edit_transaction(data=updated_data)
