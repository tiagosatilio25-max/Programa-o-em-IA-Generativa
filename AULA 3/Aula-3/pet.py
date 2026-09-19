import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input

# 1. Preparação dos Dados
pets = pd.DataFrame({
    'passeios': [1, 2, 3, 4, 5],
    'felicidade': [2, 4, 5, 8, 10]
})

X = np.array(pets['passeios'], dtype=np.float32).reshape(-1, 1)
y = np.array(pets['felicidade'], dtype=np.float32)

# 2. Definição do Modelo
modelo = Sequential([
    Input(shape=(1,)),
    Dense(units=1)
])

# 3. Compilação
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.05),
    loss='mean_squared_error'
)

# 4. Treinamento
modelo.fit(X, y, epochs=600, verbose=0)

# 5. Predição
passeios_teste = np.array([[3.0]], dtype=np.float32)
previsao = modelo.predict(passeios_teste)

print(f"Passeios: {passeios_teste[0][0]} -> Felicidade prevista: {previsao[0][0]:.2f} / 10")