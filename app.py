from roboflow import InferenceHTTPClient
import streamlit as st
from PIL import Image
import tempfile

# Inicializa o cliente Roboflow
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="PEyV0064YFk1pNh46OS6"
)

# Nome do projeto e versão do modelo
PROJECT = "CandleVisionAI-2"  # substituído conforme imagem
VERSION = "v2"                # versão correta conforme imagem

# Configuração da interface Streamlit
st.set_page_config(page_title="CandleVisionAI - Análise de Mercado", layout="centered")
st.title("📊 CandleVisionAI - Análise de Mercado Financeiro")
st.markdown("""
Este aplicativo permite enviar gráficos de velas (candlestick) e utiliza um modelo treinado no Roboflow para identificar padrões e gerar sinais de decisão.
""")

# Upload da imagem
uploaded_file = st.file_uploader("📁 Envie uma imagem do gráfico (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Gráfico enviado", use_column_width=True)

    # Salva a imagem temporariamente
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Faz a inferência com o modelo Roboflow
    try:
        result = CLIENT.infer(tmp_path, model_id=f"{PROJECT}/{VERSION}")
        st.success("✅ Análise concluída com sucesso!")
        st.subheader("🧠 Resultado da Inferência")
        st.json(result)
    except Exception as e:
        st.error(f"❌ Erro ao conectar com o modelo: {e}")

st.markdown("---")
st.caption("Versão 1.0 • Desenvolvido por Jefferson • Modelo hospedado via Roboflow")
