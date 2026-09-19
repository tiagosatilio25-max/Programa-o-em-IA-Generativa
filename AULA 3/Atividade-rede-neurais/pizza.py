import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input

# 1. Preparação dos Dados
pizza = pd.DataFrame({
    'tamanho': [20, 25, 30, 35, 40],
    'preco': [20, 30, 40, 50, 60]
})

X = np.array(pizza['tamanho'], dtype=np.float32).reshape(-1, 1)
y = np.array(pizza['preco'], dtype=np.float32)

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
tamanho_teste = np.array([[32.0]], dtype=np.float32)
previsao = modelo.predict(tamanho_teste)

print(f"Tamanho: {tamanho_teste[0][0]} cm -> Preço previsto: R$ {previsao[0][0]:.2f}")