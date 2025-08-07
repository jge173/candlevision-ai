import streamlit as st
from PIL import Image
import io
from inference_sdk import InferenceHTTPClient

st.set_page_config(page_title="Agente de IA Financeiro", layout="wide")
st.title("📊 Análise de Padrões de Velas com IA")

# Upload de imagem
uploaded_file = st.file_uploader("Envie uma imagem do gráfico de velas", type=["png", "jpg", "jpeg"])

if uploaded_file:
    try:
        # 1. Carregamento e conversão segura da imagem
        image = Image.open(uploaded_file)
        
        # Verificação e conversão de formato
        if image.mode in ('RGBA', 'P', 'LA'):
            image = image.convert('RGB')
            st.warning("⚠️ Imagem convertida para RGB para compatibilidade")
        
        # 2. Exibição da imagem processada
        st.image(image, 
                caption="Imagem enviada para análise",
                use_column_width=True,
                output_format="JPEG")

        # 3. Preparação para envio à API
        st.info("🔍 Enviando imagem para análise...")
        
        # Converter para bytes com tratamento explícito
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG', quality=95)
        img_data = img_buffer.getvalue()
        
        # 4. Configuração do cliente Roboflow
        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key="PEyV0064YFk1pNh46OS6"  # Lembre-se de usar variáveis de ambiente em produção
        )
        
        # 5. Chamada à API com tratamento robusto
        result = CLIENT.infer(img_data, model_id="candle-patterns/1")
        
        # 6. Processamento dos resultados
        if result and "predictions" in result:
            predictions = result["predictions"]
            if predictions:
                prediction = predictions[0]
                st.success(
                    f"**Padrão detectado:** {prediction['class'].upper()}\n"
                    f"**Confiança:** {prediction['confidence']:.2%}"
                )
                
                # Sugestões de trading
                if "bullish" in prediction['class'].lower():
                    st.markdown("🟢 **Sugestão:** Posição de COMPRA")
                    st.progress(prediction['confidence'])
                elif "bearish" in prediction['class'].lower():
                    st.markdown("🔴 **Sugestão:** Posição de VENDA")
                    st.progress(prediction['confidence'])
                else:
                    st.markdown("🟡 **Sugestão:** Manter posição atual")
            else:
                st.warning("⚠️ Nenhum padrão reconhecível detectado")
        else:
            st.warning("⚠️ A análise não retornou resultados válidos")

    except Exception as e:
        st.error(f"❌ Erro no processamento: {str(e)}")
        st.error("Dica: Tente enviar a imagem novamente ou em outro formato")

# Rodapé profissional
st.markdown("---")
st.caption("""
**Versão 2.0** • Sistema de análise de padrões candlestick •  
Desenvolvido por Jefferson • Modelo hospedado via Roboflow API  
Última atualização: Agosto 2024
""")
