import streamlit as st
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Simulador de Detecção de Objetos",
    page_icon="🤖",
    layout="centered",
)

st.title("Simulador de Visão Computacional (Regras)")
st.write(
    "Envie uma imagem para simular a identificação de objetos (Pessoa, Carro,"
    " Animal)."
)

# Upload de imagem
uploaded_file = st.file_uploader(
    "Escolha uma imagem (JPG, PNG)...", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption="Imagem Enviada", use_column_width=True)

  st.markdown("---")
  st.subheader("Resultado da Simulação")

  # Simulação baseada em regras/heurística demonstrativa
  if st.button("Executar Análise"):
    with st.spinner("Analisando características da imagem..."):
      # Simulação de detecção para fins acadêmicos/demonstrativos
      st.success("Análise concluída com sucesso!")

      # Exibição de métricas simuladas
      col1, col2, col3 = st.columns(3)
      with col1:
        st.metric(label="Pessoa", value="Detectado", delta="98% conf.")
      with col2:
        st.metric(label="Carro", value="Não detectado", delta="-")
      with col3:
        st.metric(label="Animal", value="Possível (Cachorro)", delta="85% conf.")