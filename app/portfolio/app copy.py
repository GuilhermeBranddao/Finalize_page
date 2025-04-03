import streamlit as st
import pandas as pd

st.header("Pagina Principal")

with st.form("my_form"):
    st.write("Adicionar Transação")

    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    tipo_ativo = st.selectbox(label="Qual o evento?", options=["Ações", "Fund. Invest", "FIIs", "Cripto"])
    evento = st.selectbox(label="Qual o evento?", options=["Compra", "Venda"])

    st.write("Data da Compra")
    st.write("Quantidade")
    st.write("Preço em R$")
    st.write("Outros custos")
    st.write("Valor total R$ 0.00")
    
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:

        dict_transaction = {"tipo_ativo":tipo_ativo,
                            "evento":evento}
        df = pd.DataFrame([dict_transaction])
        df.to_csv('transação.csv', index=False)

        st.write("slider", slider_val, "checkbox", checkbox_val)


st.write("Outside the form")