import sqlite3
from collections import Counter
import string
import pandas as pd
import streamlit as st
import nltk

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO E CARREGAMENTO DE RECURSOS DO NLTK
# -----------------------------------------------------------------------------
@st.cache_resource
def carregar_recursos_nltk():
    recursos = ['punkt', 'punkt_tab', 'stopwords', 'vader_lexicon', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng']
    for recurso in recursos:
        try:
            nltk.download(recurso, quiet=True)
        except Exception:
            pass

carregar_recursos_nltk()

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tag import pos_tag

# -----------------------------------------------------------------------------
# BANCO DE DADOS LOCAL (SQLite)
# -----------------------------------------------------------------------------
DB_NAME = "laboratorio_pln.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            atividade TEXT,
            entrada TEXT,
            resultado TEXT,
            data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def salvar_historico(atividade, entrada, resultado):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historico_atividades (atividade, entrada, resultado)
        VALUES (?, ?, ?)
    """, (atividade, str(entrada), str(resultado)))
    conn.commit()
    conn.close()

def carregar_historico():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM historico_atividades ORDER BY id DESC", conn)
    conn.close()
    return df

init_db()

# -----------------------------------------------------------------------------
# INTERFACE STREAMLIT
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Laboratório Avançado de PLN", layout="wide")

st.title("⚡ Central de Soluções em Processamento de Linguagem Natural")
st.markdown("""
Plataforma educativa moderna para execução de rotinas analíticas em larga escala. 
Cada módulo abaixo resolve uma problemática corporativa específica utilizando **Streamlit**, **NLTK**, **POS Tagging**, **Polaridade** e persistência em **banco de dados SQLite local**.
""")

st.divider()

abas = st.tabs([f"Ativ {i}" for i in range(1, 11)] + ["🗄️ Histórico Geral"])

# -----------------------------------------------------------------------------
# ATIVIDADE 1: Tokenização Simples
# -----------------------------------------------------------------------------
with abas[0]:
    st.subheader("Atividade 1: Tokenização Básica")
    st.markdown("**Problemática:** Transformar textos brutos em unidades individuais (tokens).")
    
    t1 = st.text_input("Digite o texto:", "O atendimento do suporte foi rápido e muito eficiente.", key="i1")
    if st.button("Executar Tokenização", key="b1"):
        tokens = word_tokenize(t1, language='portuguese')
        tags = pos_tag(tokens)
        st.write("**Tokens Gerados:**", tokens)
        st.write("**POS Tags (Classes Gramaticais):**", tags)
        salvar_historico("Atividade 1", t1, f"Tokens: {len(tokens)}")
        st.success("Processado e salvo no banco SQLite!")

# -----------------------------------------------------------------------------
# ATIVIDADE 2: Frequência de Palavras
# -----------------------------------------------------------------------------
with abas[1]:
    st.subheader("Atividade 2: Frequência de Palavras")
    st.markdown("**Problemática:** Identificar quais palavras aparecem com mais frequência em avaliações.")
    
    t2 = st.text_area("Texto de Avaliações:", "o produto é bom o produto é rápido o produto chegou no prazo", key="i2")
    if st.button("Contar Frequência", key="b2"):
        tokens = [p.lower() for p in word_tokenize(t2, language='portuguese') if p.isalnum()]
        freq = Counter(tokens)
        df = pd.DataFrame(freq.items(), columns=["Palavra", "Frequência"]).sort_values(by="Frequência", ascending=False)
        st.dataframe(df, use_container_width=True)
        salvar_historico("Atividade 2", t2, f"Total termos: {len(tokens)}")
        st.success("Processado e salvo no banco SQLite!")

# -----------------------------------------------------------------------------
# ATIVIDADE 3: Detecção de Palavras Negativas e Palavrões (CORRIGIDO)
# -----------------------------------------------------------------------------
with abas[2]:
    st.subheader("Atividade 3: Alerta de Palavras Negativas e Palavrões")
    st.markdown("**Problemática:** Detectar termos de insatisfação, negações e profanidades para priorizar o suporte.")
    
    t3 = st.text_area("Mensagem:", "Olá não gostei do atendimento porra", key="i3")
    if st.button("Analisar Alerta", key="b3"):
        texto_lower = t3.lower()
        
        # Dicionário expandido de palavras críticas, palavrões e negações
        palavrões_e_profanidades = [
            "porra", "caralho", "merda", "puta", "bosta", "cacete", "pQP", "inferno", "lixo"
        ]
        
        termo_insatisfacao = [
            "ruim", "péssimo", "pessimo", "erro", "defeito", "horrivel", "horrível", 
            "odiei", "demorado", "incompetente", "maldito", "pessima", "péssima"
        ]
        
        expressoes_negativas = [
            "não gostei", "nao gostei", "não funciona", "nao funciona", 
            "não recomendo", "nao recomendo", "sem condições", "nao recebi", "não recebi"
        ]
        
        # Verificações
        palavroes_encontrados = [p for p in palavrões_e_profanidades if p in texto_lower]
        insatisfacoes_encontradas = [p for p in termo_insatisfacao if p in texto_lower]
        expressoes_encontradas = [e for e in expressoes_negativas if e in texto_lower]
        
        alertas = palavroes_encontrados + insatisfacoes_encontradas + expressoes_encontradas
        
        sia = SentimentIntensityAnalyzer()
        score = sia.polarity_scores(t3)['compound']
        
        if alertas:
            st.error(f"🚨 **PRIORIDADE MÁXIMA / ALERTA CRÍTICO**")
            if palavroes_encontrados:
                st.write(f"🤬 **Linguagem Inapropriada/Palavrões:** {palavroes_encontrados}")
            if expressoes_encontradas or insatisfacoes_encontradas:
                st.write(f"⚠️ **Termos de Insatisfação:** {expressoes_encontradas + insatisfacoes_encontradas}")
            st.write(f"📊 **Score de Polaridade VADER:** `{score}`")
        else:
            st.success("✅ Sem termos críticos de alerta.")
            
        salvar_historico("Atividade 3", t3, f"Alertas: {alertas}")

# -----------------------------------------------------------------------------
# ATIVIDADE 4: Remoção de Stopwords
# -----------------------------------------------------------------------------
with abas[3]:
    st.subheader("Atividade 4: Remoção de Stopwords")
    st.markdown("**Problemática:** Eliminar palavras irrelevantes para melhorar a interpretação.")
    
    t4 = st.text_input("Texto:", "A entrega do produto foi feita para o cliente de forma rápida.", key="i4")
    if st.button("Remover Stopwords", key="b4"):
        tokens = word_tokenize(t4, language='portuguese')
        stop_words = set(stopwords.words('portuguese'))
        tokens_limpos = [p for p in tokens if p.lower() not in stop_words and p.isalnum()]
        
        st.write("**Resultado:**", tokens_limpos)
        salvar_historico("Atividade 4", t4, f"Tokens filtrados: {len(tokens_limpos)}")
        st.success("Processado e salvo no banco SQLite!")

# -----------------------------------------------------------------------------
# ATIVIDADE 5: Classificação de Sentimento Simples
# -----------------------------------------------------------------------------
with abas[4]:
    st.subheader("Atividade 5: Classificação de Sentimento por Condicionais")
    st.markdown("**Problemática:** Entender rapidamente o sentimento de comentários com base em palavras-chave.")
    
    t5 = st.text_input("Comentário:", "O produto é excelente, muito bom e fácil de usar!", key="i5")
    if st.button("Classificar Sentimento", key="b5"):
        positivas = ["bom", "excelente", "ótimo", "fácil", "adoramos"]
        negativas = ["ruim", "péssimo", "horrível", "difícil", "quebrado", "porra", "lixo"]
        
        tokens = t5.lower().split()
        p_count = sum(1 for p in tokens if p in positivas)
        n_count = sum(1 for p in tokens if p in negativas)
        
        res = "Positivo" if p_count > n_count else ("Negativo" if n_count > p_count else "Neutro")
        st.metric("Sentimento Identificado", res)
        salvar_historico("Atividade 5", t5, res)

# -----------------------------------------------------------------------------
# ATIVIDADE 6: Roteamento de Chatbot
# -----------------------------------------------------------------------------
with abas[5]:
    st.subheader("Atividade 6: Roteamento Inteligente")
    st.markdown("**Problemática:** Identificar palavras-chave para direcionar o cliente ao setor correto.")
    
    t6 = st.text_input("Mensagem:", "Estou com um erro ao tentar efetuar o pagamento da fatura.", key="i6")
    if st.button("Rotear Mensagem", key="b6"):
        txt = t6.lower()
        if "cancelar" in txt:
            setor = "Retenção e Cancelamentos"
        elif "pagamento" in txt or "fatura" in txt:
            setor = "Financeiro"
        elif "erro" in txt or "problema" in txt:
            setor = "Suporte Técnico"
        else:
            setor = "Atendimento Geral"
            
        st.info(f"➡️ Direcionado para: **{setor}**")
        salvar_historico("Atividade 6", t6, setor)

# -----------------------------------------------------------------------------
# ATIVIDADE 7: Frequência em Reclamações
# -----------------------------------------------------------------------------
with abas[6]:
    st.subheader("Atividade 7: Palavras Frequentes em Reclamações")
    st.markdown("**Problemática:** Identificar termos recorrentes em reclamações para melhoria do produto.")
    
    t7 = st.text_area("Reclamação:", "O aplicativo apresenta erro ao logar. O aplicativo fecha sozinho e o erro persists.", key="i7")
    if st.button("Analisar Reclamação", key="b7"):
        tokens = word_tokenize(t7.lower(), language='portuguese')
        stop_words = set(stopwords.words('portuguese'))
        uteis = [p for p in tokens if p not in stop_words and p.isalnum()]
        comuns = Counter(uteis).most_common(3)
        
        st.write("**Top Termos:**", comuns)
        salvar_historico("Atividade 7", t7, str(comuns))

# -----------------------------------------------------------------------------
# ATIVIDADE 8: Classificação em Setores
# -----------------------------------------------------------------------------
with abas[7]:
    st.subheader("Atividade 8: Classificação Automática por Regras")
    st.markdown("**Problemática:** Classificar mensagens automaticamente em Suporte Técnico ou Financeiro.")
    
    t8 = st.text_input("Mensagem:", "Não consigo fazer o pagamento do meu plano.", key="i8")
    if st.button("Classificar", key="b8"):
        txt = t8.lower()
        tec = any(p in txt for p in ["erro", "bug", "lentidão", "login", "senha"])
        fin = any(p in txt for p in ["cobrança", "fatura", "cartão", "pagamento"])
        
        cat = "Suporte Técnico" if tec and not fin else ("Financeiro" if fin and not tec else "Triagem Geral")
        st.success(f"Categoria: **{cat}**")
        salvar_historico("Atividade 8", t8, cat)

# -----------------------------------------------------------------------------
# ATIVIDADE 9: Limpeza e Normalização
# -----------------------------------------------------------------------------
with abas[8]:
    st.subheader("Atividade 9: Limpeza e Normalização de Textos")
    st.markdown("**Problemática:** Remover pontuação e normalizar texto para IA.")
    
    t9 = st.text_input("Texto Bruto:", "Atenção: O pedido #12344 foi cancelado! Por favor, verifique...", key="i9")
    if st.button("Normalizar", key="b9"):
        tokens = word_tokenize(t9.lower(), language='portuguese')
        limpos = [p for p in tokens if p not in string.punctuation and p.isalnum()]
        resultado = " ".join(limpos)
        
        st.code(resultado)
        salvar_historico("Atividade 9", t9, resultado)

# -----------------------------------------------------------------------------
# ATIVIDADE 10: Tokenização + Sentimento
# -----------------------------------------------------------------------------
with abas[9]:
    st.subheader("Atividade 10: Tokenização + Sentimento Avançado")
    st.markdown("**Problemática:** Combinar tokenização, stopwords e análise de polaridade.")
    
    t10 = st.text_area("Avaliação:", "A entrega foi rápida, o produto veio muito bem embalado e funcionou perfeitamente!", key="i10")
    if st.button("Processar Análise Completa", key="b10"):
        tokens = word_tokenize(t10.lower(), language='portuguese')
        stop_words = set(stopwords.words('portuguese'))
        tokens_uteis = [p for p in tokens if p not in stop_words and p.isalnum()]
        
        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(t10)
        
        st.write("**Tokens Úteis:**", tokens_uteis)
        st.json(scores)
        salvar_historico("Atividade 10", t10, f"Compound: {scores['compound']}")
        st.success("Processado com sucesso!")

# -----------------------------------------------------------------------------
# HISTÓRICO GERAL
# -----------------------------------------------------------------------------
with abas[10]:
    st.subheader("🗄️ Histórico de Execuções (Banco SQLite Local)")
    df_hist = carregar_historico()
    if not df_hist.empty:
        st.dataframe(df_hist, use_container_width=True)
    else:
        st.info("Nenhuma execução registrada até o momento.")