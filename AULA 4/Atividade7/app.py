import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import re
import string
import time

# 1. Configuração da página
st.set_page_config(
    page_title="Plataforma Integrada de PLN",
    page_icon="⚡",
    layout="wide"
)
# Injeção de CSS corrigida para contraste e legibilidade
st.markdown("""
<style>
    /* Fundo da aplicação */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    
    /* Estilização da barra lateral */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Cartão de destaque visual */
    .main-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    
    /* CORREÇÃO DO TEXTO NOS INPUTS E TEXTAREAS */
    .stTextInput input, .stTextArea textarea {
        color: #0f172a !important;
        background-color: #f1f5f9 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    
    /* Rótulos/Labels acima dos campos */
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    
    /* Botões personalizados com gradiente */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
    }

    /* Títulos destacados */
    h1, h2, h3 {
        color: #f1f5f9 !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Inicialização dos Recursos NLTK
@st.cache_resource
def carregar_nltk():
    recursos = ['punkt', 'punkt_tab', 'stopwords', 'vader_lexicon']
    for r in recursos:
        nltk.download(r, quiet=True)
    return SentimentIntensityAnalyzer()

vader = carregar_nltk()

# 4. Navegação Lateral
st.sidebar.markdown("# 📌 **Menu PLN**")
atividade = st.sidebar.selectbox(
    "Escolha o Módulo:",
    [
        "Template: VADER (Análise de Sentimentos)",
        "Atividade 1: Tokenização",
        "Atividade 2: Frequência de Palavras",
        "Atividade 3: Alerta de Palavras Negativas",
        "Atividade 4: Remoção de Stopwords",
        "Atividade 5: Sentimento por Regras",
        "Atividade 6: Chatbot & Direcionamento",
        "Atividade 7: Top Palavras em Reclamações",
        "Atividade 8: Classificador de Chamados",
        "Atividade 9: Limpeza e Normalização",
        "Atividade 10: Pipeline Completo"
    ]
)

# -------------------------------------------------------------------
# VADER TEMPLATE
# -------------------------------------------------------------------
if atividade == "Template: VADER (Análise de Sentimentos)":
    st.markdown("""
    <div class="main-card">
        <h1>🎭 Análise de Sentimento com VADER</h1>
        <p style="color: #94a3b8;">Insira uma frase em português para calcular a polaridade e pontuação compound.</p>
    </div>
    """, unsafe_allow_html=True)

    texto = st.text_area("Texto para Análise:", "O atendimento foi excelente e o produto chegou super rápido!")

    if st.button("🚀 Processar Sentimento", use_container_width=True):
        if texto.strip():
            scores = vader.polarity_scores(texto)
            compound = scores['compound']

            if compound >= 0.05:
                st.balloons()
                st.success(f"🟢 **Sentimento Positivo** (Compound: {compound:.4f})")
            elif compound <= -0.05:
                st.snow()
                st.error(f"🔴 **Sentimento Negativo** (Compound: {compound:.4f})")
            else:
                st.info(f"⚪ **Sentimento Neutro** (Compound: {compound:.4f})")
        else:
            st.warning("Insira um texto válido.")

# -------------------------------------------------------------------
# ATIVIDADE 2 (Frequência sem dependência do Plotly)
# -------------------------------------------------------------------
elif atividade == "Atividade 2: Frequência de Palavras":
    st.markdown("""
    <div class="main-card">
        <h1>📊 Atividade 2: Frequência de Palavras</h1>
        <p style="color: #94a3b8;">Contagem visual das palavras mais utilizadas no texto.</p>
    </div>
    """, unsafe_allow_html=True)

    texto = st.text_area("Texto de Avaliações:", "o produto é muito bom o atendimento também foi bom o produto surpreendeu")

    if st.button("📈 Gerar Gráfico de Frequência", use_container_width=True):
        palavras = texto.lower().split()
        contagem = Counter(palavras)
        
        # Gráfico nativo do Streamlit (não requer Plotly)
        st.bar_chart(dict(contagem))

# -------------------------------------------------------------------
# OUTRAS ATIVIDADES (Exemplo de estrutura padronizada)
# -------------------------------------------------------------------
elif atividade == "Atividade 1: Tokenização":
    st.markdown("<div class='main-card'><h1>🔤 Atividade 1: Tokenização</h1></div>", unsafe_allow_html=True)
    texto = st.text_area("Entrada:", "Olá, gostaria de saber o status do meu pedido.")
    if st.button("Processar", use_container_width=True):
        st.write("**Tokens:**", word_tokenize(texto))

elif atividade == "Atividade 3: Alerta de Palavras Negativas":
    st.markdown("<div class='main-card'><h1>🚨 Atividade 3: Alerta de Palavras Negativas</h1></div>", unsafe_allow_html=True)
    mensagem = st.text_input("Mensagem:", "Ocorreu um erro no sistema e o serviço está ruim.")
    if st.button("Verificar", use_container_width=True):
        alerta = any(p in mensagem.lower() for p in ["ruim", "péssimo", "erro", "falha"])
        if alerta:
            st.error("⚠️ **PRIORIDADE ALTA!** Palavra de alerta detetada.")
        else:
            st.success("✅ **STATUS NORMAL**")

elif atividade == "Atividade 4: Remoção de Stopwords":
    st.markdown("<div class='main-card'><h1>🧹 Atividade 4: Remoção de Stopwords</h1></div>", unsafe_allow_html=True)
    texto = st.text_area("Texto:", "O atendimento do suporte para o meu problema foi rápido.")
    if st.button("Limpar", use_container_width=True):
        st_pt = set(stopwords.words('portuguese'))
        tokens = [p for p in word_tokenize(texto.lower()) if p.isalnum() and p not in st_pt]
        st.info(" ".join(tokens))

elif atividade == "Atividade 5: Sentimento por Regras":
    st.markdown("<div class='main-card'><h1>🎭 Atividade 5: Classificação por Regras</h1></div>", unsafe_allow_html=True)
    comentario = st.text_input("Comentário:", "O produto é excelente e a entrega foi rápida.")
    if st.button("Classificar", use_container_width=True):
        pos = sum(1 for p in comentario.lower().split() if p in ["excelente", "bom", "ótimo", "rápida"])
        neg = sum(1 for p in comentario.lower().split() if p in ["ruim", "péssimo", "demorado"])
        if pos > neg:
            st.success("Sentimento: Positivo")
        elif neg > pos:
            st.error("Sentimento: Negativo")
        else:
            st.info("Sentimento: Neutro")

elif atividade == "Atividade 6: Chatbot & Direcionamento":
    st.markdown("<div class='main-card'><h1>🤖 Atividade 6: Chatbot & Direcionamento</h1></div>", unsafe_allow_html=True)
    mensagem = st.text_input("Solicitação:", "Quero realizar o pagamento da minha fatura.")
    if st.button("Encaminhar", use_container_width=True):
        msg = mensagem.lower()
        if "cancelar" in msg:
            st.subheader("Direcionado para: Setor de Cancelamentos")
        elif "erro" in msg:
            st.subheader("Direcionado para: Suporte Técnico")
        elif "pagamento" in msg:
            st.subheader("Direcionado para: Setor Financeiro")
        else:
            st.subheader("Direcionado para: Atendimento Geral")

elif atividade == "Atividade 7: Top Palavras em Reclamações":
    st.markdown("<div class='main-card'><h1>📋 Atividade 7: Palavras Mais Frequentes</h1></div>", unsafe_allow_html=True)
    reclamacao = st.text_area("Reclamação:", "O aplicativo fecha sozinho. O aplicativo está lento.")
    if st.button("Analisar", use_container_width=True):
        palavras = re.sub(r'[^\w\s]', '', reclamacao.lower()).split()
        st.write(Counter(palavras).most_common(3))

elif atividade == "Atividade 8: Classificador de Chamados":
    st.markdown("<div class='main-card'><h1>🏷️ Atividade 8: Classificador de Chamados</h1></div>", unsafe_allow_html=True)
    mensagem = st.text_input("Chamado:", "Minha tela travou e o sistema não abre.")
    if st.button("Classificar", use_container_width=True):
        msg = mensagem.lower()
        if any(p in msg for p in ["tela", "travou", "sistema", "erro"]):
            st.warning("Categoria: Suporte Técnico")
        elif any(p in msg for p in ["fatura", "boleto", "pagamento"]):
            st.info("Categoria: Financeiro")
        else:
            st.write("Categoria: Triagem Geral")

elif atividade == "Atividade 9: Limpeza e Normalização":
    st.markdown("<div class='main-card'><h1>🧼 Atividade 9: Limpeza de Texto</h1></div>", unsafe_allow_html=True)
    texto = st.text_input("Texto:", "Olá! O serviço é ótimo, porém o valor está alto...")
    if st.button("Normalizar", use_container_width=True):
        st.code(texto.lower().translate(str.maketrans('', '', string.punctuation)))

elif atividade == "Atividade 10: Pipeline Completo":
    st.markdown("<div class='main-card'><h1>⚡ Atividade 10: Pipeline Completo</h1></div>", unsafe_allow_html=True)
    avaliacao = st.text_area("Avaliação:", "O produto chegou rápido, porém a qualidade é ruim e fraca!")
    if st.button("Executar Pipeline", use_container_width=True):
        limpo = avaliacao.lower().translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(limpo)
        score = sum(1 if t in ["rápido", "bom", "ótimo"] else -1 if t in ["ruim", "fraca"] else 0 for t in tokens)
        st.write("**Tokens:**", tokens)
        st.metric("Score Final", score)