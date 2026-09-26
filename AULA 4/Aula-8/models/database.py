import sqlite3
import pandas as pd

DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            lemmas TEXT NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def salvar_solicitacao(texto, categoria, lemmas):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO solicitacoes (texto, categoria, lemmas) VALUES (?, ?, ?)",
        (texto, categoria, ",".join(lemmas))
    )
    conn.commit()
    conn.close()

def obter_historico_df():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT id, texto, categoria, lemmas, data_criacao FROM solicitacoes ORDER BY id DESC", conn)
    conn.close()
    return df