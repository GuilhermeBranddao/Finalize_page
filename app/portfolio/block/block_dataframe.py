import streamlit as st
from datetime import date

def dividends_received_per_month(assets_dividends_received_per_date):
    st.dataframe(
            assets_dividends_received_per_date,
            column_config={
                "date": st.column_config.DateColumn(
                    "Data",
                    min_value=date(1900, 1, 1),
                    max_value=date(2005, 1, 1),
                    format="DD/MM/YYYY",
                    step=1,
                ),
                "asset_name": st.column_config.Column(
                    "Nome do ativo",
                    help="Nome do ativo",
                    width="medium",
                    required=True,
                ),
                "quantity": st.column_config.Column(
                    "Quantidade",
                    help="A quantidade de ativos",
                    width="medium",
                    required=True,
                ),
                "dividends": st.column_config.NumberColumn(
                    "Dividendos por cota",
                    help="O valor dos dividendos por cota",
                    min_value=0.0001,
                    max_value=1000000,
                    step=0.0001,
                    format="R$%.3f",
                ),
                "dividends_received_total": st.column_config.NumberColumn(
                    "Dividendos Recebidos",
                    help="O total de dividendos recebidos (em BRL)",
                    min_value=0.0001,
                    max_value=1000000,
                    step=0.0001,
                    format="R$%.2f",
                )

            },
            hide_index=True,
            use_container_width=False,
        )
