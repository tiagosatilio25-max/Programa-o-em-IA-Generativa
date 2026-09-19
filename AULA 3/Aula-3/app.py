import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input

# 1. Preparação dos Dados
estudos = pd.DataFrame({
    'notas': [1, 2, 4, 6, 8, 10],
    'horas': [2, 4, 5, 7, 9, 10]
})

X = np.array(estudos['horas'], dtype=np.float32).reshape(-1, 1)
y = np.array(estudos['notas'], dtype=np.float32)

# 2. Definição da Arquitetura
modelo = Sequential([
    Input(shape=(1,)),
    Dense(units=1)
])

# 3. Compilação (Adam costuma convergir melhor sem escala nos dados)
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
    loss='mean_squared_error'
)

# 4. Treinamento
modelo.fit(X, y, epochs=500, verbose=0)

# 5. Predição
horas_teste = np.array([[6.0]], dtype=np.float32)
previsao = modelo.predict(horas_teste)

print(f"Nota prevista para {horas_teste[0][0]} horas de estudo: {previsao[0][0]:.2f}")