import streamlit as st
import json
from pathlib import Path
import plotly.graph_objects as go

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Job Market Intelligence", page_icon="💼", layout="wide")

# CSS Customizado para Centralização e Estilo
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #0077b5;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #666666;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    .footer-container {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #e6e9ef;
    }
    /* Estilo para os cards de métricas */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e6e9ef;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CARGA DE DADOS
gold_path = Path("data/gold/jobs_summary.json")

@st.cache_data
def load_data():
    if not gold_path.exists(): return None
    with open(gold_path, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()
if not data:
    st.error("Dados não encontrados. Rode o pipeline primeiro.")
    st.stop()

# 3. HEADER CENTRALIZADO
st.markdown("<h1 class='main-title'>💼 Job Market Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Análise estratégica de dados via Pipeline Medallion & GitHub Actions</p>", unsafe_allow_html=True)

# 4. MÉTRICAS (KPIs)
total = data.get("total_jobs", 0)
remote = data.get("remote_jobs", 0)
perc_remote = (remote / total * 100) if total > 0 else 0

c1, c2, c3 = st.columns(3)
with c1: st.metric("Oportunidades", f"{total:,}".replace(",", "."))
with c2: st.metric("Vagas Remotas", f"{remote:,}".replace(",", "."))
with c3: st.metric("Taxa de Trabalho Remoto", f"{perc_remote:.1f}%")

st.markdown("---")

# 5. EXPLICAÇÃO DA ARQUITETURA (O diferencial do seu portfólio)
with st.expander("🔍 Entenda a Engenharia por trás deste Dashboard"):
    st.markdown("""
    Este projeto utiliza uma **Arquitetura Medallion** automatizada:
    1. **Bronze (Raw):** Ingestão de dados brutos da API de empregos.
    2. **Silver (Clean):** Limpeza, desduplicação e normalização de tags.
    3. **Gold (Analytics):** Agregação de métricas e extração das Top 10 Skills.
    *Tudo orquestrado via **GitHub Actions** com ambientes Python isolados.*
    """)

# 6. FILTRO E GRÁFICO
tags_raw = data.get("top_10_tags", [])
dict_tags = {str(item[0]): int(item[1]) for item in tags_raw}

st.subheader("🎯 Tendências de Tecnologias")
opcoes = list(dict_tags.keys())
selecionadas = st.multiselect("Filtre as skills que deseja comparar:", opcoes, default=opcoes[:10])

if selecionadas:
    # Preparar dados filtrados e ordenados
    filtered_data = sorted([(s, dict_tags[s]) for s in selecionadas], key=lambda x: x[1])
    skills_plot = [x[0] for x in filtered_data]
    values_plot = [x[1] for x in filtered_data]

    fig = go.Figure(go.Bar(
        x=values_plot,
        y=skills_plot,
        orientation='h',
        text=values_plot,
        textposition='outside',
        marker_color='#0077b5',
        hovertemplate='<b>%{y}</b><br>Vagas: %{x}<extra></extra>'
    ))

    fig.update_layout(
        template="plotly_white",
        xaxis=dict(title="Volume de Vagas", showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(title=""),
        margin=dict(l=20, r=80, t=10, b=10),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

# 7. RODAPÉ CENTRALIZADO
st.markdown(f"""
    <div class="footer-container">
        <p>💡 <b>Status do Pipeline:</b> Operacional (Incremental Updates)</p>
        <p>Desenvolvido por João Cochet | Tech Stack: Python, UV, Medallion, Plotly</p>
    </div>
    """, unsafe_allow_html=True)

