import streamlit as st
import requests
import pandas as pd
from app.portfolio.dialog.asset_transaction import editar_ativo, asset_list
from datetime import datetime
from app.utils.constants import API_URL


def block_trading_history(wallet_id):
    st.subheader("Lançamento")
    # Obter o token de acesso
    access_token = "seu_access_token"  # Substitua por como você obtém o token
    headers = {"Authorization": f"Bearer {access_token}"}
    # Fazer uma requisição para obter os detalhes da carteira
    response = requests.get(f"{API_URL}/portfolio/transaction/{wallet_id}", headers=headers)
    json_asset_transaction = response.json()

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        json_asset_transaction = response.json()
        df_asset_transaction = pd.DataFrame(json_asset_transaction)
        
        # Verificar se há dados no DataFrame
        if not df_asset_transaction.empty:
            # Selecionar colunas relevantes para exibição

            list_asset = asset_list()
            dict_asset = {asset_data['id']:asset_data['symbol'] for asset_data in list_asset}
            df_asset_transaction["asset_name"] = df_asset_transaction["asset_id"].apply(lambda x: dict_asset.get(x, "-"))

            formatted_df = df_asset_transaction[["id", "date", "asset_name", "quantity", "unit_value", "purchase_value", "transaction_type_id"]].copy()
            formatted_df.rename(columns={
                "id": "ID",
                "date":"Data",
                "asset_name": "Ativo",
                "quantity": "Quantidade",
                "unit_value":"Valor Unitário",
                "purchase_value": "Preço (R$)",
                "transaction_type_id":"Evento"
            }, inplace=True)
            formatted_df["Preço (R$)"] = formatted_df["Preço (R$)"].apply(lambda x: f"R${x:.2f}")

            # Exibir cabeçalho
            header_col1, header_col2, header_col3, header_col4, header_col5, header_col6, header_col7, header_col8 = st.columns([1, 1, 2, 2, 2, 1, 1, 1])
            header_col1.write("**Data**")
            header_col2.write("**Ativo**")
            header_col3.write("**Quantidade**")
            header_col4.write("**Valor Unitário**")
            header_col5.write("**Preço (R$)**")
            header_col6.write("**Evento**")
            header_col7.write("**Editar**")
            header_col8.write("**Excluir**")

            # Exibir cada linha de negociação
            for index, row in formatted_df.iterrows():
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 1.5, 2, 2, 2, 1, 1, 1])
                col1.write(datetime.strptime(row["Data"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
                col2.write(row["Ativo"].replace(".SA", ""))
                col3.write(row["Quantidade"])
                col4.write(row["Valor Unitário"])
                col5.write(row["Preço (R$)"])
                col6.write(row["Evento"])


                # Botão Editar
                if col7.button("✏️", key=f"edit_{row['ID']}"):
                    editar_ativo(wallet_id, asset_transaction_id=row['ID'])
                    st.session_state["edit_id"] = row["ID"]  # Salvar o ID do ativo para edição
                    st.info(f"Edição acionada para o ativo {row['Ativo']} (ID: {row['ID']})")


                # Botão Excluir
                if col8.button("🗑️", key=f"delete_{row['ID']}"):
                    with st.spinner("Excluindo negociação..."):
                        delete_response = requests.delete(f"{API_URL}/portfolio/transaction/delete/{row['ID']}")
                            #delete_response = requests.delete(f"{API_URL}/portfolio/transaction/{row['ID']}", headers=headers)
                        if delete_response.status_code == 200:
                            st.success(f"Ativo {row['Ativo']} excluído com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao excluir o ativo {row['Ativo']}.")

        else:
            st.warning("Nenhuma negociação encontrada.")
    else:
        st.error("Erro ao buscar o histórico de negociações.")


def block_wallet_info(analyze_transactions):
    # Dados para exibição
    # CSS para estilizar os blocos
    st.markdown(
        """
        <style>
        .wallet-block {
            background-color: #1E1E2F; /* Fundo escuro */
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            color: white;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        }
        .wallet-title {
            font-size: 16px;
            font-weight: bold;
            color: #B0B0C3; /* Cinza claro */
        }
        .wallet-value {
            font-size: 28px;
            font-weight: bold;
            margin-top: 10px;
        }
        .wallet-red {
            color: red;
            font-weight: bold;
        }
        .wallet-green {
            color: green;
            font-weight: bold;
        }
        .wallet-icon {
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    valor_aplicado = analyze_transactions['total_invested']
    saldo_bruto = analyze_transactions['total_portfolio_value']
    variacao = analyze_transactions['profitability']
    # Layout com colunas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="wallet-block">
                <img src="https://img.icons8.com/color/100/money-bag.png" class="wallet-icon" width="50"/>
                <div class="wallet-title">VALOR APLICADO</div>
                <div class="wallet-value">R$ {valor_aplicado:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="wallet-block">
                <img src="https://img.icons8.com/color/100/money-bag.png" class="wallet-icon" width="50"/>
                <div class="wallet-title">SALDO BRUTO</div>
                <div class="wallet-value">R$ {saldo_bruto:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        color = "green" if variacao>0 else 'red'
        st.markdown(
            f"""
            <div class="wallet-block">
                <img src="https://img.icons8.com/color/100/money-bag.png" class="wallet-icon" width="50"/>
                <div class="wallet-title">VARIAÇÃO</div>
                <div class="wallet-value wallet-{color}"> R$ {(saldo_bruto-valor_aplicado):,.2f} | {variacao}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
