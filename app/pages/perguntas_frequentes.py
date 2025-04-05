import streamlit as st

def show():
    st.title("Perguntas Frequentes")

    with st.expander("O que é este app?"):
        st.write("Este é um exemplo de layout com acordeão.")
    with st.expander("Como usar?"):
        st.write("Selecione as opções no menu e explore os recursos.")
    with st.expander("Contato"):
        st.write("Entre em contato pelo e-mail: exemplo@empresa.com")