
import streamlit as st #interface gráfica
import pandas as pd # tratar dados
from sklearn.linear_model import LinearRegression # o tipo de treinamento que vou aplicaar 


dados = pd.read_csv("vendas.csv")

df = pd.DataFrame(dados)

st.write(dados)
# analisar a previsão de vendas do mes de setembro