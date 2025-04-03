import streamlit as st
import requests
from app.portfolio.pages.page_investidor_10 import page_switch_carteira
from app.portfolio.dialog.nova_carteira import nova_carteira
from app.portfolio.dialog.delete_wallet import delete_wallet

from streamlit.runtime.scriptrunner import add_script_run_ctx
from app.portfolio.dialog.asset_transaction import adicionar_ativo
from app.utils.api_client import get_wallets, get_pred_price_close, make_request
from app.portfolio.block.buttons import render_choose_wallet_buttons


def config_query_params():
    """Configura os parâmetros de consulta e navega para a página da carteira, se necessário."""
    wallet_id = st.session_state.get("wallet_id", None)
    if wallet_id:
        page_switch_carteira(wallet_id)

def render_carteiras():
    """Renderiza a seção de carteiras."""
    st.title("Carteiras")

    # Indicador de carregamento
    with st.spinner("Carregando carteiras..."):
        wallets = get_wallets()

    if not wallets:
        st.warning("Nenhuma carteira disponível. Crie uma nova para começar!")
             
    # Seção de carteiras
    col_choice_wallet, col_add_asset = st.columns([1, 1])
    with col_choice_wallet:
        with st.expander("Carteiras"):
            render_choose_wallet_buttons(wallets)

    # Ação para adicionar ativo
    with col_add_asset:
        wallet_id = st.session_state.get("wallet_id", None)
        if st.button("Adicionar Ativo", key="add_asset", disabled=not bool(wallet_id)):
            adicionar_ativo(wallet_id)
            #st.write(f"Adicionar ativo na carteira: {wallet_id}")
            
        if not wallet_id:
            st.info("Selecione uma carteira para adicionar ativos.")

    # Configurar query params
    config_query_params()