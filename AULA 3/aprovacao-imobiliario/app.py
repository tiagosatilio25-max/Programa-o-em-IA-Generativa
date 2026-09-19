# app_streamlit.py

import streamlit as st

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulador de Crédito Imobiliário",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# CABEÇALHO DA APLICAÇÃO
# -----------------------------------------------------------------------------
st.title("🏠 Simulador de Aprovação de Crédito Imobiliário")
st.caption(
    "🔑 Módulo 5 — Simule em tempo real a viabilidade do seu financiamento imobiliário!"
)
st.markdown("---")

# -----------------------------------------------------------------------------
# FORMULÁRIO DE ENTRADA DE DADOS
# -----------------------------------------------------------------------------
with st.form("form_simulacao"):
    st.subheader("📋 Dados do Proponente e do Imóvel")

    col1, col2 = st.columns(2)

    with col1:
        idade = st.number_input(
            "🎂 Idade do comprador (anos)",
            min_value=14,
            max_value=100,
            value=28,
            step=1,
            help="Idade mínima permitida: 18 anos.",
        )

        renda_mensal = st.number_input(
            "💰 Renda Mensal Familiar Bruta (R$)",
            min_value=0.0,
            value=8000.0,
            step=500.0,
            format="%.2f",
            help="Soma das rendas brutas de todos os compradores envolvidos.",
        )

        prazo_anos = st.number_input(
            "📅 Prazo Desejado (Anos)",
            min_value=1,
            max_value=35,
            value=30,
            step=1,
            help="O prazo máximo padrão de financiamento imobiliário é de 35 anos.",
        )

    with col2:
        valor_imovel = st.number_input(
            "🏢 Valor do Apartamento (R$)",
            min_value=0.0,
            value=300000.0,
            step=10000.0,
            format="%.2f",
        )

        valor_entrada = st.number_input(
            "💵 Valor da Entrada (R$)",
            min_value=0.0,
            value=60000.0,
            step=5000.0,
            format="%.2f",
            help="Entrada mínima exigida pelos bancos: 20% do valor do imóvel.",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    btn_simular = st.form_submit_button(
        "⚡ Analisar Crédito Imobiliário", use_container_width=True
    )

# -----------------------------------------------------------------------------
# LÓGICA DE PROCESSAMENTO E RESULTADOS
# -----------------------------------------------------------------------------
if btn_simular:
    # 1. Cálculos Financeiros Básicos
    entrada_minima_requerida = valor_imovel * 0.20
    valor_financiado = valor_imovel - valor_entrada
    total_meses = prazo_anos * 12

    # Taxa de juros anual simulada (10% a.a.) -> Conversão para taxa mensal proporcional
    taxa_anual = 0.10
    taxa_mensal = ((1 + taxa_anual) ** (1 / 12)) - 1

    # Cálculo da Parcela Estimada (Fórmula da Tabela Price)
    if valor_financiado > 0 and total_meses > 0:
        parcela_estimada = (
            valor_financiado
            * (taxa_mensal * (1 + taxa_mensal) ** total_meses)
            / (((1 + taxa_mensal) ** total_meses) - 1)
        )
    else:
        parcela_estimada = 0.0

    percentual_comprometimento = (
        (parcela_estimada / renda_mensal) * 100 if renda_mensal > 0 else 0
    )
    percentual_entrada = (
        (valor_entrada / valor_imovel) * 100 if valor_imovel > 0 else 0
    )

    # 2. Validação das Regras de Negócio e Risco Financeiro
    erros = []

    if idade < 18:
        erros.append(
            "❌ **Maioridade Legal:** O comprador deve ter pelo menos 18 anos completos (Incapacidade civil)."
        )

    if (idade + prazo_anos) > 80:
        erros.append(
            f"❌ **Limite Idade + Prazo:** A soma da sua idade ({idade}) com o prazo ({prazo_anos} anos) é **{idade + prazo_anos} anos**. O limite máximo permitido pelas seguradoras bancárias é de **80 anos**."
        )

    if valor_entrada < entrada_minima_requerida:
        erros.append(
            f"❌ **Entrada Insuficiente:** A entrada informada de R$ {valor_entrada:,.2f} ({percentual_entrada:.1f}%) é inferior aos **20% mínimos exigidos** (R$ {entrada_minima_requerida:,.2f})."
        )

    if percentual_comprometimento > 30.0:
        erros.append(
            f"❌ **Comprometimento de Renda Excedido:** A parcela estimada de R$ {parcela_estimada:,.2f} compromete **{percentual_comprometimento:.1f}%** da sua renda. O limite máximo permitido é **30.0%** (R$ {renda_mensal * 0.30:,.2f})."
        )

    st.markdown("### 📊 Resultado da Simulação")

    # Exibição dos KPIs / Cartões de Métricas
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

    col_kpi1.metric(
        label="🏢 Valor Financiado", value=f"R$ {valor_financiado:,.2f}"
    )

    col_kpi2.metric(
        label="📝 Parcela Estimada", value=f"R$ {parcela_estimada:,.2f}"
    )

    col_kpi3.metric(
        label="📈 Comprometimento de Renda",
        value=f"{percentual_comprometimento:.1f}%",
        delta=f"{30.0 - percentual_comprometimento:.1f}% de folga",
        delta_color="normal"
        if percentual_comprometimento <= 30
        else "inverse",
    )

    col_kpi4.metric(
        label="💵 Entrada Realizada",
        value=f"{percentual_entrada:.1f}%",
        delta=f"{percentual_entrada - 20.0:.1f}% da mínima",
        delta_color="normal" if percentual_entrada >= 20 else "inverse",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Parecer Final e Recomendações de Adequação
    if not erros:
        st.success("🎉 **CRÉDITO PRÉ-APROVADO COM SUCESSO!**")
        st.write(
            f"Parabéns! Seu perfil financeiro atende a todos os critérios do banco. A parcela estimada de **R$ {parcela_estimada:,.2f}** é compatível com a sua renda mensal."
        )
        st.balloons()
    else:
        st.error("⚠️ **CRÉDITO NEGADO / NECESSITA DE AJUSTES**")
        st.write(
            "Foram identificados os seguintes impedimentos no seu pedido:"
        )

        for erro in erros:
            st.write(erro)

        # Sugestões do Banco
        st.markdown("---")
        st.warning("💡 **SUGESTÕES DO BANCO PARA APROVAÇÃO DO CRÉDITO:**")

        if (idade + prazo_anos) > 80:
            prazo_maximo_permitido = 80 - idade
            st.write(
                f"• **Ajuste o prazo:** Para a sua idade ({idade} anos), o prazo máximo permitido é de **{prazo_maximo_permitido} anos**."
            )

        if valor_entrada < entrada_minima_requerida:
            diferenca_entrada = entrada_minima_requerida - valor_entrada
            st.write(
                f"• **Complete a entrada:** É necessário acrescentar pelo menos **R$ {diferenca_entrada:,.2f}** ao valor da entrada (você pode utilizar o saldo do seu FGTS)."
            )

        if percentual_comprometimento > 30.0:
            parcela_maxima_permitida = renda_mensal * 0.30
            st.write(
                f"• **Adeqúe a parcela:** Para a renda informada de R$ {renda_mensal:,.2f}, a parcela aceita é de no máximo **R$ {parcela_maxima_permitida:,.2f}**."
            )
            st.write(
                "• **Dica:** Tente aumentar a entrada ou buscar um imóvel de menor valor para reduzir o valor da prestação mensal."
            )

    # -------------------------------------------------------------------------
    # MEMÓRIA DE CÁLCULO
    # -------------------------------------------------------------------------
    with st.expander("🔍 Ver Memória de Cálculo e Detalhes Técnicos"):
        st.markdown(
            f"""
        **Resumo dos Parâmetros Utilizados:**
        - **Valor do Imóvel:** R$ {valor_imovel:,.2f}
        - **Valor a Financiar:** R$ {valor_financiado:,.2f}
        - **Prazo Escolhido:** {prazo_anos} anos ({total_meses} meses)
        - **Soma (Idade + Prazo):** {idade + prazo_anos} anos *(Limite máximo: 80 anos)*
        - **Taxa de Juros Aplicada:** 10,0% ao ano *(Aprox. {taxa_mensal * 100:.2f}% ao mês)*
        - **Sistema de Amortização:** Tabela Price (Parcelas Fixas)
        - **Margem de Renda Consignável (30%):** R$ {renda_mensal * 0.30:,.2f}
        """
        )