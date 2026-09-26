import streamlit as st
import spacy
from collections import Counter

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="Plataforma Integrada de PLN com spaCy",
    page_icon="⚡",
    layout="wide"
)

# 2. Carregamento do Modelo spaCy
@st.cache_resource
def carregar_spacy():
    try:
        return spacy.load("pt_core_news_sm")
    except OSError:
        from spacy.cli import download
        download("pt_core_news_sm")
        return spacy.load("pt_core_news_sm")

nlp = carregar_spacy()

# 3. CSS Personalizado (Estilo Moderno & Alto Contraste para Leitura)
st.markdown("""
<style>
    /* Fundo da Aplicação */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #090d16 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Card de Conteúdo Principal */
    .main-card {
        background: rgba(30, 41, 59, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }

    /* CORREÇÃO VISUAL: Garantir leitura clara do texto digitado */
    .stTextInput input, .stTextArea textarea {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 10px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
    }
    
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }

    /* Botões com Gradiente */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        box-shadow: 0 4px 14px rgba(168, 85, 247, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6) !important;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. Navegação do Menu Lateral
st.sidebar.markdown("## ⚡ **Menu de Atividades**")
atividade = st.sidebar.selectbox(
    "Selecione a Atividade:",
    [
        "Atividade 1: Sentimentos por Palavras-Chave",
        "Atividade 2: Tokenização de Avaliações",
        "Atividade 3: Classificador Bancário",
        "Atividade 4: Remoção de Stopwords",
        "Atividade 5: Deteção de Reclamações",
        "Atividade 6: Extração de Entidades (NER)",
        "Atividade 7: Frequência de Palavras",
        "Atividade 8: Deteção de Intenções (Chatbot)",
        "Atividade 9: Normalização de Texto",
        "Atividade 10: Classificação Tripla em Pipeline"
    ]
)

# -------------------------------------------------------------------
# ATIVIDADE 1
# -------------------------------------------------------------------
if atividade == "Atividade 1: Sentimentos por Palavras-Chave":
    st.markdown("""
    <div class="main-card">
        <h1>📣 Atividade 1: Análise de Sentimentos Simples</h1>
        <p style="color: #cbd5e1;">Identifique rapidamente se os comentários dos clientes são positivos ou negativos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    texto = st.text_area("Comentário do Cliente:", "O produto é muito bom e o atendimento foi excelente!")
    
    if st.button("Analisar Sentimento", use_container_width=True):
        doc = nlp(texto.lower())
        lemmas = [token.lemma_ for token in doc]
        
        pos = {"bom", "excelente", "ótimo", "maravilhoso", "gostar", "adorar"}
        neg = {"ruim", "péssimo", "horrível", "atrasado", "defeito"}
        
        s_pos = sum(1 for l in lemmas if l in pos)
        s_neg = sum(1 for l in lemmas if l in neg)
        
        if s_pos > s_neg:
            st.success("🟢 **Sentimento Detectado: POSITIVO**")
        elif s_neg > s_pos:
            st.error("🔴 **Sentimento Detectado: NEGATIVO**")
        else:
            st.info("⚪ **Sentimento Detectado: NEUTRO**")

# -------------------------------------------------------------------
# ATIVIDADE 2
# -------------------------------------------------------------------
elif atividade == "Atividade 2: Tokenização de Avaliações":
    st.markdown("""
    <div class="main-card">
        <h1>🛒 Atividade 2: Tokenização com spaCy</h1>
        <p style="color: #cbd5e1;">Separe as palavras das avaliações do e-commerce para análise.</p>
    </div>
    """, unsafe_allow_html=True)
    
    texto = st.text_area("Avaliação do Produto:", "A entrega foi rápida e o produto chegou em perfeitas condições.")
    
    if st.button("Executar Tokenização", use_container_width=True):
        doc = nlp(texto)
        tokens = [token.text for token in doc if not token.is_space]
        
        st.write("### Lista de Tokens Extratados")
        st.write(tokens)

# -------------------------------------------------------------------
# ATIVIDADE 3
# -------------------------------------------------------------------
elif atividade == "Atividade 3: Classificador Bancário":
    st.markdown("""
    <div class="main-card">
        <h1>🏦 Atividade 3: Classificador para Banco Digital</h1>
        <p style="color: #cbd5e1;">Identificação automática de solicitações de serviços bancários.</p>
    </div>
    """, unsafe_allow_html=True)
    
    texto = st.text_input("Solicitação do Cliente:", "Preciso urgente bloquear o meu cartão.")
    
    if st.button("Classificar Solicitação", use_container_width=True):
        doc = nlp(texto.lower())
        lemmas = {token.lemma_ for token in doc}
        
        if {"bloquear", "cartão", "bloqueio"}.intersection(lemmas):
            st.warning("💳 **Categoria:** Cartões - Bloqueio de Cartão")
        elif {"boleto", "segunda", "via", "fatura"}.intersection(lemmas):
            st.info("📄 **Categoria:** Financeiro - Segundas Vias")
        else:
            st.write("❓ **Categoria:** Outros Atendimentos")

# -------------------------------------------------------------------
# ATIVIDADE 4
# -------------------------------------------------------------------
elif atividade == "Atividade 4: Remoção de Stopwords":
    st.markdown("""
    <div class="main-card">
        <h1>🧹 Atividade 4: Remoção de Stopwords</h1>
        <p style="color: #cbd5e1;">Remova palavras gramaticais irrelevantes para otimizar o processamento.</p>
    </div>
    """, unsafe_allow_html=True)
    
    texto = st.text_area("Texto de Entrada:", "Esta é uma demonstração de remoção das palavras irrelevantes.")
    
    if st.button("Filtrar Texto", use_container_width=True):
        doc = nlp(texto)
        sem_stopwords = [token.text for token in doc if not token.is_stop and not token.is_punct]
        
        st.write("**Texto sem Stopwords:**")
        st.info(" ".join(sem_stopwords))

# -------------------------------------------------------------------
# ATIVIDADE 5
# -------------------------------------------------------------------
elif atividade == "Atividade 5: Deteção de Reclamações":
    st.markdown("""
    <div class="main-card">
        <h1>🚨 Atividade 5: Deteção Automática de Reclamações</h1>
        <p style="color: #cbd5e1;">Identifique termos de forte insatisfação nas mensagens de suporte.</p>
    </div>
    """, unsafe_allow_html=True)
    
    texto = st.text_area("Mensagem de Suporte:", "O sistema apresentou um erro e o serviço está péssimo.")
    
    if st.button("Detetar Alerta", use_container_width=True):
        doc = nlp(texto.lower())
        palavras_negativas = {"ruim", "erro", "péssimo", "horrível", "falha"}
        encontradas = [t.text for t in doc if t.lemma_ in palavras_negativas or t.text in palavras_negativas]
        
        if encontradas:
            st.error(f"🚨 **Alerta de Reclamação:** Foram encontradas as palavras críticas: {', '.join(set(encontradas))}")
        else:
            st.success("✅ **Nenhuma palavra de reclamação crítica foi detetada.**")

# -------------------------------------------------------------------
# ATIVIDADE 6
# -------------------------------------------------------------------
elif atividade == "Atividade 6: Extração de Entidades (NER)":
    st.markdown("""
    <div class="main-card">
        <h1>🏢 Atividade 6: Reconhecimento de Entidades (NER)</h1>
        <p style="color: #cbd5e1;">Identificação de nomes de pessoas, empresas e localidades.</p>
    </div>
    """, unsafe_allow_html=True)
    
    texto = st.text_area("Documento:", "O diretor Carlos esteve na sede da Petrobras em São Paulo.")
    
    if st.button("Extrair Entidades", use_container_width=True):
        doc = nlp(texto)
        if doc.ents:
            for ent in doc.ents:
                st.write(f"🔹 **{ent.text}** — Categoria: `{ent.label_}`")
        else:
            st.warning("Nenhuma entidade identificada no texto.")

# -------------------------------------------------------------------
# ATIVIDADE 7
# -------------------------------------------------------------------
elif atividade == "Atividade 7: Frequência de Palavras":
    st.markdown("""
    <div class="main-card">
        <h1>📊 Atividade 7: Frequência de Palavras em Redes Sociais</h1>
        <p style="color: #cbd5e1;">Contagem dos termos mais frequentes nos comentários.</p>
    </div>
    """, unsafe_allow_html=True)
    
    texto = st.text_area("Comentários da Postagem:", "produto bom produto excelente bom atendimento produto")
    
    if st.button("Calcular Frequência", use_container_width=True):
        doc = nlp(texto.lower())
        palavras = [t.lemma_ for t in doc if not t.is_stop and not t.is_punct and t.is_alpha]
        contagem = Counter(palavras)
        
        st.bar_chart(dict(contagem))

# -------------------------------------------------------------------
# ATIVIDADE 8
# -------------------------------------------------------------------
elif atividade == "Atividade 8: Deteção de Intenções (Chatbot)":
    st.markdown("""
    <div class="main-card">
        <h1>🤖 Atividade 8: Intenções para Chatbot</h1>
        <p style="color: #cbd5e1;">Identificação de intenções do utilizador por regras de PLN.</p>
    </div>
    """, unsafe_allow_html=True)
    
    texto = st.text_input("Mensagem para o Chatbot:", "Quero comprar um novo produto.")
    
    if st.button("Identificar Intenção", use_container_width=True):
        doc = nlp(texto.lower())
        lemmas = {t.lemma_ for t in doc}
        
        if {"comprar", "adquirir"}.intersection(lemmas):
            st.success("🎯 **Intenção:** Comprar")
        elif {"cancelar", "encerrar"}.intersection(lemmas):
            st.error("🎯 **Intenção:** Cancelar")
        elif {"suporte", "ajuda", "técnico"}.intersection(lemmas):
            st.warning("🎯 **Intenção:** Suporte")
        else:
            st.info("🎯 **Intenção:** Outra / Indefinida")

# -------------------------------------------------------------------
# ATIVIDADE 9
# -------------------------------------------------------------------
elif atividade == "Atividade 9: Normalização de Texto":
    st.markdown("""
    <div class="main-card">
        <h1>🧼 Atividade 9: Normalização e Limpeza de Texto</h1>
        <p style="color: #cbd5e1;">Padronização para minúsculas e remoção de pontuações.</p>
    </div>
    """, unsafe_allow_html=True)
    
    texto = st.text_input("Texto Bruto:", "Olá!!! Este É Um Exemplo, Certo?")
    
    if st.button("Normalizar Texto", use_container_width=True):
        doc = nlp(texto)
        limpo = " ".join([t.text.lower() for t in doc if not t.is_punct])
        st.code(limpo, language="text")

# -------------------------------------------------------------------
# ATIVIDADE 10
# -------------------------------------------------------------------
elif atividade == "Atividade 10: Classificação Tripla em Pipeline":
    st.markdown("""
    <div class="main-card">
        <h1>⚡ Atividade 10: Classificação Tripla em Pipeline</h1>
        <p style="color: #cbd5e1;">Processamento completo com tokenização e classificação em 3 categorias.</p>
    </div>
    """, unsafe_allow_html=True)
    
    texto = st.text_area("Feedback do Cliente:", "O produto chegou no prazo certo, mas a qualidade é ruim.")
    
    if st.button("Executar Pipeline Completo", use_container_width=True):
        doc = nlp(texto.lower())
        lemmas = [t.lemma_ for t in doc if not t.is_stop and not t.is_punct]
        
        pos = {"bom", "ótimo", "excelente", "rápido", "prazo"}
        neg = {"ruim", "péssimo", "lento", "defeito"}
        
        p_count = sum(1 for l in lemmas if l in pos)
        n_count = sum(1 for l in lemmas if l in neg)
        
        st.write("**Tokens Relevantes:**", lemmas)
        
        if p_count > n_count:
            st.success("🟢 **Classificação Final: POSITIVO**")
        elif n_count > p_count:
            st.error("🔴 **Classificação Final: NEGATIVO**")
        else:
            st.info("⚪ **Classificação Final: NEUTRO**")