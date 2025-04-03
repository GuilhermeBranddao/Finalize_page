import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import requests
from typing import List, Dict
from datetime import datetime
from app.portfolio.dialog.asset_transaction import adicionar_ativo, asset_list

from app.portfolio.block.block_trading_history import block_trading_history, block_wallet_info
from app.portfolio.block.block_graphic import block_graphic_amount
from app.portfolio.block.block_dataframe import dividends_received_per_month
from app.utils.util import classify_asset
from graphics.dividends.plot_bar_dividends_received_history import plot_recebimentos_ativo_mes
from st_aggrid import AgGrid
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import numpy as np
from app.utils.profitability import calcular_rentabilidade_mensal
from app.utils.api_client import get_asset_list, get_pred_price_close, make_request
from app.utils.constants import API_URL

def generate_asset_analysis_report(asset_id):
    response = requests.get(f"{API_URL}/portfolio/generate-asset-analysis-report/{asset_id}")
    if not response.status_code == 200:
        return {}
    
    return response.json()

# Função para analisar transações do portfólio
def analyze_portfolio_transactions(df_transactions: pd.DataFrame) -> Dict:
    """
    Analyze portfolio transactions and calculate key metrics such as total investment,
    portfolio value, profitability, profitability per asset, and portfolio distribution.

    Args:
        transactions (pd.DataFrame): A Data Frame containing transaction data. 
                                   Each dictionary must have the following keys:
                                   - asset_id: The ID of the asset.
                                   - transaction_type_id: 0 for purchase, 1 for sale.
                                   - purchase_value: Total value of the purchase.
                                   - quantity: Number of units purchased.
                                   - asset_id: Identifier for the asset.

    Returns:
        Dict: A dictionary containing the following metrics:
              - total_invested: Total amount invested in purchases.
              - total_portfolio_value: Current total value of the portfolio.
              - profitability: Portfolio profitability as a percentage.
              - profitability_per_asset: Profitability of each asset as a percentage.
              - portfolio_distribution: Current distribution of the portfolio by asset.
    """
    if df_transactions.empty:
        raise ValueError("The transactions list cannot be empty.")
    
    required_columns = {"asset_id", "transaction_type_id", "purchase_value", "quantity"}
    if not required_columns.issubset(df_transactions.columns):
        raise ValueError(f"The transactions data must include the following columns: {required_columns}")

    # Update values with the current price of each asset
    df_transactions["unit_value_today"] = df_transactions["asset_id"].apply(get_pred_price_close)
    df_transactions["purchase_value_today"] = df_transactions["unit_value_today"] * df_transactions["quantity"]

    # Calculate total invested value (only for purchases)
    total_invested = df_transactions[df_transactions["transaction_type_id"] == 0]["purchase_value"].sum()

    # Calculate current portfolio value
    total_portfolio_value = df_transactions["purchase_value_today"].sum()

    # Calculate overall profitability
    if total_invested == 0:
        profitability = 0.0  # Avoid division by zero
    else:
        profitability = round(((total_portfolio_value * 100) / total_invested) - 100, 2)

    # Calculate profitability per asset
    profitability_per_asset = (
        df_transactions.groupby("asset_id").apply(
            lambda group: round(
                ((group["purchase_value_today"].sum() * 100) / group["purchase_value"].sum()) - 100, 2
            ) if group["purchase_value"].sum() > 0 else 0.0
        ).to_dict()
    )

    # Calculate portfolio distribution
    portfolio_distribution = (
        df_transactions.groupby("asset_id")["purchase_value_today"].sum().to_dict()
    )

    # Return results as a dictionary
    return {
        "total_invested": total_invested,
        "total_portfolio_value": total_portfolio_value,
        "profitability": profitability,
        "profitability_per_asset": profitability_per_asset,
        "portfolio_distribution": portfolio_distribution,
    }

# Função principal da página
def page_switch_carteira(wallet_id: int):
    """
    Exibe a página de resumo da carteira de investimentos.

    Args:
        wallet_id (int): ID da carteira.
    """
    # Requisição para obter o histórico da carteira
    response_json = make_request(
        method="GET",
        endpoint=f"/portfolio/history/{wallet_id}",
        log_level="WARNING",
    )
    
    if not response_json:
        st.warning("Nenhuma negociação encontrada.")
        return

    df_historico_dividendos = pd.DataFrame(response_json)
    if df_historico_dividendos.empty:
        st.warning("Nenhuma negociação encontrada.")
        return

    # Obter lista e dicionário de ativos
    list_asset = asset_list()
    dict_asset = {asset_data['id']: asset_data['symbol'] for asset_data in list_asset}

    # Filtrar transações e categorizar ativos
    df_transaction = df_historico_dividendos[df_historico_dividendos['transaction_type_id'] == 0].copy()
    df_transaction['category'] = df_transaction['asset_name'].apply(classify_asset)

    # Analisar transações
    analyze_transactions = analyze_portfolio_transactions(df_transaction)

    # Renderizar informações da carteira
    block_wallet_info(analyze_transactions)

    st.title("Resumo da Carteira de Investimentos")
    tabs = st.tabs([
        "Resumo", 
        "Proventos", 
        "Lançamentos", 
        "Info Ativos", 
        "Rentabilidade", 
        "Configurações"
    ])

    # Renderização de cada aba
    render_tab_resumo(tabs[0], df_transaction, analyze_transactions, dict_asset, df_historico_dividendos)
    render_tab_proventos(tabs[1], df_historico_dividendos)
    render_tab_lancamentos(tabs[2], wallet_id)
    render_tab_info_ativos(tabs[3], wallet_id, df_transaction)
    render_tab_rentabilidade(tabs[4], df_historico_dividendos)
    render_tab_config(tabs[5])

def render_tab_resumo(tab, df_transaction, analyze_transactions, dict_asset, df_historico_dividendos):
    """
    Renderiza a aba de Resumo.

    Args:
        tab (streamlit.tab): Aba correspondente.
        df_transaction (pd.DataFrame): Dados das transações.
        analyze_transactions (dict): Análise das transações.
        dict_asset (dict): Mapeamento de IDs para símbolos de ativos.
        df_historico_dividendos (pd.DataFrame): Histórico de dividendos.
    """
    with tab:
        st.markdown("<h2 style='text-align: center; color:rgb(193, 199, 201);'>Resumo da Carteira</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)


        with col1:
            st.subheader("Distribuição da Carteira")
            fig = px.pie(
                df_transaction, 
                names="category", 
                values="purchase_value", 
                title="Distribuição por Tipo", 
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Rentabilidade por Categoria")
            list_asset_names = [dict_asset.get(asset_id, "Desconhecido") for asset_id in analyze_transactions["profitability_per_asset"]]

            df_profit = pd.DataFrame({
                "category": list(list_asset_names),
                "profitability": list(analyze_transactions["profitability_per_asset"].values())
            })
            fig = px.bar(df_profit, x="category", y="profitability", color="category", title="Rentabilidade (%)")
            st.plotly_chart(fig, use_container_width=True)
        with col3:
            fig = block_graphic_amount()
            st.plotly_chart(fig, use_container_width=True)
    
def render_tab_rentabilidade(tab, df_historico_dividendos):
    with tab:
        st.subheader("Rentabilidade")

        st.selectbox(label="Ativo", options=["Todos", "MXRF11", "IRDM11"], 
            placeholder="Selecione um ativo",
            key="asset_selected")
        
        df_pivot = calcular_rentabilidade_mensal(df_historico_dividendos)

        st.dataframe(df_pivot, use_container_width=True)
        st.subheader("HISTÓRICO MENSAL")
        
def render_tab_proventos(tab, df_historico_dividendos:pd.DataFrame):
    with tab:
        st.subheader("Histórico de Dividendos")
        fig = plot_recebimentos_ativo_mes(df_historico_dividendos)
        st.plotly_chart(fig, use_container_width=True)

        df_historico_dividendos["date"] = pd.to_datetime(df_historico_dividendos["date"])
        df_historico_dividendos.sort_values(by="date", inplace=True, ascending=False)

        # Filtrar os dividendos do mês atual
        df_dividendos_mes = df_historico_dividendos[
            (df_historico_dividendos["date"].dt.month == datetime.now().month) &    # Mês atual
            (df_historico_dividendos["date"].dt.year == datetime.now().year)       # Ano atual
        ].copy()


        assets_dividends_received_per_date = df_dividendos_mes[df_dividendos_mes['dividends_received_total']>0]
        assets_dividends_received_per_date.reset_index(drop=True, inplace=True)

        columns = ["date", 'asset_name', "quantity", "dividends", "dividends_received_total"]
        assets_dividends_received_per_date = assets_dividends_received_per_date[columns]

        dividends_received_per_month(assets_dividends_received_per_date)
        #st.dataframe(assets_dividends_received_per_date[columns],  use_container_width=True)


# Função para renderizar a aba 3
def render_tab_lancamentos(tab, wallet_id):
    with tab:
        block_trading_history(wallet_id)

def render_tab_info_ativos(tab, wallet_id, df_transaction):
    with tab:
        # Usa ThreadPoolExecutor para paralelismo
        with ThreadPoolExecutor() as executor:
            asset_reports = list(executor.map(generate_asset_analysis_report, df_transaction["asset_id"]))


        df_response = pd.DataFrame(asset_reports)

        #st.dataframe(df_response, use_container_width=True)

        st.data_editor(
            df_response,
            column_config={
                "monthly_percentage_variation": st.column_config.ListColumn(
                    "Variação do Ativo % (last 6 months)",
                    help="A valorização do ativo nos últimos 5 meses",
                    width="medium",
                ),
            },
            hide_index=True,
        )

def render_tab_config(tab):
    with tab:
        st.write("Configurações")
        st.checkbox("Ativar Modo Escuro")
