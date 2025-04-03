import plotly.graph_objects as go
import pandas as pd
import numpy as np

def block_graphic_amount():
    # Gerando dados aleatórios
    np.random.seed(42)
    dias = pd.date_range(start="2024-08-01", periods=15, freq="D")
    patrimonio = np.linspace(14000, 11000, num=15) + np.random.normal(0, 300, size=15)

    # Criando o gráfico com Plotly
    fig = go.Figure()

    # Adicionando a linha do patrimônio
    fig.add_trace(go.Scatter(
        x=dias, 
        y=patrimonio, 
        mode="lines+markers", 
        name="Patrimônio",
        line=dict(color="cyan", width=2),
        marker=dict(size=6, color="cyan")
    ))

    # Layout
    fig.update_layout(
        title="Patrimônio",
        xaxis_title="Data",
        yaxis_title="Valor em R$",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        #plot_bgcolor="#1E1E2F",
        #paper_bgcolor="#1E1E2F",
        font=dict(color="white"),
        hovermode="x unified",
        margin=dict(l=40, r=40, t=40, b=40),
    )

    # Adicionando anotações (tooltip simulada)
    for i, (data, valor) in enumerate(zip(dias, patrimonio)):
        if i % 3 == 0:  # Simula pontos de destaque
            fig.add_trace(go.Scatter(
                x=[data], 
                y=[valor], 
                mode="markers+text",
                text=[f"R$ {valor:,.2f}"],
                textposition="top center",
                marker=dict(color="white", size=8)
            ))

    # Exibindo o gráfico
    return fig