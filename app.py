import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# Configuração da página
st.set_page_config(
    page_title="OdontoFast - Análise Preditiva",
    page_icon="🦷",
    layout="wide"
)

# Título e descrição
st.title("OdontoFast - Sistema de Análise Preditiva para Problemas Bucais")
st.markdown("### Prevendo riscos de problemas bucais com base no histórico e hábitos do paciente")

# Função para carregar o modelo
@st.cache_resource
def load_model():
    try:
        # Tente carregar o modelo
        model = joblib.load('modelo_problema_bucal.pkl')
        return model
    except:
        st.warning("Modelo não encontrado. Será utilizada uma simulação para demonstração.")
        return None

# Carregar modelo
model = load_model()

# Função para fazer previsões
def predict_risk(data):
    # Se o modelo foi carregado, use-o
    if model is not None:
        try:
            # Converter para DataFrame
            input_df = pd.DataFrame([data])
            # Fazer previsão
            prediction = model.predict(input_df)[0]
            prediction_proba = model.predict_proba(input_df)[0]
            
            # Extrair importância de recursos
            feature_importances = []
            for name, importance in zip(input_df.columns, model.feature_importances_):
                feature_importances.append({"nome": name, "importancia": importance})
            
            # Ordenar features por importância
            feature_importances = sorted(feature_importances, key=lambda x: x["importancia"], reverse=True)
            
            return {
                "prediction": prediction,
                "probability": max(prediction_proba) * 100,
                "features": feature_importances
            }
        except Exception as e:
            st.error(f"Erro ao fazer previsão: {e}")
            # Cair no modelo de simulação
            return simulate_prediction(data)
    else:
        # Usar simulação
        return simulate_prediction(data)

# Função para simular previsões (quando o modelo não está disponível)
def simulate_prediction(data):
    # Calcular pontuação de risco baseada nos fatores de risco
    risk_score = 0
    
    # Idade é um fator importante
    if data["idade"] > 60:
        risk_score += 25
    elif data["idade"] > 40:
        risk_score += 15
    elif data["idade"] > 30:
        risk_score += 5
    
    # Hábitos de higiene bucal
    if data["frequencia_escovacao"] < 2:
        risk_score += 30
    if data["uso_fio_dental"] == 0:
        risk_score += 25
    if data["tempo_escovacao"] < 2:
        risk_score += 20
    
    # Hábitos prejudiciais
    if data["fumante"] == 1:
        risk_score += 35
    if data["consumo_acucar_dia"] == 2:
        risk_score += 20
    elif data["consumo_acucar_dia"] == 1:
        risk_score += 10
    
    # Histórico
    if data["historico_problemas"] == 1:
        risk_score += 30
    if data["hist_prob_familiar"] == 1:
        risk_score += 15
    
    # Cuidados preventivos
    if data["visitas_ao_dentista"] == 0:
        risk_score += 25
    elif data["visitas_ao_dentista"] == 1:
        risk_score += 15
    
    # Outros fatores
    if data["uso_alcool"] == 2:
        risk_score += 15
    
    # Normalizar para probabilidade (0-100%)
    probability = min(risk_score / 2.5, 95)
    
    # Criar importância simulada para as características
    feature_importance = [
        {"nome": "Idade", "importancia": 0.20 if data["idade"] > 40 else 0.05},
        {"nome": "Frequência de escovação", "importancia": 0.25 if data["frequencia_escovacao"] < 2 else 0.05},
        {"nome": "Uso de fio dental", "importancia": 0.20 if data["uso_fio_dental"] == 0 else 0.05},
        {"nome": "Fumante", "importancia": 0.30 if data["fumante"] == 1 else 0.05},
        {"nome": "Histórico de problemas", "importancia": 0.25 if data["historico_problemas"] == 1 else 0.05},
        {"nome": "Visitas ao dentista", "importancia": 0.15 if data["visitas_ao_dentista"] < 2 else 0.05}
    ]
    
    # Ordenar por importância
    feature_importance = sorted(feature_importance, key=lambda x: x["importancia"], reverse=True)
    
    # Risco é binário: alto ou baixo
    prediction = 1 if probability > 50 else 0
    
    return {
        "prediction": prediction,
        "probability": probability,
        "features": feature_importance
    }

# Layout da interface com duas colunas
col1, col2 = st.columns([1, 1.5])

# Formulário para entrada de dados do paciente
with col1:
    st.markdown("### Dados do Paciente")
    
    with st.form("patient_form"):
        # Dados demográficos
        idade = st.number_input("Idade", min_value=1, max_value=120, value=30)
        genero = st.selectbox("Gênero", options=["Feminino", "Masculino"], index=0)
        
        # Hábitos de higiene bucal
        st.markdown("#### Hábitos de Higiene Bucal")
        frequencia_escovacao = st.selectbox(
            "Frequência de escovação diária",
            options=["1 vez ao dia", "2 vezes ao dia", "3 vezes ao dia", "Mais de 3 vezes ao dia"],
            index=1
        )
        tempo_escovacao = st.number_input("Tempo médio de escovação (minutos)", min_value=1, max_value=10, value=3)
        uso_fio_dental = st.radio("Usa fio dental", options=["Não", "Sim"], index=1)
        uso_enx_bucal = st.radio("Usa enxaguante bucal", options=["Não", "Sim"], index=0)
        
        # Fatores de risco
        st.markdown("#### Fatores de Risco")
        fumante = st.radio("Fumante", options=["Não", "Sim"], index=0)
        consumo_acucar = st.selectbox(
            "Consumo de açúcar",
            options=["Alto", "Médio", "Baixo"],
            index=1
        )
        uso_alcool = st.selectbox(
            "Consumo de álcool",
            options=["Alto", "Médio", "Baixo"],
            index=1
        )
        
        # Histórico médico
        st.markdown("#### Histórico Médico")
        historico_problemas = st.selectbox(
            "Histórico de problemas bucais",
            options=["Nenhum", "Cárie", "Canal", "Gengivite"],
            index=0
        )
        hist_prob_familiar = st.radio("Histórico familiar de problemas bucais", options=["Não", "Sim"], index=0)
        
        # Cuidados preventivos
        st.markdown("#### Cuidados Preventivos")
        visitas_ao_dentista = st.selectbox(
            "Frequência de visitas ao dentista",
            options=["Menos de 1 vez por ano", "1 vez por ano", "2 vezes por ano", "Mais de 2 vezes por ano"],
            index=1
        )
        
        # Botão de submit
        submit_button = st.form_submit_button("Analisar Risco")

# Preparar os dados para predição quando o formulário for enviado
if submit_button:
    # Mapear valores para numéricos
    data = {
        "idade": idade,
        "frequencia_escovacao": ["1 vez ao dia", "2 vezes ao dia", "3 vezes ao dia", "Mais de 3 vezes ao dia"].index(frequencia_escovacao),
        "uso_fio_dental": 1 if uso_fio_dental == "Sim" else 0,
        "uso_enx_bucal": 1 if uso_enx_bucal == "Sim" else 0,
        "fumante": 1 if fumante == "Sim" else 0,
        "historico_problemas": ["Nenhum", "Cárie", "Canal", "Gengivite"].index(historico_problemas),
        "hist_prob_familiar": 1 if hist_prob_familiar == "Sim" else 0,
        "genero": 1 if genero == "Masculino" else 0,
        "tempo_escovacao": tempo_escovacao,
        "consumo_acucar_dia": ["Alto", "Médio", "Baixo"].index(consumo_acucar),
        "visitas_ao_dentista": ["Menos de 1 vez por ano", "1 vez por ano", "2 vezes por ano", "Mais de 2 vezes por ano"].index(visitas_ao_dentista),
        "uso_alcool": ["Alto", "Médio", "Baixo"].index(uso_alcool)
    }
    
    # Fazer previsão
    result = predict_risk(data)
    
    # Mostrar resultado na coluna direita
    with col2:
        st.markdown("### Resultado da Análise")
        
        # Status do risco
        risk_status = "ALTO RISCO" if result["prediction"] == 1 else "BAIXO RISCO"
        probability = result["probability"]
        
        # Cores com base no risco
        if probability > 70:
            color = "#d73027"  # Vermelho escuro
        elif probability > 50:
            color = "#fc8d59"  # Laranja
        elif probability > 30:
            color = "#fee08b"  # Amarelo
        else:
            color = "#1a9850"  # Verde
        
        # Mostrar resultado principal
        st.markdown(f"""
        <div style="
            padding: 20px; 
            border-radius: 10px; 
            background-color: {'#ffebee' if risk_status == 'ALTO RISCO' else '#e8f5e9'};
            margin-bottom: 20px;
        ">
            <h2 style="color: {'#c62828' if risk_status == 'ALTO RISCO' else '#2e7d32'}; margin-bottom: 15px;">{risk_status}</h2>
            <h3>Probabilidade de problemas bucais: <span style="color: {color};">{probability:.1f}%</span></h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Recomendações
        st.markdown("### Recomendações")
        if risk_status == "ALTO RISCO":
            st.markdown("""
            - ⚠️ Agende uma consulta com seu dentista dentro dos próximos 30 dias
            - 🪥 Escove os dentes pelo menos 3 vezes ao dia, por 2-3 minutos
            - 🧵 Use fio dental diariamente
            - 🍬 Reduza o consumo de açúcar e alimentos ácidos
            - 🧪 Use enxaguante bucal com flúor
            """)
        else:
            st.markdown("""
            - ✅ Continue com as consultas regulares ao dentista (a cada 6 meses)
            - 🪥 Mantenha a rotina de higiene bucal
            - 🧵 Use fio dental regularmente
            - 💧 Beba bastante água
            """)
        
        # Gráfico de importância das características
        st.markdown("### Principais Fatores de Risco")
        
        # Criar DataFrame para o gráfico
        feature_df = pd.DataFrame(result["features"])
        
        # Limitar a 6 características mais importantes
        if len(feature_df) > 6:
            feature_df = feature_df.iloc[:6]
        
        # Criar figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Gráfico de barras horizontais
        bars = ax.barh(
            feature_df["nome"], 
            feature_df["importancia"], 
            color=sns.color_palette("Blues_r", len(feature_df))
        )
        
        # Adicionar valores nas barras
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 0.01, 
                bar.get_y() + bar.get_height()/2, 
                f'{width:.2f}', 
                va='center'
            )
        
        # Ajustar layout
        plt.xlabel('Importância')
        plt.title('Contribuição de cada fator para o risco')
        plt.tight_layout()
        
        # Mostrar o gráfico
        st.pyplot(fig)
        
        # Explicação
        st.markdown("""
        **O que isso significa?**  
        Este gráfico mostra os fatores que mais contribuem para seu nível de risco.
        Quanto maior a barra, maior a influência do fator na sua saúde bucal.
        """)

# Exibir informações sobre como usar o sistema quando nenhuma previsão foi feita ainda
if not submit_button:
    with col2:
        st.markdown("### Como funciona")
        st.info("""
        **Instruções:**
        1. Preencha todos os dados do paciente no formulário à esquerda
        2. Clique em "Analisar Risco" para obter uma previsão personalizada
        3. Analise o resultado e as recomendações
        
        O sistema usa um modelo de aprendizado de máquina treinado com dados de milhares de pacientes para prever riscos de problemas bucais no futuro.
        """)
        
        st.markdown("### Sobre o sistema")
        st.markdown("""
        O OdontoFast é um sistema de análise preditiva para problemas bucais que utiliza 
        técnicas de aprendizado de máquina para ajudar dentistas e pacientes a identificarem 
        riscos potenciais antes que se desenvolvam em problemas sérios.
        
        **Principais benefícios:**
        - Identificação precoce de riscos
        - Personalização de planos preventivos
        - Melhoria na educação do paciente sobre saúde bucal
        - Economia de custos a longo prazo
        
        Este sistema deve ser usado como ferramenta de apoio à decisão, sempre em conjunto com a avaliação profissional do dentista.
        """)

# Rodapé
st.markdown("---")
st.markdown("© 2023 OdontoFast - Sistema de Análise Preditiva para Problemas Bucais")