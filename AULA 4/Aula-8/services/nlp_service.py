import spacy

nlp = spacy.load("pt_core_news_sm")

INTENCOES = {
    "Bloqueio de Cartão": {"bloquear", "cartao", "perda", "roubo", "furtado", "cancelar"},
    "Segunda Via de Boleto": {"boleto", "segunda", "via", "fatura", "codigo", "barras", "vencimento"},
    "Consulta de Saldo/Extrato": {"saldo", "extrato", "conta", "dinheiro", "sobra"},
    "Suporte Geral": {"atendimento", "falar", "humano", "ajuda", "suporte"}
}

def classificar_texto(texto):
    doc = nlp(texto.lower())
    
    # Extrai lemas removendo pontuações e stop words
    lemmas = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
    set_lemmas = set(lemmas)
    
    pontuacoes = {}
    for intencao, palavras_chave in INTENCOES.items():
        intersecao = set_lemmas.intersection(palavras_chave)
        pontuacoes[intencao] = len(intersecao)
    
    # Retorna a intenção com maior contagem de coincidências
    categoria = max(pontuacoes, key=pontuacoes.get)
    if pontuacoes[categoria] == 0:
        categoria = "Não Identificado"
        
    return categoria, lemmas