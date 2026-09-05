import streamlit as st
import pandas as pd

st.title("Visualizador de Planilhas")

st.header("Dados dos alunos")

dados = {
    "Nome": ["Ana", "João", "Maria", "Pedro"],
    "Idade": [20, 22, 19, 25],
    "Curso": ["Policial", "Engenheiro", "Bombeiro", "Cozinheiro"],
    "Nota": [8.5, 7.0, 9.2, 6.5]
}

df = pd.DataFrame(dados)

st.subheader("Tabela interativa")

st.dataframe(df)

st.subheader("Tabela estática")

st.table(df)
