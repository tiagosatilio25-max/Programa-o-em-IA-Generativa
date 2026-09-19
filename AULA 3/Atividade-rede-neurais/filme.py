import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input

# 1. Preparação dos Dados
filmes = pd.DataFrame({
    'duracao': [80, 90, 100, 110, 120],
    'nota': [4, 5, 7, 8, 9]
})

X = np.array(filmes['duracao'], dtype=np.float32).reshape(-1, 1)
y = np.array(filmes['nota'], dtype=np.float32)

# 2. Definição do Modelo
modelo = Sequential([
    Input(shape=(1,)),
    Dense(units=1)
])

# 3. Compilação
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
    loss='mean_squared_error'
)

# 4. Treinamento
modelo.fit(X, y, epochs=800, verbose=0)

# 5. Predição
duracao_teste = np.array([[105.0]], dtype=np.float32)
previsao = modelo.predict(duracao_teste)

print(f"Duração: {duracao_teste[0][0]} min -> Nota prevista: {previsao[0][0]:.2f}")