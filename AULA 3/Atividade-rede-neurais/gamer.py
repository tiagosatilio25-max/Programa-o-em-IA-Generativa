import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
import pandas as pd
import numpy as np

# ==========================================
# 2. Detector de Sono Gamer
# Objetivo: Prever o nível de cansaço baseado em horas jogando
# Modelo: Regressão Linear Simples
# ==========================================

# 1. Preparação dos Dados
gamer = pd.DataFrame({
    'horas_jogo': [1, 2, 4, 6, 8, 10],
    'cansaco': [1, 2, 3, 5, 8, 10]
})

# Separando as variáveis preditoras (features) e o alvo (target)
# Adequando o formato dos dados para NumPy arrays do tipo float32 bidimensionais
X = np.array(gamer['horas_jogo'], dtype=np.float32).reshape(-1, 1)
y = np.array(gamer['cansaco'], dtype=np.float32)

print("Horas jogadas (Entrada):", X.flatten())
print("Nível de cansaço (Alvo):", y)
print("-" * 40)

# 2. Definição do Modelo (Arquitetura)
# Para implementar a Regressão Linear com o TensorFlow/Keras, 
# utilizamos uma camada de Entrada e uma camada Densa com 1 neurônio.
modelo = Sequential([
    Input(shape=(1,)),
    Dense(units=1)
])

# 3. Compilação do Modelo
# Usamos o otimizador Adam (com taxa de aprendizado ajustada) para melhor convergência
# e o Erro Quadrático Médio (MSE) como função de perda para regressão.
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.05),
    loss='mean_squared_error'
)

# Exibindo o resumo da arquitetura do modelo
modelo.summary()
print("-" * 40)

# 4. Treinamento (Fit)
# Treinamos o modelo por 600 épocas para otimizar os pesos
print("Treinando o Detector de Sono Gamer...")
historico = modelo.fit(X, y, epochs=600, verbose=0)
print("Treinamento concluído!")
print("-" * 40)

# 5. Realizando Predições
# Prevendo o nível de cansaço para um gamer que jogou por 7 horas
horas_teste = np.array([[7.0]], dtype=np.float32)
previsao = modelo.predict(horas_teste)

print(f"Previsão para {horas_teste[0][0]:.0f} horas seguidas de jogo:")
print(f"Nível de cansaço estimado: {previsao[0][0]:.2f} / 10")