
import streamlit as st

st.title("Dashboard de Vendas")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Vendas", "R$10K", "+5%", border=True)
with col2:
    st.metric("Clientes", "500", "+8%", border=True)
with col3:
    st.metric("Feedbacks", "80%", "-2%", border=True)


st.metric(label="", value="", delta="-2%", border=True)


st.title("Aplicativo de Exemplo")

tab1, tab2, tab3 = st.tabs(["Dados", "Gráficos", "Configurações"])

with tab1:
    st.write("Tabela de dados.")
    st.dataframe({"Coluna A": [1, 2], "Coluna B": [3, 4]})
with tab2:
    st.write("Gráfico de exemplo.")
    st.line_chart([1, 2, 3, 4])
with tab3:
    st.write("Configurações do aplicativo.")
    st.checkbox("Ativar Modo Escuro")


st.title("Análise de Dados")

# Filtros
st.sidebar.header("Filtros")
date = st.sidebar.date_input("Selecione a data")
category = st.sidebar.selectbox("Categoria", ["A", "B", "C"])

st.write(f"Você selecionou a data: {date} e a categoria: {category}")

# Gráfico
import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.randn(50, 3), columns=["A", "B", "C"])
st.line_chart(df)