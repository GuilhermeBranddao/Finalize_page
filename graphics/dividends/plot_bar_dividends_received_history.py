import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime


## DIVIDENDOS
def create_periods_barras(qtd_periods_barras=24):
    data_hoje = datetime.now().strftime('%b-%Y')
    data_inicial = pd.to_datetime(data_hoje, format='%b-%Y')
    intervalo_datas = pd.date_range(end=data_inicial, periods=qtd_periods_barras, freq='ME')
    datas_formatadas = list(intervalo_datas.strftime('%b-%Y'))
    datas_formatadas.append(data_hoje)
    return pd.DataFrame([{'asset_name': '_',
                'mes': 0,
                'ano': 0,
                'dividends': 0,
                'mes-map': '-',
                'mes-ano':mes_ano} for mes_ano in datas_formatadas])

def plot_recebimentos_ativo_mes(df_historico_dividendos, target_receive_dividends=None, is_web=False):
    """
    Recebe: Dataframe de histórico de dividendos

    Retorna: plot com gráfico de barras dos dividendos recebidos no período
    """
    df_historico_dividendos["dividends_received_total"] = df_historico_dividendos["quantity"] * df_historico_dividendos["dividends"]
    if isinstance(df_historico_dividendos, pd.DataFrame):

        df = df_historico_dividendos.copy()

        # Converter a coluna 'date_pagamento' para o tipo 'datetime'

        df['date'] = pd.to_datetime(df['date'])

        # Extrair o mês e o ano da coluna 'date' em duas novas colunas
        df['mes'] = df['date'].dt.month
        df['ano'] = df['date'].dt.year

        # Agregar os valores recebidos por ativo, mês e ano
        df_agregado = df.groupby(['asset_name', 'mes', 'ano'])['dividends_received_total'].sum().reset_index()

        # Mapear números de mês para os rótulos desejados
        mes_labels = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}

        # Substituir os números de mês pelos rótulos
        df_agregado['mes-map'] = df_agregado['mes'].map(mes_labels)

        # df_agregado['mes-ano'] = df_agregado['mes-map'].astype(str) + "-" + df_agregado['ano'].astype(str)
        df_agregado['mes-ano'] = pd.to_datetime(df_agregado['ano'].astype(str) + df_agregado['mes'].astype(str), format='%Y%m')
        df_agregado['mes-ano'] = df_agregado['mes-ano'].dt.strftime('%b-%Y')

        df_agregado = pd.concat([df_agregado, create_periods_barras(qtd_periods_barras=17)], ignore_index=True)

    else:
        df_agregado = create_periods_barras(qtd_periods_barras=17)

    # Ordenar o DataFrame pela coluna 'mes' e 'ano'
    df_agregado.sort_values(by=["ano", "mes"], ascending=True, inplace=True)
    df_agregado = df_agregado[df_agregado['asset_name']!="_"]
    #df_agregado.reset_index(drop=True, inplace=True)
    # df_agregado.reset_index(drop=True, inplace=True)

    # Criar o gráfico de barras no Plotly
    
    fig = px.bar(df_agregado, x='mes-ano', y='dividends_received_total', color='asset_name',
                labels={'dividends_received_total': 'Valor Recebido R$', 'mes-ano': 'Mês'},
                title='Dividendos recebido por mês',
                category_orders={"mes-ano": df_agregado['mes-ano']}
                )
    espaco_entre_barras = 0.1
    fig.update_layout(
        bargap=espaco_entre_barras,
        yaxis_tickformat=".2f"  # Define o formato com duas casas decimais
        )

    # Adicionar linha horizontal para representar a meta
    if target_receive_dividends is not None:
        fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=df_agregado['mes-ano'].iloc[0],
                x1=df_agregado['mes-ano'].iloc[-1],
                y0=target_receive_dividends,
                y1=target_receive_dividends,
                line=dict(color="red", width=2),
            )
        )
    
    
    # Adicionar rótulos de texto no topo de cada barra
    for i, row in df_agregado.groupby(['mes-ano'])['dividends_received_total'].sum().reset_index().iterrows():
        if row['dividends_received_total'] != 0:
            fig.add_annotation(
                go.layout.Annotation(
                    x=row['mes-ano'],
                    y=row['dividends_received_total'],
                    text='',  # f"R${row['recebidos']:.2f}",  # Exibe o valor com duas casas decimais
                    showarrow=False,
                    arrowhead=0,
                    ax=0,
                    ay=-30,
                    # yshift=10,
                    font=dict(size=14)
                    )
            )

    max = df_agregado.groupby(['mes-ano'])['dividends_received_total'].sum().max()
    
    fig.update_yaxes(range=[0, max])
    # fig.update_xaxes(tickangle=45)
    if is_web:
        return fig.to_html()
    
    return fig