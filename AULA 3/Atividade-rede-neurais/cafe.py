import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input

# 1. Preparação dos Dados
cafe = pd.DataFrame({
    'xicaras': [1, 2, 3, 4, 5],
    'energia': [2, 4, 6, 8, 10]
})

X = np.array(cafe['xicaras'], dtype=np.float32).reshape(-1, 1)
y = np.array(cafe['energia'], dtype=np.float32)

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
xicaras_teste = np.array([[3.0]], dtype=np.float32)
previsao = modelo.predict(xicaras_teste)

print(f"Xícaras de café: {xicaras_teste[0][0]} -> Nível de energia: {previsao[0][0]:.2f} / 10")