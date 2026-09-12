import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression


st.title("Análise")
st.header("Sistema de vendas - mês de setembro ⌨️")

dados = pd.read_csv("vendas.csv")

st.write("Dados de vendas:")
st.dataframe(dados)

dados = pd.read_csv("vendas.csv")

X = dados[["mes"]]
Y = dados["vendas"]


model = LinearRegression().fit(X, Y)


previsao = model.predict([[9]])[0]

st.subheader("Previsão para setembro")
st.write(f"Vendas previstas: {previsao:.2f}")
