import streamlit as st
import pandas as pd

st.markdown("""
<style>
    .stApp {
        background-color: black;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("Minha aplicação")

#procoding -> não utiliza IA generativa
dados = pd.read_csv("vendas.csv")

st.header("Calculadora STEAMLIT")
st.write("Adicione os números para calcular👌🧮")

n1 = st.number_input("Digite um número:", min_value=0)
n2 = st.number_input("Digite o segundo número:", value=0)

soma_, div_, sub_, mult_ = st.columns(4)

if soma_.button("+"):
    soma = n1 + n2
    st.info(soma)

elif sub_.button("-"):
    sub = n1 - n2
    st.info(sub)

elif mult_.button("×"):
    mult = n1 * n2
    st.info(mult)

elif div_.button("÷"):
        div = n1 / n2
        st.info(div)



st.map()

st.header("Analise de dados 🎲")

st.table(dados)

st.bar_chart(dados, x="ano", y="lucro")

st.scatter_chart(dados, x="venda", y="lucro")

st.line_chart(dados, x="ano", y="venda")