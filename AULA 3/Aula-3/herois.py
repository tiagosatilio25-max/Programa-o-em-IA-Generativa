import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input

# 1. Preparação dos Dados
herois = pd.DataFrame({
    'forca': [1, 2, 3, 7, 8, 10],
    'heroi': [0, 0, 0, 1, 1, 1]
})

X = np.array(herois['forca'], dtype=np.float32).reshape(-1, 1)
y = np.array(herois['heroi'], dtype=np.float32)

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
forca_teste = np.array([[5.0]], dtype=np.float32)
probabilidade = modelo.predict(forca_teste)[0][0]
categoria = "Forte" if probabilidade >= 0.5 else "Fraco"

print(f"Força: {forca_teste[0][0]} -> Probabilidade de ser Forte: {probabilidade:.2%} ({categoria})")