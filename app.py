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
        # Abrir e converter imagem para RGB se necessário
        image = Image.open(uploaded_file)
        
        # Converter RGBA para RGB se a imagem tiver transparência
        if image.mode == 'RGBA':
            image = image.convert('RGB')
            
        st.image(image, caption="Imagem enviada", use_column_width=True)

        # Enviar imagem para Roboflow
        st.info("🔍 Enviando imagem para análise...")
        
        # Configuração do cliente Roboflow
        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key="PEyV0064YFk1pNh46OS6"  # Sua chave API (considere usar variáveis de ambiente)
        )
        
        # Converter a imagem para bytes no formato JPEG
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)  # Voltar ao início do buffer
        
        # Inferência com tratamento de erros
        result = CLIENT.infer(img_bytes.getvalue(), model_id="candle-patterns/1")
        
        if result.get("predictions"):
            predictions = result["predictions"]
            if predictions:  # Verifica se há predições
                pattern = predictions[0].get("class", "Padrão não identificado")
                confidence = predictions[0].get("confidence", 0)
                
                st.success(f"**Padrão detectado**: {pattern} (Confiança: {confidence:.2%})")
                
                # Sugestões baseadas no padrão
                if "bullish" in pattern.lower():
                    st.markdown("✅ **Sugestão**: Potencial sinal de COMPRA")
                elif "bearish" in pattern.lower():
                    st.markdown("❌ **Sugestão**: Potencial sinal de VENDA")
                else:
                    st.markdown("➖ **Sugestão**: Manter posição ou aguardar confirmação")
            else:
                st.warning("⚠️ Nenhum padrão reconhecido foi detectado na imagem.")
        else:
            st.warning("⚠️ A API não retornou predições válidas. Verifique o modelo.")
            
    except requests.exceptions.RequestException as e:
        st.error(f"🔴 Erro de conexão com a API: {str(e)}")
    except Exception as e:
        st.error(f"🔴 Erro inesperado: {str(e)}")

# Rodapé
st.markdown("---")
st.caption("Versão 1.1 • Desenvolvido por Jefferson • Modelo hospedado via Roboflow")
