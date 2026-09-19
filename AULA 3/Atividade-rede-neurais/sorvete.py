import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input

# 1. Preparação dos Dados
sorvete = pd.DataFrame({
    'temperatura': [18, 20, 24, 27, 30, 35],
    'vendas': [20, 25, 40, 55, 70, 100]
})

X = np.array(sorvete['temperatura'], dtype=np.float32).reshape(-1, 1)
y = np.array(sorvete['vendas'], dtype=np.float32)

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
temp_teste = np.array([[28.0]], dtype=np.float32)
previsao = modelo.predict(temp_teste)

print(f"Temperatura: {temp_teste[0][0]}°C -> Vendas previstas: {previsao[0][0]:.2f}")