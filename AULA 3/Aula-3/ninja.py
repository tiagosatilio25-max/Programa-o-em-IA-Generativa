import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input

# 1. Preparação dos Dados
alunos = pd.DataFrame({
    'faltas': [0, 1, 2, 5, 7, 10],
    'resultado': [1, 1, 1, 0, 0, 0]
})

X = np.array(alunos['faltas'], dtype=np.float32).reshape(-1, 1)
y = np.array(alunos['resultado'], dtype=np.float32)

# 2. Definição do Modelo
modelo = Sequential([
    Input(shape=(1,)),
    Dense(units=1, activation='sigmoid')
])

# 3. Compilação
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# 4. Treinamento
modelo.fit(X, y, epochs=600, verbose=0)

# 5. Predição
faltas_teste = np.array([[3.0]], dtype=np.float32)
probabilidade = modelo.predict(faltas_teste)[0][0]
status = "Aprovado" if probabilidade >= 0.5 else "Reprovado"

print(f"Faltas: {faltas_teste[0][0]} -> Probabilidade de Aprovação: {probabilidade:.2%} ({status})")