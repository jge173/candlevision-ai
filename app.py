import streamlit as st
import requests
from PIL import Image
import io
from inference_sdk import InferenceHTTPClient

st.set_page_config(page_title="Agente de IA Financeiro", layout="wide")
st.title("📊 Análise de Padrões de Velas com IA")

# Upload de imagem
uploaded_file = st.file_uploader("Envie uma imagem do gráfico de velas", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem enviada", use_column_width=True)

    # Enviar imagem para Roboflow
    st.info("🔍 Enviando imagem para análise...")
    
    CLIENT = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key="PEyV0064YFk1pNh46OS6"
    )


    response = requests.post(
        api_url,
        files={"file": uploaded_file},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if response.status_code == 200:
        result = response.json()
        predictions = result.get("predictions", [])
        if predictions:
            pattern = predictions[0]["class"]
            confidence = predictions[0]["confidence"]
            st.success(f"Padrão detectado: **{pattern}** com confiança de {confidence:.2%}")
            if "bullish" in pattern.lower():
                st.markdown("✅ **Sugestão de entrada**: Compra")
            elif "bearish" in pattern.lower():
                st.markdown("🚫 **Sugestão de entrada**: Venda")
            else:
                st.markdown("🔄 **Sugestão de entrada**: Manter posição")
        else:
            st.warning("Nenhum padrão detectado com alta confiança.")
    else:
        st.error("Erro ao conectar com a API do Roboflow.")

st.markdown("---")
st.caption("Versão 1.0 • Desenvolvido por Jefferson • Modelo hospedado via Roboflow")






