import streamlit as st #interface gráfica
import pandas as pd # tratar dados
from sklearn.linear_model import LinearRegression # o tipo de treinamento que vou aplicaar 


st.title("Vendas")
st.header("Previsão de vendas ⌨️")


dados_vendas = pd.DataFrame({

    "investimentos": [100,200,300,550,750,800],
    "faturamento": [1200,2500,3700,3900,5500,6900]
})

st.write(dados_vendas)


# treinar os dados

X = dados_vendas[["investimentos"]]
Y = dados_vendas["faturamento"]

model = LinearRegression().fit(X,Y) # treina o modelo com os dados

investimento = st.number_input("Digite o faturamento", value = 150)

if investimento:
    if st.button("Analisar:"):
        previsao = model.predict([[investimento]])[0]
        st.write(f"Faturamento - previsao R$: {previsao:.2f} **")