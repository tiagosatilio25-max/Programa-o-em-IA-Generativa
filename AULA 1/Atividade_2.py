import streamlit as st

st.title("Dados do Usuário 🎲")

st.header("Olá seja bem vindo, por favor preencha seus dados 😁")

nome = st.text_input("Informe seu nome:")
idade = st.number_input("Idade:", min_value=0)
termos = st.checkbox("Aceitar termos de uso")

if st.button("Enviar dados"):
    enviar = "Nome: " + nome + " \nidade: " + str(idade)
    st.info(enviar)