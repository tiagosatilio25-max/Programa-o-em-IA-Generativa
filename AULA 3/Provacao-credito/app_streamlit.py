"""Interface web interativa do simulador de crédito, usando Streamlit.

Assim como o `cli.py`, este módulo só cuida de coleta e apresentação —
a decisão de crédito é sempre delegada ao `credito.service`, mantendo a
mesma lógica de negócio consistente entre as duas interfaces.

Executar com: streamlit run app_streamlit.py
"""

import streamlit as st

from credito.service import DadosInvalidosError, analisar_credito

st.set_page_config(page_title="Simulador de Crédito Bancário", page_icon="🏦")

st.title("🏦 Simulador de Aprovação de Crédito Bancário")
st.caption("Módulo 5 — simule em tempo real a aprovação do financiamento da sua moto.")

with st.form("form_simulacao"):
    idade = st.number_input("Idade (anos)", min_value=0, max_value=120, step=1)
    renda = st.number_input("Renda Mensal (R$)", min_value=0.0, step=100.0, format="%.2f")
    parcela = st.number_input(
        "Valor da Parcela Desejada (R$)", min_value=0.0, step=50.0, format="%.2f"
    )
    enviado = st.form_submit_button("Simular Crédito")

if enviado:
    try:
        resultado = analisar_credito(idade=int(idade), renda=float(renda), parcela=float(parcela))
    except DadosInvalidosError as erro:
        # Erro de negócio conhecido: mensagem amigável, sem stack trace.
        st.error(f"Não foi possível simular: {erro}")
    except Exception:
        # Erro não previsto: mensagem genérica ao usuário final.
        st.error("Ocorreu um erro inesperado. Tente novamente.")
    else:
        if resultado.aprovado:
            st.success(f"🎉 {resultado.motivo}")
        else:
            st.error(f"🚫 {resultado.motivo}")
            if resultado.parcela_sugerida is not None:
                st.info(
                    f"💡 Sugerimos uma parcela de até "
                    f"R$ {resultado.parcela_sugerida:.2f}."
                )
