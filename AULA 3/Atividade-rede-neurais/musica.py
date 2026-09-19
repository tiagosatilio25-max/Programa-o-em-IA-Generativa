import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input

# 1. Preparação dos Dados
musica = pd.DataFrame({
    'bpm': [80, 90, 100, 120, 140],
    'viral': [1, 2, 4, 7, 10]
})

X = np.array(musica['bpm'], dtype=np.float32).reshape(-1, 1)
y = np.array(musica['viral'], dtype=np.float32)

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
bpm_teste = np.array([[110.0]], dtype=np.float32)
previsao = modelo.predict(bpm_teste)

print(f"BPM: {bpm_teste[0][0]} -> Chance de viralizar: {previsao[0][0]:.2f} / 10")