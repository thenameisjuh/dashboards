import streamlit as st
import pandas as pd
import plotly.express as px
import os
import random

df_f = pd.DataFrame() 

# --- 1. CONFIGURAÇÃO DA PÁGINA (Sempre o primeiro comando) ---
st.set_page_config(page_title="Horos HD - O Oráculo", layout="wide", initial_sidebar_state="expanded")

# --- 2. ESTILO CSS CUSTOMIZADO (Aesthetic Midnight, Blue & Gold) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400;600&display=swap');
    
    /* FUNDO E TEXTO BASE */
    .stApp { 
        background: radial-gradient(circle at top, #0A192F 0%, #02050A 100%); 
        color: #E2E8F0; 
    }
    
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #FFD700 !important; text-align: center; }

    /* CARDS DE MÉTRICAS (KPIs) - ABAIXO DO TÍTULO */
    [data-testid="stMetricLabel"] { 
        width: 100;
        text-align: center;
        color: #FFD700 !important; /* Dourado para o nome da métrica */
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    [data-testid="stMetricValue"] { 
        width: 100%;
        text-align: center;
        color: #FFFFFF !important; /* Branco para o número */
        font-size: 2rem !important;
    }
    div[data-testid="stMetric"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        background: rgba(10, 25, 47, 0.6) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.05);
        backdrop-filter: blur(10px);
    }

    /* CARTAS DE TAROT */
    .tarot-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 15px;
        padding: 20px;
        height: 260px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .tarot-card:hover {
        transform: translateY(-10px);
        border: 1px solid #FFD700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.15);
    }
    .tarot-card h4 { color: #FFD700 !important; margin-bottom: 10px; font-size: 0.95rem; }
    .tarot-card p { color: #A2D2FF !important; font-size: 0.8rem; }

    /* BOTÕES (Consultar e Fechar) */
    .stButton > button {
        background-color: rgba(10, 25, 47, 0.8) !important;
        color: #FFD700 !important;
        border: 1px solid #FFD700 !important;
        border-radius: 20px !important;
        transition: 0.4s all;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #FFD700 !important;
        color: #0A192F !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
    }

    /* BOX DO VATICÍNIO */
    .vaticinio-box {
        background: rgba(255, 215, 0, 0.05);
        border: 2px solid #FFD700;
        border-radius: 20px;
        padding: 30px;
        margin-top: 25px;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MOTOR DE DADOS ---
@st.cache_data
def load_data():
    file = 'humanidades_digitais_def.csv'
    if not os.path.exists(file): return None
    try:
        df = pd.read_csv(file, sep=';')
        df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        df['pdf_page_count'] = pd.to_numeric(df['pdf_page_count'], errors='coerce').fillna(0).astype(int)
        df['primary_category_label'] = df['primary_category_label'].fillna("Outros")
        return df
    except: return None

df = load_data()

# --- 4. FUNÇÃO: GERADOR DE PROFECIAS DINÂMICO ---
def construir_mensagem_mistica(row):
    interpretacoes_casa = {
        "Edição digital": "a claridade textual e a preservação da palavra",
        "Património digital": "o resgate de memórias ancestrais e a reconstrução de mundos",
        "Arquivos e bibliotecas digitais": "a organização de saberes infinitos e a guarda do conhecimento",
        "Métodos computacionais aplicados às humanidades": "a precisão algorítmica fundida com a alma humana",
        "Humanidades espaciais / GIS": "o mapeamento de territórios invisíveis e trajetórias perdidas"
    }
    
    casa = row['primary_category_label']
    signo_desc = interpretacoes_casa.get(casa, "a exploração de novas fronteiras digitais")
    
    paginas = row['pdf_page_count']
    if paginas > 200: magnitude_txt = "uma obra de densidade monumental, revelando um esforço hercúleo"
    elif paginas > 100: magnitude_txt = "um equilíbrio perfeito entre a teoria densa e a prática inovadora"
    else: magnitude_txt = "uma faísca de inovação rápida, focada e certeira"
        
    aura = str(row['keywords']).replace('|', ' e ').split(' e ')
    aura_principal = aura[0] if len(aura) > 0 else "conhecimento"
    
    return (
        f"O alinhamento da casa de <b>{casa}</b> revela <b>{signo_desc}</b>. "
        f"Esta estrela manifesta-se através de <b>{aura_principal}</b>, apresentando-se como <b>{magnitude_txt}</b>. "
        f"Os astros do ciclo de <b>{row['year']}</b> indicam que este trabalho será um guia fundamental no firmamento das Humanidades Digitais."
    )

# --- 5. LÓGICA DE INTERFACE ---
if df is not None:
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔮 O Oráculo")
        search_q = st.text_input("🔍 Procurar no Cosmos", "")
        anos_validos = sorted([a for a in df['year'].unique() if a > 0])
        sel_anos = st.select_slider("Ciclo Temporal", options=anos_validos, value=(min(anos_validos), max(anos_validos)))
        
        todas_cats = sorted(df['primary_category_label'].unique().tolist())
        sel_cats = st.multiselect("Casas Ativas", todas_cats, default=todas_cats)

    # Filtragem Global
    mask = (df['year'] >= sel_anos[0]) & (df['year'] <= sel_anos[1])
    if sel_cats: mask &= df['primary_category_label'].isin(sel_cats)
    if search_q: mask &= (df['title'].str.contains(search_q, case=False, na=False) | 
                         df['primary_author'].str.contains(search_q, case=False, na=False))
    df_f = df[mask]

    # Cabeçalho
    st.markdown("<h1>Oráculo Humanitas</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8892B0; margin-top: -15px;'>Mapeamento de Humanidades Digitais • UMinho</p>", unsafe_allow_html=True)
# --- LOGICA DE EXIBIÇÃO (Coloca isto depois de criares o df_f) ---

if df_f.empty:
    # Mensagem quando não há resultados
    st.markdown(f"""
        <div style="text-align: center; padding: 100px 20px;">
            <h1 style="font-size: 5rem; margin-bottom: 20px;">🌙</h1>
            <h2 style="color: #FFD700; font-family: 'Playfair Display';">O oráculo está nublado...</h2>
            <p style="color: #8892B0; font-size: 1.2rem;">Não existem estrelas que correspondam a essa busca no firmamento de HD.</p>
            <p style="color: #475569; font-size: 0.9rem;">Tenta ajustar os filtros ou pesquisar por outro termo.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    # KPIs (Métricas abaixo do título)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Estrelas (Teses)", len(df_f))
    m2.metric("Mestres (Autores)", df_f['primary_author'].nunique())
    m3.metric("Casas (Áreas)", df_f['primary_category_label'].nunique())
    m4.metric("Magnitude Média", f"{int(df_f['pdf_page_count'].mean())} pág.")

    st.write("---")

    # --- 6. VISÃO MACRO (RODA DO ZODÍACO) ---
    st.markdown("## ☯️ A Roda das Casas")
    fig_wheel = px.sunburst(
        df_f, path=['primary_category_label', 'document_type_normalized'], 
        color='year', color_continuous_scale='Blues', template="plotly_dark"
    )
    fig_wheel.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, l=10, r=10, b=10))
    st.plotly_chart(fig_wheel, use_container_width=True)

    st.write("---")

    # --- 7. VISÃO MICRO (BARALHO DE TAROT) ---
    st.markdown("## 🃏 O Baralho das Humanidades")
    
    # Grelha de Cartas (4 por linha)
    num_cards = 12 
    display_df = df_f.head(num_cards)
    
    for i in range(0, len(display_df), 4):
        cols = st.columns(4)
        chunk = display_df.iloc[i:i+4]
        for j, (idx, row) in enumerate(chunk.iterrows()):
            with cols[j]:
                st.markdown(f"""
                    <div class="tarot-card">
                        <p style="text-transform: uppercase; letter-spacing: 1px;">{row.primary_category_label}</p>
                        <h4>{row.title[:65]}...</h4>
                        <p>{row.primary_author} • {row.year}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Consultar Vaticínio", key=f"btn_{idx}"):
                    st.session_state['selected_idx'] = idx

    # Exibição do Vaticínio Detalhado
    if 'selected_idx' in st.session_state:
        t = df.loc[st.session_state['selected_idx']]
        profecia = construir_mensagem_mistica(t)
        
        st.markdown(f"""
            <div class="vaticinio-box">
                <h2 style="text-align: left; margin-top: 0;">✨ Vaticínio Estelar</h2>
                <p style="font-size: 1.4rem; color: #FFD700;"><b>{t['title']}</b></p>
                <p style="color: #A2D2FF;"><b>Mestre:</b> {t['primary_author']} | <b>Ciclo:</b> {t['year']}</p>
                <hr style="border-color: rgba(255, 215, 0, 0.2); margin: 20px 0;">
                <div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 15px; border-left: 4px solid #FFD700;">
                    <p style="font-size: 1.1rem; line-height: 1.6; color: #E2E8F0;"><i>"{profecia}"</i></p>
                </div>
                <p style="margin-top: 20px; font-size: 0.9rem;"><b>Energias:</b> <span style="color: #FFD700;">{str(t['keywords']).replace('|', ' • ')}</span></p>
                <details style="margin-top: 15px; cursor: pointer; color: #8892B0;">
                    <summary style="color: #A2D2FF;">Revelar Manuscrito Original (Abstract)</summary>
                    <p style="font-size: 0.85rem; padding-top: 10px; color: #BDC3C7;">{t['abstract']}</p>
                </details>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🌌 Fechar Vaticínio"):
            del st.session_state['selected_idx']
            st.rerun()

        st.markdown("<p style='text-align: center; color: #475569; padding: 50px;'>Oráculo Supremo v6.0 • UC Projeto Integrado • UMinho</p>", unsafe_allow_html=True)
    else:
        st.error("O Oráculo está nublado. O ficheiro CSV não foi detetado.")
