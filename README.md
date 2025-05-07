# 🦷 OdontoFast - Sistema Preditivo para Problemas Bucais

## 📋 Visão Geral

OdontoFast possui um sistema de análise preditiva para problemas bucais que utiliza técnicas de aprendizado de máquina para identificar riscos potenciais de pacientes desenvolverem problemas dentários. A ferramenta foi desenvolvida para auxiliar profissionais da odontologia na prevenção e planejamento de tratamentos personalizados.

## 📂 Conteúdo do Repositório

O repositório contém:

### 📊 Notebook de Análise e Treinamento
**Arquivo:** `OdontoFast_AnalisePreditivaFinal_.ipynb`
- 📈 **Análise exploratória** de dados odontológicos
- 🧹 **Pré-processamento** e preparação dos dados
- 🤖 **Construção e avaliação** de modelos preditivos (Random Forest, Gradient Boosting)
- 💾 **Treinamento e salvamento** do modelo final

### 💻 Aplicação Web
**Arquivo:** `app.py`
- 🖥️ Interface de usuário desenvolvida com **Streamlit**
- 📝 Formulário interativo para entrada de dados do paciente
- 📊 Visualização dinâmica dos resultados e recomendações
- 🔄 Sistema de backup para simulação quando o modelo treinado não está disponível

## ⚙️ Funcionalidades

### 🔮 Análise Preditiva
- 🚨 **Previsão de riscos** para diferentes problemas bucais (cárie, gengivite, periodontite, etc.)
- 🔍 **Identificação dos fatores críticos** que mais contribuem para o risco de cada paciente
- 📊 **Probabilidade percentual** de desenvolvimento de problemas bucais

### 👤 Interface do Usuário
- 📋 Formulário **intuitivo e responsivo** para entrada de dados do paciente
- 📊 **Visualização gráfica** clara e compreensível dos resultados
- 💡 **Recomendações personalizadas** com base no perfil de risco individual

## 📊 Variáveis Utilizadas

O sistema considera diversos fatores para a análise de risco:

| **Categoria** | **Variáveis** |
|---------------|---------------|
| 👤 **Dados demográficos** | Idade, gênero |
| 🪥 **Hábitos de higiene bucal** | Frequência de escovação, tempo de escovação, uso de fio dental, uso de enxaguante bucal |
| ⚠️ **Fatores de risco** | Tabagismo, consumo de açúcar, consumo de álcool |
| 📋 **Histórico médico** | Problemas bucais anteriores, histórico familiar |
| 🩺 **Cuidados preventivos** | Frequência de visitas ao dentista |

## 📈 Benefícios do Sistema

> ### *"Prevenir é melhor que remediar"*

- 🔍 **Identificação precoce** de riscos de problemas bucais
- 👤 **Personalização de planos preventivos** para cada paciente
- 🗣️ **Melhoria na comunicação** e educação do paciente sobre saúde bucal
- 💰 **Economia de custos** a longo prazo, evitando tratamentos mais complexos

## ⚠️ Limitações e Considerações

**IMPORTANTE:**
- 🩺 O sistema deve ser utilizado como **ferramenta de apoio à decisão**, sempre em conjunto com a avaliação profissional do dentista
- 📊 A precisão do modelo depende da **qualidade e quantidade dos dados** utilizados no treinamento
- 🧪 O modelo atual apresenta uma **acurácia moderada** e está em constante desenvolvimento

## 🛠️ Tecnologias Utilizadas

### Principais ferramentas:
```
🐍 Python       - Linguagem de programação principal
📊 Pandas/NumPy - Manipulação e processamento de dados
🤖 Scikit-learn - Construção de modelos de aprendizado de máquina
📈 Matplotlib   - Visualização de dados
🖥️ Streamlit    - Desenvolvimento da interface web
```

---

#### Nota de Implementação
Este sistema é um projeto em desenvolvimento e deve ser usado apenas como ferramenta complementar na prática odontológica. Todas as decisões clínicas devem ser baseadas primordialmente no julgamento profissional do dentista.
