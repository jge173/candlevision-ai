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
    try:
        # Abrir e converter imagem se necessário
        image = Image.open(uploaded_file)
        
        # Verificar e converter formato da imagem
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
            st.warning("⚠️ Imagem convertida de RGBA/P para RGB para compatibilidade")
            
        st.image(image, caption="Imagem enviada", use_column_width=True)

        # Enviar imagem para Roboflow
        st.info("🔍 Enviando imagem para análise...")
        
        # Configuração do cliente Roboflow
        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key="PEyV0064YFk1pNh46OS6"  # Sua chave API
        )
        
        # Converter imagem para bytes antes de enviar
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Usando o método correto do InferenceHTTPClient
        result = CLIENT.infer(img_byte_arr.getvalue(), model_id="candle-patterns/1")
        
        if result.get("predictions"):
            predictions = result["predictions"]
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
            
    except Exception as e:
        st.error(f"Erro ao processar imagem: {str(e)}")

st.markdown("---")
st.caption("Versão: 1.0 - Desenvolvido por Jefferson - Modelo hospedado via Roboflow")
st.caption("Versão 1.0 • Desenvolvido por Jefferson • Modelo hospedado via Roboflow")

