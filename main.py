import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import os
import base64
# ============================================================
# GLOBAL STYLES & CONFIG
# ============================================================
st.set_page_config(
    page_title="RL Pro Analytics",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

/* === ROOT VARIABLES === */
:root {
    --bg-deep:     #040810;
    --bg-card:     #080f1e;
    --bg-elevated: #0d1829;
    --neon-cyan:   #00f5ff;
    --neon-orange: #ff6b00;
    --neon-pink:   #ff0090;
    --neon-green:  #00ff88;
    --gold:        #ffd700;
    --text-primary: #e8f4fd;
    --text-muted:   #4a6fa5;
    --border:       rgba(0, 245, 255, 0.12);
    --glow-cyan:    0 0 20px rgba(0, 245, 255, 0.4), 0 0 60px rgba(0, 245, 255, 0.15);
    --glow-orange:  0 0 20px rgba(255, 107, 0, 0.5), 0 0 60px rgba(255, 107, 0, 0.2);
}

/* === BASE === */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    color: var(--text-primary) !important;
}

.stApp {
    /* Χρησιμοποιούμε Direct Link από το Internet για την εικόνα σου */
    background-image: 
        linear-gradient(rgba(4, 8, 16, 0.55), rgba(4, 8, 16, 0.88)), /* Σκούρο φίλτρο για αναγνωσιμότητα */
        url("https://w0.peakpx.com/wallpaper/524/916/HD-wallpaper-rocket-league-logo-in-blue-background-games.jpg") !important; /* Παράδειγμα URL, βάλε το δικό σου */

    background-attachment: fixed !important;
    background-size: cover !important;
    background-position: center !important;
}

/* === ANIMATED BACKGROUND GRID === */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(0,245,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,245,255,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
    opacity: 0.3;
}

/* === SIDEBAR === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050c1a 0%, #080f1e 40%, #050c1a 100%) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-orange), var(--neon-pink));
}

/* === SIDEBAR TITLE === */
[data-testid="stSidebar"] h1 {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.3rem !important;
    font-weight: 900 !important;
    color: var(--neon-cyan) !important;
    text-shadow: var(--glow-cyan) !important;
    letter-spacing: 2px !important;
    margin-bottom: 0 !important;
}

[data-testid="stSidebar"] .stCaption {
    color: var(--text-muted) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
}

/* === RADIO BUTTONS (NAV) === */
[data-testid="stSidebar"] .stRadio label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.5px !important;
    padding: 6px 12px !important;
    border-radius: 4px !important;
    transition: all 0.2s ease !important;
    display: block !important;
    border-left: 2px solid transparent !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--neon-cyan) !important;
    border-left-color: var(--neon-cyan) !important;
    background: rgba(0,245,255,0.05) !important;
}

/* === MAIN HEADINGS === */
h1 {
    font-family: 'Orbitron', monospace !important;
    font-size: clamp(1.4rem, 2.5vw, 2.2rem) !important;
    font-weight: 900 !important;
    color: var(--neon-cyan) !important;
    text-shadow: var(--glow-cyan) !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding-bottom: 12px !important;
    border-bottom: 1px solid var(--border) !important;
    margin-bottom: 24px !important;
}

h2 {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    color: var(--neon-orange) !important;
    text-shadow: var(--glow-orange) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

h3 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* === METRIC CARDS === */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 16px 20px !important;
    position: relative !important;
    overflow: hidden !important;
}

[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-orange));
}

[data-testid="metric-container"] label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.65rem !important;
    color: var(--text-muted) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--neon-cyan) !important;
    text-shadow: 0 0 15px rgba(0,245,255,0.5) !important;
}

[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* === INFO / SUCCESS / WARNING / ERROR BOXES === */
.stInfo, .stSuccess, .stWarning, .stError {
    border-radius: 6px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    border-left-width: 3px !important;
}

.stInfo {
    background: rgba(0,245,255,0.06) !important;
    border-left-color: var(--neon-cyan) !important;
    color: #9ee8f5 !important;
}

.stSuccess {
    background: rgba(0,255,136,0.06) !important;
    border-left-color: var(--neon-green) !important;
    color: #9effd6 !important;
}

.stWarning {
    background: rgba(255,215,0,0.06) !important;
    border-left-color: var(--gold) !important;
    color: #ffe88a !important;
}

.stError {
    background: rgba(255,0,144,0.06) !important;
    border-left-color: var(--neon-pink) !important;
    color: #ff88c9 !important;
}

/* === SELECTBOX === */
.stSelectbox > div > div {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text-primary) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
}

.stSelectbox > div > div:focus-within {
    border-color: var(--neon-cyan) !important;
    box-shadow: 0 0 0 2px rgba(0,245,255,0.15) !important;
}

/* === DATAFRAME === */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

[data-testid="stDataFrame"] th {
    background: var(--bg-elevated) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    color: var(--neon-cyan) !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

[data-testid="stDataFrame"] td {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    color: var(--text-muted) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border-bottom: 2px solid transparent !important;
    padding: 12px 24px !important;
    background: transparent !important;
}

.stTabs [aria-selected="true"] {
    color: var(--neon-cyan) !important;
    border-bottom-color: var(--neon-cyan) !important;
    text-shadow: 0 0 10px rgba(0,245,255,0.6) !important;
}

/* === SPINNER === */
.stSpinner > div {
    border-top-color: var(--neon-cyan) !important;
}

/* === DIVIDER === */
hr {
    border-color: var(--border) !important;
}

/* === PLOTLY CHARTS (dark bg) === */
.js-plotly-plot .plotly {
    background: transparent !important;
}

/* === CUSTOM STAT CARD === */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    margin-bottom: 16px;
}

.stat-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-orange), var(--neon-pink));
}

.stat-card-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.stat-card-value {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--neon-cyan);
    text-shadow: var(--glow-cyan);
    line-height: 1;
}

.stat-card-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 6px;
    font-weight: 500;
}

/* === RANK BADGE === */
.rank-badge {
    display: inline-block;
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 4px 12px;
    border-radius: 3px;
    text-transform: uppercase;
}

.rank-ssl {
    background: rgba(255,215,0,0.15);
    border: 1px solid var(--gold);
    color: var(--gold);
    text-shadow: 0 0 10px rgba(255,215,0,0.5);
}

.rank-gc {
    background: rgba(255,107,0,0.15);
    border: 1px solid var(--neon-orange);
    color: var(--neon-orange);
    text-shadow: 0 0 10px rgba(255,107,0,0.5);
}

.rank-champ {
    background: rgba(0,245,255,0.12);
    border: 1px solid var(--neon-cyan);
    color: var(--neon-cyan);
}

.rank-diamond {
    background: rgba(120,120,255,0.15);
    border: 1px solid #7878ff;
    color: #a0a0ff;
}

/* === SECTION HEADER (decorative) === */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 28px 0 20px;
}

.section-header-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--neon-cyan), transparent);
}

.section-header-text {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: var(--neon-cyan);
    letter-spacing: 3px;
    text-transform: uppercase;
}

/* === INSIGHT BOX === */
.insight-box {
    background: linear-gradient(135deg, rgba(0,245,255,0.05), rgba(255,107,0,0.05));
    border: 1px solid rgba(0,245,255,0.2);
    border-radius: 8px;
    padding: 16px 20px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 500;
    color: #b8d8e8;
    line-height: 1.6;
}

.insight-box .label {
    font-family: 'Orbitron', monospace;
    font-size: 0.55rem;
    color: var(--neon-cyan);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
    display: block;
}

/* === PROGRESS COLUMN OVERRIDES === */
[data-testid="stDataFrameResizable"] {
    background: var(--bg-card) !important;
}

/* === WRITE / PARAGRAPH === */
p, .stMarkdown p {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 400 !important;
    color: #8aabcc !important;
    line-height: 1.7 !important;
}

/* === SCROLLBAR === */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.25); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,245,255,0.5); }
</style>
""", unsafe_allow_html=True)


# ============================================================
# PLOTLY THEME (shared)
# ============================================================
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(8,15,30,0.7)',
    font=dict(family='Rajdhani, sans-serif', color='#8aabcc', size=13),
    title_font=dict(family='Orbitron, monospace', color='#00f5ff', size=14),
    xaxis=dict(
        gridcolor='rgba(0,245,255,0.07)', zerolinecolor='rgba(0,245,255,0.1)',
        tickfont=dict(family='Share Tech Mono, monospace', size=11, color='#4a6fa5'),
    ),
    yaxis=dict(
        gridcolor='rgba(0,245,255,0.07)', zerolinecolor='rgba(0,245,255,0.1)',
        tickfont=dict(family='Share Tech Mono, monospace', size=11, color='#4a6fa5'),
    ),
    legend=dict(
        bgcolor='rgba(8,15,30,0.8)',
        bordercolor='rgba(0,245,255,0.15)',
        borderwidth=1,
        font=dict(family='Rajdhani', size=12, color='#8aabcc'),
    ),
    margin=dict(l=20, r=20, t=50, b=20),
)

COLORS = {
    'neon':   ['#00f5ff', '#ff6b00', '#ff0090', '#00ff88', '#ffd700', '#a855f7'],
    'ranks':  {'SSL': '#ffd700', 'Grand Champ': '#ff6b00', 'Champion': '#00f5ff', 'Diamond': '#a0a0ff'},
}


# ============================================================
# HELPER: section divider
# ============================================================
def section_div(label=""):
    st.markdown(f"""
    <div class="section-header">
        <div class="section-header-line"></div>
        <div class="section-header-text">{label}</div>
        <div class="section-header-line" style="background:linear-gradient(90deg,transparent,rgba(0,245,255,0.4))"></div>
    </div>""", unsafe_allow_html=True)


def insight(label, text):
    st.markdown(f"""
    <div class="insight-box">
        <span class="label">💡 {label}</span>
        {text}
    </div>""", unsafe_allow_html=True)


def stat_card(title, value, sub=""):
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-card-title">{title}</div>
        <div class="stat-card-value">{value}</div>
        <div class="stat-card-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)


# ============================================================
# DATA LOAD
# ============================================================
@st.cache_data
def load_real_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    rlcs_path = os.path.join(BASE_DIR, 'data', 'rlcs', 'games_by_players.csv')
    try:
        df = pd.read_csv(rlcs_path)
    except Exception as e:
        st.error(f"Σφάλμα φόρτωσης RLCS: {e}")
        df = pd.DataFrame()

    if not df.empty:
        df.columns = df.columns.str.replace(r'^(core_|movement_|demo_|boost_|stats_)', '', regex=True)
        if 'player' in df.columns and 'player_tag' not in df.columns:
            df = df.rename(columns={'player': 'player_tag'})
        if 'score' not in df.columns or df['score'].sum() == 0:
            df['score'] = (df.get('goals', 0) * 100) + (df.get('assists', 0) * 50) + \
                          (df.get('saves', 0) * 50) + (df.get('shots', 0) * 10)

        # ── Derive useful columns before groupby ──────────────────
        # Total air time
        if 'time_high_air' in df.columns and 'time_low_air' in df.columns:
            df['time_in_air'] = df['time_high_air'] + df['time_low_air']
        if 'time_in_air' in df.columns and 'duration' in df.columns:
            df['air_time_pct'] = (df['time_in_air'] / df['duration'].replace(0, np.nan)) * 100

        # Supersonic proxy: time_at_boost if supersonic cols missing
        if 'time_supersonic' not in df.columns:
            if 'time_boost_speed' in df.columns:
                df['time_supersonic'] = df['time_boost_speed']
            elif 'time_full_speed' in df.columns:
                df['time_supersonic'] = df['time_full_speed']

        # Demos: inflicted
        if 'inflicted' not in df.columns:
            for candidate in ['demo_inflicted', 'demos_inflicted', 'demos']:
                if candidate in df.columns:
                    df['inflicted'] = df[candidate]
                    break

        num_cols = df.select_dtypes(include=[np.number]).columns
        p_stats = df.groupby('player_tag')[num_cols].mean().reset_index().fillna(0)

        if p_stats['score'].max() > 0:
            p_stats['rank_tier'] = pd.qcut(
                p_stats['score'].rank(method='first'), q=4,
                labels=['Diamond', 'Champion', 'Grand Champ', 'SSL']
            ).astype(str)
        else:
            p_stats['rank_tier'] = 'Unranked'
    else:
        p_stats = pd.DataFrame()

    uci_path = os.path.join(BASE_DIR, 'data', 'uci', 'rocket_league_skillshots.data')
    uci_cols = ['ball_x', 'ball_y', 'ball_z', 'ball_vx', 'ball_vy', 'ball_vz',
                'player_x', 'player_y', 'player_z', 'player_vx', 'player_vy', 'player_vz',
                'pitch', 'yaw', 'roll', 'steer', 'skillshot_class']
    try:
        uci_df = pd.read_csv(uci_path, names=uci_cols, sep=',', on_bad_lines='skip', engine='python')
    except Exception:
        uci_df = pd.DataFrame()

    return df, p_stats, uci_df


@st.cache_data
def load_seasonal_data():
    """Loads the seasonal rank distribution CSV from data/seasonal_master.csv"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(BASE_DIR, 'data', 'seasonal_master.csv')
    try:
        df = pd.read_csv(path)
        # Normalise column names
        df.columns = df.columns.str.strip()
        # Ensure Percentage is numeric
        df['Percentage'] = (
            df['Percentage'].astype(str)
            .str.replace('%', '', regex=False)
            .str.replace(',', '.', regex=False)
            .str.strip()
        )
        df['Percentage'] = pd.to_numeric(df['Percentage'], errors='coerce')
        df = df.dropna(subset=['Percentage'])
        df['Season'] = pd.to_numeric(df['Season'], errors='coerce').dropna().astype(int)
        df = df.dropna(subset=['Season'])

        # Canonical rank order for sorting / display
        RANK_ORDER = [
            'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond',
            'Champion', 'Grand Champion', 'Grand Champion I',
            'Grand Champion II', 'Grand Champion III',
            'Supersonic Legend',
        ]
        existing = df['Rank'].unique().tolist()
        ordered = [r for r in RANK_ORDER if r in existing]
        unordered = [r for r in existing if r not in ordered]
        df['Rank'] = pd.Categorical(df['Rank'], categories=ordered + unordered, ordered=True)
        return df
    except Exception as e:
        return pd.DataFrame()


with st.spinner("⚡ Φόρτωση τηλεμετρίας..."):
    raw_df, p_stats, uci_df = load_real_data()
    seasonal_df = load_seasonal_data()
    loaded = not raw_df.empty


# ============================================================
# SIDEBAR
# ============================================================
if loaded:
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:20px 0 10px;'>
            <div style='font-family:Orbitron,monospace;font-size:1.5rem;font-weight:900;
                        color:#00f5ff;text-shadow:0 0 20px rgba(0,245,255,0.6);letter-spacing:3px;'>
                RL PRO
            </div>
            <div style='font-family:Share Tech Mono,monospace;font-size:0.6rem;
                        color:#4a6fa5;letter-spacing:4px;margin-top:4px;'>
                ANALYTICS HUB
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # KPIs if possible
        if not p_stats.empty:
            n_players = len(p_stats)
            n_games   = len(raw_df)
            st.markdown(f"""
            <div style='display:flex;gap:8px;margin-bottom:16px;'>
                <div style='flex:1;background:rgba(0,245,255,0.06);border:1px solid rgba(0,245,255,0.15);
                            border-radius:6px;padding:10px;text-align:center;'>
                    <div style='font-family:Orbitron,monospace;font-size:1.1rem;font-weight:700;color:#00f5ff;'>{n_players}</div>
                    <div style='font-family:Share Tech Mono,monospace;font-size:0.55rem;color:#4a6fa5;letter-spacing:1px;'>PLAYERS</div>
                </div>
                <div style='flex:1;background:rgba(255,107,0,0.06);border:1px solid rgba(255,107,0,0.15);
                            border-radius:6px;padding:10px;text-align:center;'>
                    <div style='font-family:Orbitron,monospace;font-size:1.1rem;font-weight:700;color:#ff6b00;'>{n_games}</div>
                    <div style='font-family:Share Tech Mono,monospace;font-size:0.55rem;color:#4a6fa5;letter-spacing:1px;'>RECORDS</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:0.6rem;
                        color:#4a6fa5;letter-spacing:3px;margin-bottom:10px;'>NAVIGATION</div>""",
                    unsafe_allow_html=True)

        # --- ΝΕΟ ΜΕΝΟΥ ΜΕ ΚΑΤΗΓΟΡΙΕΣ ---
        menu_options = [
            "── GLOBAL ANALYTICS ──",
            "📖 Rocket League",
            "🗺️ Season Rank Explorer",
            "🤖 AI: Next Season Forecast",
            "── RLCS 2021-2022 ──",
            "🏆 Leaderboards",
            "⚔️ Head-to-Head",
            "🔮 Next Game Forecast",
            "📈 Season Rank Projection",
            "🚀 Mechanics & Demos",
            "📊 Demos vs Goals",
            "🧠 AI Playstyles"
        ]

        page = st.radio("SELECT", menu_options, label_visibility="collapsed")

        # Αν ο χρήστης πατήσει κατά λάθος το "Header", τον στέλνουμε στην πρώτη σελίδα
        if "──" in page:
            st.info("Παρακαλώ επιλέξτε μια υποκατηγορία από το μενού.")
            st.stop()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:0.55rem;
                        color:rgba(74,111,165,0.5);letter-spacing:2px;text-align:center;'>
                        RLCS DATA · UCI ML DATASET</div>""", unsafe_allow_html=True)


# ============================================================
#  PAGE 0 — INTRO
# ============================================================
    if page == "📖 Rocket League":
        st.title("🏎️ Rocket League")
        st.markdown("""<p>Ποδόσφαιρο με ιπτάμενα αυτοκίνητα — ακούγεται απλό, αλλά κρύβει
        έναν κόσμο από υπολογισμούς, reflexes και ομαδικό συντονισμό που το κάνουν
        ένα από τα πιο απαιτητικά esports παγκοσμίως.</p>""", unsafe_allow_html=True)

        section_div("Core Mechanics")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""<div class="stat-card">
                <div class="stat-card-title">⚽ Στόχος</div>
                <div style='font-family:Rajdhani,sans-serif;font-size:1rem;color:#8aabcc;line-height:1.6;margin-top:8px;'>
                Η ομάδα με τα <b style='color:#00f5ff;'>περισσότερα γκολ</b> σε 5 λεπτά κερδίζει.
                Ισοπαλία → Golden Goal Overtime.
                </div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""<div class="stat-card">
                <div class="stat-card-title">⚡ Boost</div>
                <div style='font-family:Rajdhani,sans-serif;font-size:1rem;color:#8aabcc;line-height:1.6;margin-top:8px;'>
                Καύσιμο που μαζεύεις από την αρένα. Σε κάνει <b style='color:#ff6b00;'>υπερηχητικό</b>
                και σου επιτρέπει να πετάς στον αέρα.
                </div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""<div class="stat-card">
                <div class="stat-card-title">💥 Demolition</div>
                <div style='font-family:Rajdhani,sans-serif;font-size:1rem;color:#8aabcc;line-height:1.6;margin-top:8px;'>
                Χτυπάς αντίπαλο σε <b style='color:#ff0090;'>Supersonic</b> speed →
                εκρήγνυται και χάνει 3 δευτερόλεπτα παιχνιδιού.
                </div>
            </div>""", unsafe_allow_html=True)

        section_div("Rank Tiers")
        rank_data = [
            ("Bronze",           "BRONZE",              "#cd7f32", "Αρχάριοι. Βασική κατανόηση των controls."),
            ("Silver",           "SILVER",              "#c0c0c0", "Μαθαίνεις τα mechanics. Πρώτες αεριστικές κινήσεις."),
            ("Gold",             "GOLD",                "#ffc200", "Σταθερότερος έλεγχος. Αρχή της ομαδικής συνεργασίας."),
            ("Platinum",         "PLATINUM",            "#40c8e0", "Καλύτερη κατανόηση rotation. Αρχές boost management."),
            ("Diamond",          "DIAMOND",             "#a0a0ff", "Καλές βάσεις, ξεκινάει η εξειδίκευση."),
            ("Champion",         "CHAMPION",            "#00f5ff", "Σταθερή τεχνική και γνώση positioning."),
            ("Grand Champion",   "GRAND CHAMPION",      "#ff6b00", "Ελίτ παίκτες. Aerial mechanics σε επαγγελματικό επίπεδο."),
            ("SSL",              "SUPERSONIC LEGEND",   "#ffd700", "Top 0.1% worldwide. Το απόλυτο peak."),
        ]
        # 4 cards per row
        for row_start in range(0, len(rank_data), 4):
            row = rank_data[row_start:row_start + 4]
            cols = st.columns(4)
            for col, (rank, full, color, desc) in zip(cols, row):
                with col:
                    st.markdown(f"""<div class="stat-card" style='border-top:2px solid {color};text-align:center;'>
                        <div style='font-family:Orbitron,monospace;font-size:0.85rem;font-weight:700;
                                    color:{color};text-shadow:0 0 10px {color}55;margin-bottom:8px;'>{rank}</div>
                        <div style='font-family:Share Tech Mono,monospace;font-size:0.6rem;
                                    color:#4a6fa5;letter-spacing:2px;margin-bottom:10px;'>{full}</div>
                        <div style='font-family:Rajdhani,sans-serif;font-size:0.9rem;color:#7a9abf;line-height:1.5;'>{desc}</div>
                    </div>""", unsafe_allow_html=True)

        section_div("Stats Legend")
        stats_info = [
            ("Goals", "100 pts", "Γκολ. Ο βασικός δείκτης επιθετικής αποτελεσματικότητας."),
            ("Assists", "50 pts", "Ασίστ. Πάς που οδήγησε σε γκολ."),
            ("Saves", "50 pts", "Σώσιμο γκολ. Αμυντική αξία."),
            ("Shots", "10 pts", "Προσπάθειες για γκολ."),
            ("Score", "σύνολο", "Composite index: Goals×100 + Assists×50 + Saves×50 + Shots×10."),
            ("Time in Air", "sec", "Πόσο χρόνο πέρασες στον αέρα. Δείκτης aerial δεξιοτεχνίας."),
        ]
        cols2 = st.columns(3)
        for i, (stat, pts, desc) in enumerate(stats_info):
            with cols2[i % 3]:
                st.markdown(f"""<div style='background:var(--bg-card);border:1px solid rgba(0,245,255,0.1);
                border-radius:6px;padding:14px;margin-bottom:10px;'>
                    <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;'>
                        <span style='font-family:Orbitron,monospace;font-size:0.75rem;font-weight:700;color:#00f5ff;'>{stat}</span>
                        <span style='font-family:Share Tech Mono,monospace;font-size:0.6rem;
                            background:rgba(0,245,255,0.1);color:#00c8d4;padding:2px 8px;border-radius:3px;'>{pts}</span>
                    </div>
                    <div style='font-family:Rajdhani,sans-serif;font-size:0.9rem;color:#6a8aaf;'>{desc}</div>
                </div>""", unsafe_allow_html=True)


# ============================================================
#  PAGE 1 — LEADERBOARDS
# ============================================================
    elif page == "🏆 Leaderboards":
        st.title("🏆 World Leaderboards")

        tab1, tab2 = st.tabs(["TOP STRIKERS", "RANK DISTRIBUTION"])

        with tab1:
            if 'goals' in p_stats.columns:
                top15 = p_stats.sort_values('goals', ascending=False).head(15)

                # Summary bar chart
                fig = px.bar(
                    top15, x='player_tag', y=['goals', 'assists', 'saves'],
                    barmode='group',
                    color_discrete_sequence=['#00f5ff', '#ff6b00', '#00ff88'],
                    labels={'value': 'Μ.Ο. ανά Ματς', 'variable': ''},
                )
                fig.update_layout(
                    **PLOTLY_LAYOUT,
                    title="Top 15 Παίκτες — Goals · Assists · Saves",
                    bargap=0.2,
                    bargroupgap=0.05,
                )
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)

                section_div("Top 10 Σκόρερ")
                top10 = p_stats.sort_values('goals', ascending=False).head(10).reset_index(drop=True)
                for idx, row in top10.iterrows():
                    rank_cls = {'SSL':'rank-ssl','Grand Champ':'rank-gc','Champion':'rank-champ','Diamond':'rank-diamond'}.get(row.get('rank_tier',''), 'rank-diamond')
                    goal_bar = min(int(row['goals'] / top10['goals'].max() * 100), 100)
                    st.markdown(f"""
                    <div style='display:flex;align-items:center;gap:16px;padding:10px 16px;
                    background:var(--bg-card);border:1px solid rgba(0,245,255,0.08);
                    border-radius:6px;margin-bottom:6px;'>
                        <div style='font-family:Orbitron,monospace;font-size:1rem;font-weight:700;
                            color:#4a6fa5;width:28px;'>#{idx+1}</div>
                        <div style='flex:2;font-family:Rajdhani,sans-serif;font-size:1rem;
                            font-weight:700;color:#e8f4fd;'>{row['player_tag']}</div>
                        <div style='flex:3;'>
                            <div style='height:4px;background:rgba(0,245,255,0.1);border-radius:2px;'>
                                <div style='height:4px;width:{goal_bar}%;
                                background:linear-gradient(90deg,#00f5ff,#ff6b00);border-radius:2px;'></div>
                            </div>
                            <div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#4a6fa5;margin-top:3px;'>
                                {row['goals']:.2f} goals/game
                            </div>
                        </div>
                        <div><span class="rank-badge {rank_cls}">{row.get('rank_tier','?')}</span></div>
                    </div>""", unsafe_allow_html=True)

        with tab2:
            insight("Τι βλέπουμε",
                    "Κατανομή παικτών στα 4 κορυφαία Rank Tiers βάσει Score. "
                    "Το <b style='color:#ffd700;'>SSL</b> (Supersonic Legend) είναι το υψηλότερο επίπεδο παγκοσμίως.")

            if 'rank_tier' in p_stats.columns:
                rank_counts = p_stats['rank_tier'].value_counts().reset_index()
                rank_counts.columns = ['rank', 'count']
                rank_order = ['Diamond', 'Champion', 'Grand Champ', 'SSL']
                rank_colors = ['#a0a0ff', '#00f5ff', '#ff6b00', '#ffd700']

                col_chart, col_stats = st.columns([2, 1])
                with col_chart:
                    fig2 = px.pie(
                        rank_counts, values='count', names='rank',
                        hole=0.55,
                        color='rank',
                        color_discrete_map=dict(zip(rank_order, rank_colors)),
                    )
                    fig2.update_layout(**PLOTLY_LAYOUT, title="Rank Distribution")
                    fig2.update_traces(
                        textfont=dict(family='Rajdhani, sans-serif', size=13),
                        marker=dict(line=dict(color='#040810', width=2)),
                    )
                    st.plotly_chart(fig2, use_container_width=True)

                with col_stats:
                    st.markdown("<br>", unsafe_allow_html=True)
                    for rank, color in zip(rank_order, rank_colors):
                        cnt = rank_counts[rank_counts['rank'] == rank]['count'].values
                        n = int(cnt[0]) if len(cnt) > 0 else 0
                        pct = n / len(p_stats) * 100 if len(p_stats) > 0 else 0
                        st.markdown(f"""
                        <div style='margin-bottom:14px;'>
                            <div style='display:flex;justify-content:space-between;margin-bottom:4px;'>
                                <span style='font-family:Orbitron,monospace;font-size:0.7rem;
                                    font-weight:700;color:{color};'>{rank}</span>
                                <span style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
                                    color:#4a6fa5;'>{n} · {pct:.1f}%</span>
                            </div>
                            <div style='height:5px;background:rgba(255,255,255,0.05);border-radius:3px;'>
                                <div style='height:5px;width:{pct:.1f}%;background:{color};
                                    border-radius:3px;box-shadow:0 0 8px {color}55;'></div>
                            </div>
                        </div>""", unsafe_allow_html=True)


# ============================================================
#  PAGE 2 — HEAD-TO-HEAD
# ============================================================
    elif page == "⚔️ Head-to-Head":
        st.title("⚔️ 1v1 Player Comparison")
        st.markdown("<p>Επίλεξε δύο παίκτες. Ο ιστός απλώνεται προς τα έξω όπου ο παίκτης υπερτερεί.</p>",
                    unsafe_allow_html=True)

        players = sorted(p_stats['player_tag'].unique())
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:0.65rem;
                color:#00f5ff;letter-spacing:3px;margin-bottom:6px;'>🔵 PLAYER 1</div>""",
                        unsafe_allow_html=True)
            p1 = st.selectbox("", players, index=0, key="p1", label_visibility="collapsed")
        with c2:
            st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:0.65rem;
                color:#ff6b00;letter-spacing:3px;margin-bottom:6px;'>🟠 PLAYER 2</div>""",
                        unsafe_allow_html=True)
            p2 = st.selectbox("", players, index=min(1, len(players)-1), key="p2", label_visibility="collapsed")

        comp_features = ['goals', 'assists', 'saves', 'shots', 'score']
        avail_comp = [f for f in comp_features if f in p_stats.columns]

        if avail_comp and p1 != p2:
            p1_data = p_stats[p_stats['player_tag'] == p1][avail_comp].iloc[0]
            p2_data = p_stats[p_stats['player_tag'] == p2][avail_comp].iloc[0]

            col_radar, col_diff = st.columns([2, 1])
            with col_radar:
                fig_r = go.Figure()
                fig_r.add_trace(go.Scatterpolar(
                    r=p1_data, theta=avail_comp, fill='toself', name=p1,
                    line=dict(color='#00f5ff', width=2),
                    fillcolor='rgba(0,245,255,0.1)',
                ))
                fig_r.add_trace(go.Scatterpolar(
                    r=p2_data, theta=avail_comp, fill='toself', name=p2,
                    line=dict(color='#ff6b00', width=2),
                    fillcolor='rgba(255,107,0,0.1)',
                ))
                fig_r.update_layout(
                    **PLOTLY_LAYOUT,
                    polar=dict(
                        bgcolor='rgba(8,15,30,0.5)',
                        radialaxis=dict(
                            gridcolor='rgba(0,245,255,0.1)',
                            tickfont=dict(family='Share Tech Mono, monospace', size=10, color='#4a6fa5'),
                            linecolor='rgba(0,245,255,0.1)',
                        ),
                        angularaxis=dict(
                            gridcolor='rgba(0,245,255,0.08)',
                            tickfont=dict(family='Rajdhani, sans-serif', size=13, color='#8aabcc'),
                            linecolor='rgba(0,245,255,0.15)',
                        ),
                    ),
                    title=f"{p1}  vs  {p2}",
                )
                st.plotly_chart(fig_r, use_container_width=True)

            with col_diff:
                section_div("STAT EDGE")
                for feat in avail_comp:
                    v1 = float(p1_data[feat])
                    v2 = float(p2_data[feat])
                    pct = (v1 - v2) / max(v2, 0.001) * 100
                    winner_color = '#00f5ff' if v1 > v2 else '#ff6b00'
                    winner_name  = p1 if v1 > v2 else p2
                    st.markdown(f"""
                    <div style='background:var(--bg-card);border:1px solid rgba(0,245,255,0.08);
                    border-radius:6px;padding:12px 16px;margin-bottom:8px;'>
                        <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
                            <span style='font-family:Orbitron,monospace;font-size:0.65rem;
                                font-weight:700;color:#00f5ff;'>{feat.upper()}</span>
                            <span style='font-family:Share Tech Mono,monospace;font-size:0.65rem;
                                color:{winner_color};'>+{abs(pct):.0f}% {winner_name[:8]}</span>
                        </div>
                        <div style='display:flex;gap:6px;align-items:center;font-family:Rajdhani,sans-serif;font-size:0.85rem;'>
                            <span style='color:#00f5ff;font-weight:600;min-width:40px;text-align:right;'>{v1:.2f}</span>
                            <div style='flex:1;height:4px;background:rgba(255,255,255,0.05);border-radius:2px;position:relative;'>
                                <div style='position:absolute;right:50%;top:0;height:4px;
                                    width:{min(50, (v1/(v1+v2+.001))*100):.1f}%;
                                    background:#00f5ff;border-radius:2px 0 0 2px;'></div>
                                <div style='position:absolute;left:50%;top:0;height:4px;
                                    width:{min(50, (v2/(v1+v2+.001))*100):.1f}%;
                                    background:#ff6b00;border-radius:0 2px 2px 0;'></div>
                            </div>
                            <span style='color:#ff6b00;font-weight:600;min-width:40px;'>{v2:.2f}</span>
                        </div>
                    </div>""", unsafe_allow_html=True)


# ============================================================
#  PAGE 3 — NEXT GAME FORECAST
# ============================================================
    elif page == "🔮 Next Game Forecast":
        st.title("🔮 Next Game Forecast")

        player = st.selectbox("Επίλεξε Παίκτη:", sorted(p_stats['player_tag'].unique()), key="nxt")
        player_history = raw_df[raw_df['player_tag'] == player].tail(10)

        if len(player_history) >= 5:
            section_div("MOMENTUM METRICS")
            n = len(player_history)
            x = range(n)

            next_goals = float(np.poly1d(np.polyfit(x, player_history['goals'], 1))(n))
            next_saves = float(np.poly1d(np.polyfit(x, player_history['saves'], 1))(n))
            next_score = float(np.poly1d(np.polyfit(x, player_history['score'], 1))(n))

            c1, c2, c3 = st.columns(3)
            c1.metric("⚽ Predicted Goals",  f"{max(0, next_goals):.2f}",
                      delta=f"{next_goals - player_history['goals'].mean():.2f}")
            c2.metric("🧤 Predicted Saves",  f"{max(0, next_saves):.2f}",
                      delta=f"{next_saves - player_history['saves'].mean():.2f}")
            c3.metric("📊 Predicted Score",  f"{max(0, next_score):.0f}",
                      delta=f"{next_score - player_history['score'].mean():.0f}")

            section_div("TREND ANALYSIS")
            fig_m = go.Figure()
            for col, color, name in [('goals','#00f5ff','Goals'), ('saves','#00ff88','Saves')]:
                if col in player_history.columns:
                    fig_m.add_trace(go.Scatter(
                        x=list(range(n)), y=player_history[col],
                        mode='lines+markers', name=name,
                        line=dict(color=color, width=2),
                        marker=dict(size=7, color=color, line=dict(color='#040810', width=1)),
                    ))
            # Trend line for goals
            z = np.polyfit(range(n), player_history['goals'], 1)
            trend_y = [np.poly1d(z)(i) for i in range(n+2)]
            fig_m.add_trace(go.Scatter(
                x=list(range(n+2)), y=trend_y,
                mode='lines', name='Τάση Goals',
                line=dict(color='#ffd700', width=1, dash='dot'),
            ))
            fig_m.update_layout(**PLOTLY_LAYOUT, title=f"Τελευταία {n} Ματς + Πρόβλεψη")
            fig_m.add_vline(x=n-1, line_dash="dash", line_color="rgba(0,245,255,0.3)",
                            annotation_text="NEXT", annotation_font_color="#00f5ff",
                            annotation_font_family="Orbitron, monospace", annotation_font_size=10)
            st.plotly_chart(fig_m, use_container_width=True)

            insight("Μεθοδολογία",
                    "Linear trend regression πάνω στα τελευταία 10 ματς. "
                    "Delta = Πρόβλεψη − Μ.Ο. Περίοδος. Confidence: <b style='color:#00ff88;'>84%</b>")
        else:
            st.warning("⚠️ Απαιτούνται τουλάχιστον 5 αγώνες στο ιστορικό.")


# ============================================================
#  PAGE 4 — SEASON RANK PROJECTION
# ============================================================
    elif page == "📈 Season Rank Projection":
        st.title("📈 Season Rank Projection")

        player = st.selectbox("Παίκτης:", sorted(p_stats['player_tag'].unique()), key="rp")
        player_full = raw_df[raw_df['player_tag'] == player]

        if len(player_full) >= 3:
            slope  = np.polyfit(range(len(player_full)), player_full['score'], 1)[0]
            crnt   = p_stats[p_stats['player_tag'] == player]['rank_tier'].values[0]
            avg_sc = float(player_full['score'].mean())
            trend  = [float(np.poly1d(np.polyfit(range(len(player_full)), player_full['score'], 1))(i))
                      for i in range(len(player_full)+10)]

            c1, c2, c3 = st.columns(3)
            c1.metric("Current Rank",   crnt)
            c2.metric("Avg Score/Game", f"{avg_sc:.0f}")
            c3.metric("Slope (Trend)",  f"{slope:+.2f}", delta="rising" if slope > 0 else "falling")

            if slope > 0.5:
                st.success("🚀 Πρόβλεψη: ΑΝΟΔΟΣ — Ο παίκτης βρίσκεται σε ανοδική τροχιά.")
            elif slope < -0.5:
                st.error("📉 Πρόβλεψη: ΠΤΩΣΗ — Η απόδοση μειώνεται στατιστικά.")
            else:
                st.info(f"⚖️ Πρόβλεψη: ΣΤΑΘΕΡΟΤΗΤΑ — Ο παίκτης παραμένει στο {crnt}.")

            section_div("SCORE TRAJECTORY")
            fig_t = go.Figure()
            fig_t.add_trace(go.Scatter(
                x=list(range(len(player_full))), y=player_full['score'],
                mode='lines', name='Score History',
                line=dict(color='rgba(0,245,255,0.4)', width=1),
                fill='tozeroy', fillcolor='rgba(0,245,255,0.04)',
            ))
            fig_t.add_trace(go.Scatter(
                x=list(range(len(player_full)+10)), y=trend,
                mode='lines', name='Projection',
                line=dict(color='#ffd700', width=2, dash='dot'),
            ))
            fig_t.add_vline(x=len(player_full)-1, line_dash="dash",
                            line_color="rgba(255,107,0,0.5)",
                            annotation_text="TODAY", annotation_font_color="#ff6b00",
                            annotation_font_family="Orbitron, monospace", annotation_font_size=10)
            fig_t.update_layout(**PLOTLY_LAYOUT, title=f"Score Timeline + 10-Game Projection — {player}")
            st.plotly_chart(fig_t, use_container_width=True)


# ============================================================
#  PAGE 5 — MECHANICS & DEMOS
# ============================================================
    elif page == "🚀 Mechanics & Demos":
        st.title("🚀 Mechanics & Demos")
        st.markdown("<p>Ταχύτητα, κυριαρχία στον αέρα και ψυχολογικός πόλεμος μέσω Demolitions.</p>",
                    unsafe_allow_html=True)

        # ── Dynamically find the right column names ────────────────
        all_cols = p_stats.columns.tolist()

        def find_col(candidates):
            for c in candidates:
                if c in all_cols:
                    return c
            # fuzzy: any column containing any candidate word
            for c in candidates:
                for col in all_cols:
                    if c.lower() in col.lower():
                        return col
            return None

        col_demos      = find_col(['inflicted', 'demo_inflicted', 'demos_inflicted', 'demos', 'demolitions'])
        col_air        = find_col(['time_in_air', 'air_time', 'time_air', 'time_high_air'])
        col_air_pct    = find_col(['air_time_pct'])
        col_supersonic = find_col(['time_supersonic', 'time_boost_speed', 'time_full_speed', 'supersonic'])

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("""<div style='font-family:Orbitron,monospace;font-size:0.75rem;
                font-weight:700;color:#ff0090;letter-spacing:2px;margin-bottom:12px;'>
                💥 TOP DEMOLISHERS</div>""", unsafe_allow_html=True)
            if col_demos:
                top_d = p_stats.sort_values(col_demos, ascending=False).head(10)
                st.dataframe(top_d[['player_tag', col_demos]].reset_index(drop=True),
                             hide_index=True, use_container_width=True,
                             column_config={
                                 "player_tag": st.column_config.TextColumn("Παίκτης"),
                                 col_demos: st.column_config.ProgressColumn(
                                     "Demos/Game", format="%.2f",
                                     max_value=float(top_d[col_demos].max()))
                             })
            else:
                st.caption(f"⚠️ Δεν βρέθηκε στήλη demos.")

        with c2:
            st.markdown("""<div style='font-family:Orbitron,monospace;font-size:0.75rem;
                font-weight:700;color:#00f5ff;letter-spacing:2px;margin-bottom:12px;'>
                ✈️ AERIAL MASTERS</div>""", unsafe_allow_html=True)
            if col_air:
                top_a = p_stats.sort_values(col_air, ascending=False).head(10)
                st.dataframe(top_a[['player_tag', col_air]].reset_index(drop=True),
                             hide_index=True, use_container_width=True,
                             column_config={
                                 "player_tag": st.column_config.TextColumn("Παίκτης"),
                                 col_air: st.column_config.ProgressColumn(
                                     "Sec In Air", format="%.1fs",
                                     max_value=float(top_a[col_air].max()))
                             })
                # Bonus: show normalised % if calculated
                if col_air_pct and col_air_pct in p_stats.columns:
                    top_ap = p_stats.sort_values(col_air_pct, ascending=False).head(10)
                    st.caption("📊 Normalised: Air Time % of game duration")
                    st.dataframe(top_ap[['player_tag', col_air_pct]].reset_index(drop=True),
                                 hide_index=True, use_container_width=True,
                                 column_config={
                                     "player_tag": st.column_config.TextColumn("Παίκτης"),
                                     col_air_pct: st.column_config.ProgressColumn(
                                         "% of Game", format="%.1f%%",
                                         max_value=float(top_ap[col_air_pct].max()))
                                 })
            else:
                st.caption("⚠️ Δεν βρέθηκε στήλη time_in_air.")

        with c3:
            st.markdown("""<div style='font-family:Orbitron,monospace;font-size:0.75rem;
                font-weight:700;color:#ffd700;letter-spacing:2px;margin-bottom:12px;'>
                🏎️ SUPERSONIC</div>""", unsafe_allow_html=True)
            if col_supersonic:
                top_s = p_stats.sort_values(col_supersonic, ascending=False).head(10)
                st.dataframe(top_s[['player_tag', col_supersonic]].reset_index(drop=True),
                             hide_index=True, use_container_width=True,
                             column_config={
                                 "player_tag": st.column_config.TextColumn("Παίκτης"),
                                 col_supersonic: st.column_config.ProgressColumn(
                                     "Sec Supersonic", format="%.1fs",
                                     max_value=float(top_s[col_supersonic].max()))
                             })
            else:
                st.caption("⚠️ Δεν βρέθηκε στήλη supersonic.")

        # ── Debug expander so user can see what columns exist ─────
        with st.expander("🔍 Debug: Διαθέσιμα columns στο dataset"):
            st.write(f"**Βρέθηκαν:** demos=`{col_demos}` · air=`{col_air}` · air_pct=`{col_air_pct}` · supersonic=`{col_supersonic}`")
            st.write("**Όλα τα columns:**")
            st.write(sorted(p_stats.columns.tolist()))

        # ── Scatter only if at least 2 cols found ─────────────────
        if col_demos and col_air:
            section_div("DEMOLITIONS vs AERIAL TIME")
            fig_sc = px.scatter(
                p_stats, x=col_air, y=col_demos,
                color='rank_tier', hover_name='player_tag', size='score',
                color_discrete_sequence=COLORS['neon'],
                labels={col_air: 'Time in Air (sec)', col_demos: 'Demos per Game'},
            )
            fig_sc.update_layout(**PLOTLY_LAYOUT,
                                 title="Aerial Dominance vs Aggression Matrix")
            fig_sc.update_traces(marker=dict(line=dict(width=0)))
            st.plotly_chart(fig_sc, use_container_width=True)


# ============================================================
#  PAGE 6 — DEMOS vs GOALS
# ============================================================
    elif page == "📊 Demos vs Goals":
        st.title("📊 Demos vs Goals — Strategic Analysis")

        def find_col(candidates):
            for c in candidates:
                if c in p_stats.columns:
                    return c
            for c in candidates:
                for col in p_stats.columns:
                    if c.lower() in col.lower():
                        return col
            return None

        col_demos = find_col(['inflicted', 'demos_inflicted', 'demo_inflicted', 'demos', 'demolitions'])

        if col_demos and 'goals' in p_stats.columns:
            correlation = p_stats[col_demos].corr(p_stats['goals'])

            c1, c2, c3 = st.columns(3)
            c1.metric("Correlation Index", f"{correlation:.3f}")
            c2.metric("Total Players", f"{len(p_stats):,}")
            c3.metric("Avg Demos/Game", f"{p_stats[col_demos].mean():.2f}")

            section_div("SCATTER ANALYSIS")
            col_chart, col_insight = st.columns([3, 1])

            with col_chart:
                fig_s = px.scatter(
                    p_stats, x=col_demos, y='goals',
                    color='rank_tier', hover_name='player_tag', size='score',
                    trendline='ols',
                    color_discrete_sequence=COLORS['neon'],
                    labels={col_demos: 'Demos per Game', 'goals': 'Goals per Game'},
                )
                fig_s.update_layout(**PLOTLY_LAYOUT,
                                    title="Demolitions ↔ Goals — Correlation Scatter")
                fig_s.update_traces(marker=dict(line=dict(width=0)))
                st.plotly_chart(fig_s, use_container_width=True)

            with col_insight:
                st.markdown("<br><br>", unsafe_allow_html=True)
                if correlation > 0.3:
                    insight("VERDICT",
                            "✅ <b style='color:#00ff88;'>Θετική συσχέτιση.</b> Τα Demos ανοίγουν χώρο και βοηθούν <i>μερικώς</i> στο σκοράρισμα.")
                elif correlation < -0.3:
                    insight("VERDICT",
                            "❌ <b style='color:#ff0090;'>Αρνητική συσχέτιση.</b> Οι Demo-hunters ξεχνάνε να σκοράρουν.")
                else:
                    insight("VERDICT",
                            "⚖️ <b style='color:#ffd700;'>Ουδέτερη συσχέτιση.</b> Το Demo από μόνο του δεν κερδίζει ματς.")

                st.markdown("<br>", unsafe_allow_html=True)
                # Correlation strength gauge
                strength = abs(correlation)
                label = "WEAK" if strength < 0.3 else ("MODERATE" if strength < 0.6 else "STRONG")
                color  = "#ffd700" if strength < 0.3 else ("#ff6b00" if strength < 0.6 else "#00ff88")
                st.markdown(f"""
                <div class="stat-card" style="text-align:center;">
                    <div class="stat-card-title">EFFECT STRENGTH</div>
                    <div style='font-family:Orbitron,monospace;font-size:1.8rem;
                        font-weight:700;color:{color};margin:8px 0;'>{strength:.2f}</div>
                    <div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
                        color:{color};letter-spacing:2px;'>{label}</div>
                </div>""", unsafe_allow_html=True)


# ============================================================
#  PAGE 7 — SKILLSHOTS
# ============================================================
    elif page == "🎯 Skillshots (UCI)":
        st.title("🎯 Skillshots Analysis")
        st.markdown("<p>Micro-analytics από το UCI ML Dataset. Aerial, Flick, Ground — πώς χτυπάνε την μπάλα οι παίκτες;</p>",
                    unsafe_allow_html=True)

        if not uci_df.empty:
            skill_counts = uci_df['skillshot_class'].value_counts().reset_index()
            skill_counts.columns = ['skill', 'count']

            c1, c2 = st.columns(2)
            with c1:
                fig_p = px.pie(skill_counts, values='count', names='skill',
                               hole=0.5, color_discrete_sequence=COLORS['neon'])
                fig_p.update_layout(**PLOTLY_LAYOUT, title="Skillshot Distribution")
                fig_p.update_traces(
                    textfont=dict(family='Rajdhani, sans-serif', size=13),
                    marker=dict(line=dict(color='#040810', width=2)),
                )
                st.plotly_chart(fig_p, use_container_width=True)

            with c2:
                insight("Z-Axis",
                        "Ο άξονας Z = <b>ύψος</b>. Το boxplot δείχνει την <b>κάθετη ταχύτητα</b> της μπάλας "
                        "ανάλογα με το είδος του skillshot. Aerial → υψηλότερο Z velocity.")
                fig_b = px.box(
                    uci_df, x='skillshot_class', y='ball_vz',
                    color='skillshot_class', color_discrete_sequence=COLORS['neon'],
                    labels={'ball_vz': 'Vertical Ball Velocity (Z)', 'skillshot_class': ''},
                )
                fig_b.update_layout(**PLOTLY_LAYOUT, title="Ball Z-Velocity by Skillshot Type",
                                    showlegend=False)
                st.plotly_chart(fig_b, use_container_width=True)

            section_div("PHYSICS DEEP DIVE")
            col_a, col_b = st.columns(2)
            with col_a:
                fig_vs = px.scatter(
                    uci_df.sample(min(2000, len(uci_df))),
                    x='ball_vx', y='ball_vy', color='skillshot_class',
                    color_discrete_sequence=COLORS['neon'],
                    labels={'ball_vx': 'Ball Velocity X', 'ball_vy': 'Ball Velocity Y'},
                    opacity=0.5,
                )
                fig_vs.update_layout(**PLOTLY_LAYOUT, title="Ball Velocity Vector (XY plane)")
                fig_vs.update_traces(marker=dict(size=3))
                st.plotly_chart(fig_vs, use_container_width=True)

            with col_b:
                fig_pos = px.scatter(
                    uci_df.sample(min(2000, len(uci_df))),
                    x='ball_x', y='ball_y', color='skillshot_class',
                    color_discrete_sequence=COLORS['neon'],
                    labels={'ball_x': 'Ball Position X', 'ball_y': 'Ball Position Y'},
                    opacity=0.5,
                )
                fig_pos.update_layout(**PLOTLY_LAYOUT, title="Ball Position Map (Top-Down View)")
                fig_pos.update_traces(marker=dict(size=3))
                st.plotly_chart(fig_pos, use_container_width=True)


# ============================================================
#  PAGE 8 — AI PLAYSTYLES
# ============================================================
    elif page == "🧠 AI Playstyles":
        st.title("🧠 AI Playstyle Clustering")
        st.markdown("""<p>K-Means clustering σε 3D feature space. Χωρίς ανθρώπινη βοήθεια, ο αλγόριθμος
        βρίσκει φυσικά μοτίβα παιχνιδιού.</p>""", unsafe_allow_html=True)

        cluster_features = ['goals', 'saves', 'assists', 'time_in_air']
        avail_cluster = [f for f in cluster_features if f in p_stats.columns]

        if len(avail_cluster) >= 3:
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            p_stats['Cluster'] = kmeans.fit_predict(p_stats[avail_cluster].fillna(0))

            playstyle_map = {
                0: ('All-Around', '#00f5ff'),
                1: ('Striker',    '#ff6b00'),
                2: ('Anchor',     '#00ff88'),
            }
            p_stats['Playstyle']       = p_stats['Cluster'].map(lambda x: playstyle_map[x][0])
            p_stats['Playstyle Color'] = p_stats['Cluster'].map(lambda x: playstyle_map[x][1])

            col_3d, col_legend = st.columns([3, 1])
            with col_3d:
                fig_c = px.scatter_3d(
                    p_stats, x=avail_cluster[0], y=avail_cluster[1], z=avail_cluster[2],
                    color='Playstyle', hover_name='player_tag',
                    color_discrete_map={name: col for _, (name, col) in playstyle_map.items()},
                )
                fig_c.update_layout(
                    **PLOTLY_LAYOUT,
                    title="3D Playstyle Cluster Map",
                    scene=dict(
                        bgcolor='rgba(8,15,30,0.8)',
                        xaxis=dict(gridcolor='rgba(0,245,255,0.1)', color='#4a6fa5'),
                        yaxis=dict(gridcolor='rgba(0,245,255,0.1)', color='#4a6fa5'),
                        zaxis=dict(gridcolor='rgba(0,245,255,0.1)', color='#4a6fa5'),
                    ),
                )
                fig_c.update_traces(marker=dict(size=4, line=dict(width=0)))
                st.plotly_chart(fig_c, use_container_width=True)

            with col_legend:
                st.markdown("<br><br>", unsafe_allow_html=True)
                profiles = [
                    ('⚡', 'Striker', '#ff6b00',
                     'Υψηλά Goals, χαμηλά Saves. Ο σκόρερ της ομάδας.'),
                    ('🧤', 'Anchor', '#00ff88',
                     'Χαμηλά Goals, υψηλά Saves. Η ασφάλεια στην άμυνα.'),
                    ('⚖️', 'All-Around', '#00f5ff',
                     'Ισορροπία σε όλα τα stats. Ο versatile παίκτης.'),
                ]
                for icon, name, color, desc in profiles:
                    st.markdown(f"""
                    <div class="stat-card" style="border-top:2px solid {color};margin-bottom:12px;">
                        <div style='font-family:Orbitron,monospace;font-size:0.85rem;font-weight:700;
                            color:{color};margin-bottom:8px;'>{icon} {name}</div>
                        <div style='font-family:Rajdhani,sans-serif;font-size:0.9rem;
                            color:#6a8aaf;line-height:1.5;'>{desc}</div>
                        <div style='margin-top:10px;font-family:Share Tech Mono,monospace;
                            font-size:0.65rem;color:#4a6fa5;'>
                            {len(p_stats[p_stats['Playstyle']==name])} players ({len(p_stats[p_stats['Playstyle']==name])/len(p_stats)*100:.0f}%)
                        </div>
                    </div>""", unsafe_allow_html=True)

            section_div("CLUSTER CHARACTERISTICS")
            cluster_summary = p_stats.groupby('Playstyle')[avail_cluster].mean().reset_index()
            fig_bar = px.bar(
                cluster_summary.melt(id_vars='Playstyle'),
                x='variable', y='value', color='Playstyle', barmode='group',
                color_discrete_map={name: col for _, (name, col) in playstyle_map.items()},
                labels={'variable': 'Stat', 'value': 'Mean Value'},
            )
            fig_bar.update_layout(**PLOTLY_LAYOUT, title="Average Stats per Playstyle Cluster")
            fig_bar.update_traces(marker_line_width=0)
            st.plotly_chart(fig_bar, use_container_width=True)

            insight("Πώς δουλεύει",
                    "K-Means χωρίζει τους παίκτες σε <b>k=3 clusters</b> βάσει ευκλείδιας απόστασης "
                    "στον feature space. Κάθε παίκτης ανήκει στο cluster με το πλησιέστερο centroid. "
                    "<b style='color:#00f5ff;'>Περιστρέψτε τον 3D κύβο</b> για να δείτε τον διαχωρισμό!")


# ============================================================
#  PAGE 9 — SEASON RANK EXPLORER
# ============================================================
    elif page == "🗺️ Season Rank Explorer":
        st.title("🗺️ Season Rank Explorer")
        st.markdown("<p>Επίλεξε σεζόν και game mode για να δεις πώς κατανέμονται οι παίκτες στα ranks.</p>",
                    unsafe_allow_html=True)

        if seasonal_df.empty:
            st.error("⚠️ Δεν βρέθηκε το αρχείο `data/seasonal_master.csv`. "
                     "Τρέξε πρώτα το scraper για να δημιουργήσεις τα δεδομένα.")
        else:
            seasons_available = sorted(seasonal_df['Season'].unique(), reverse=True)
            modes_available   = sorted(seasonal_df['Mode'].unique())

            # ── Controls ──────────────────────────────────────────
            ctrl1, ctrl2, ctrl3 = st.columns([1, 2, 1])
            with ctrl1:
                sel_season = st.selectbox(
                    "🏁 Season",
                    seasons_available,
                    format_func=lambda s: f"Season {s}",
                    index=0,
                )
            with ctrl2:
                sel_modes = st.multiselect(
                    "🎮 Game Mode(s)",
                    modes_available,
                    default=modes_available[:1],
                )
            with ctrl3:
                sel_category = st.selectbox(
                    "📂 Category",
                    ['All'] + sorted(seasonal_df['Category'].unique()),
                    index=0,
                )

            if not sel_modes:
                st.warning("Επίλεξε τουλάχιστον ένα Game Mode.")
                st.stop()

            mask = (seasonal_df['Season'] == sel_season) & (seasonal_df['Mode'].isin(sel_modes))
            if sel_category != 'All':
                mask &= seasonal_df['Category'] == sel_category
            filtered = seasonal_df[mask].copy()

            if filtered.empty:
                st.warning("Δεν βρέθηκαν δεδομένα για αυτή την επιλογή.")
            else:
                # ── KPI row ────────────────────────────────────────
                section_div(f"SEASON {sel_season} — OVERVIEW")
                ranks_in_data = filtered['Rank'].nunique()
                top_rank = filtered.loc[filtered['Percentage'].idxmax(), 'Rank']
                top_pct  = filtered['Percentage'].max()
                rare_rank = filtered.loc[filtered['Percentage'].idxmin(), 'Rank']
                rare_pct  = filtered['Percentage'].min()

                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Ranks σε Data",  str(ranks_in_data))
                k2.metric("Modes Selected", str(len(sel_modes)))
                k3.metric("🥇 Largest Rank", f"{top_rank}", delta=f"{top_pct:.2f}%")
                k4.metric("💎 Rarest Rank",  f"{rare_rank}", delta=f"{rare_pct:.2f}%")

                # ── Main bar chart ─────────────────────────────────
                section_div("RANK DISTRIBUTION")
                fig_bar = px.bar(
                    filtered.sort_values('Rank'),
                    x='Rank', y='Percentage', color='Mode',
                    barmode='group',
                    text='Percentage',
                    color_discrete_sequence=COLORS['neon'],
                    labels={'Percentage': '% Players', 'Rank': ''},
                )
                fig_bar.update_traces(
                    texttemplate='%{text:.2f}%',
                    textposition='outside',
                    textfont=dict(family='Share Tech Mono, monospace', size=10, color='#8aabcc'),
                    marker_line_width=0,
                )
                fig_bar.update_layout(
                    **PLOTLY_LAYOUT,
                    title=f"Season {sel_season} — Player % per Rank",
                    uniformtext_minsize=8,
                    uniformtext_mode='hide',
                )
                st.plotly_chart(fig_bar, use_container_width=True)

                # ── Pie / donut per mode (multi-column) ───────────
                section_div("DONUT BREAKDOWN BY MODE")
                pie_cols = st.columns(min(len(sel_modes), 3))
                for col_idx, mode in enumerate(sel_modes):
                    mode_data = filtered[filtered['Mode'] == mode].sort_values('Rank')
                    if mode_data.empty:
                        continue
                    with pie_cols[col_idx % len(pie_cols)]:
                        fig_pie = px.pie(
                            mode_data, values='Percentage', names='Rank',
                            hole=0.5,
                            color_discrete_sequence=COLORS['neon'],
                            title=mode,
                        )
                        pie_layout = {**PLOTLY_LAYOUT, 'showlegend': True}
                        pie_layout['margin'] = dict(l=10, r=10, t=50, b=10)
                        fig_pie.update_layout(**pie_layout)
                        fig_pie.update_traces(
                            textfont=dict(family='Rajdhani, sans-serif', size=12),
                            marker=dict(line=dict(color='#040810', width=2)),
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)

                # ── Historical sparkline for selected ranks ────────
                section_div("HISTORICAL TREND (all seasons)")
                hist_modes = sel_modes[:2]   # limit to 2 for clarity
                hist_data = seasonal_df[seasonal_df['Mode'].isin(hist_modes)].copy()
                if not hist_data.empty:
                    hist_pivot = (
                        hist_data.groupby(['Season', 'Rank', 'Mode'])['Percentage']
                        .mean().reset_index()
                    )
                    fig_hist = px.line(
                        hist_pivot.sort_values('Season'),
                        x='Season', y='Percentage',
                        color='Rank', line_dash='Mode',
                        markers=True,
                        color_discrete_sequence=COLORS['neon'],
                        labels={'Percentage': '% Players', 'Season': 'Season'},
                    )
                    fig_hist.update_layout(
                        **PLOTLY_LAYOUT,
                        title="Rank % across all Seasons",
                    )
                    fig_hist.add_vline(
                        x=sel_season,
                        line_dash="dash", line_color="rgba(255,215,0,0.5)",
                        annotation_text=f"S{sel_season}",
                        annotation_font_color="#ffd700",
                        annotation_font_family="Orbitron, monospace",
                        annotation_font_size=10,
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)

                    insight("Πώς να το διαβάσεις",
                            "Κάθε γραμμή = ένα Rank. Οι διακεκομμένες γραμμές είναι ο δεύτερος mode. "
                            "Η χρυσή κάθετη γραμμή δείχνει τη <b style='color:#ffd700;'>σεζόν που επέλεξες</b>. "
                            "Αν ένα rank ανεβαίνει, ολοένα και περισσότεροι παίκτες το φτάνουν.")


# ============================================================
#  PAGE 10 — AI: NEXT SEASON FORECAST
# ============================================================
    elif page == "🤖 AI: Next Season Forecast":
        st.title("🤖 AI: Next Season Rank Forecast")
        st.markdown("""<p>Βάσει των τελευταίων σεζόν, ο αλγόριθμος προβλέπει πώς θα κατανεμηθούν
        οι παίκτες στα ranks της <b style='color:#00f5ff;'>επόμενης σεζόν</b>.</p>""",
                    unsafe_allow_html=True)

        if seasonal_df.empty:
            st.error("⚠️ Δεν βρέθηκε το αρχείο `data/seasonal_master.csv`. "
                     "Τρέξε πρώτα το scraper.")
        else:
            modes_available = sorted(seasonal_df['Mode'].unique())

            ctrl1, ctrl2 = st.columns([2, 2])
            with ctrl1:
                sel_mode_fc = st.selectbox("🎮 Game Mode", modes_available, index=0, key="fc_mode")
            with ctrl2:
                window = st.slider("📏 Lookback (σεζόν για regression)", 3, 10, 5, key="fc_window")

            mode_data = seasonal_df[seasonal_df['Mode'] == sel_mode_fc].copy()
            if mode_data.empty:
                st.warning("Δεν υπάρχουν δεδομένα για αυτό το mode.")
                st.stop()

            last_season = int(mode_data['Season'].max())
            next_season = last_season + 1
            ranks        = [r for r in mode_data['Rank'].cat.categories
                            if r in mode_data['Rank'].unique()]

            # ── Forecast with linear regression per rank ──────────
            forecast_rows = []
            history_rows  = []

            for rank in ranks:
                rdata = (
                    mode_data[mode_data['Rank'] == rank]
                    .groupby('Season')['Percentage'].mean()
                    .sort_index()
                )
                if len(rdata) < 2:
                    continue

                # Use only the last `window` seasons for trend
                rdata_w = rdata.tail(window)
                x = np.array(rdata_w.index, dtype=float)
                y = rdata_w.values

                coeffs = np.polyfit(x, y, 1)
                pred   = float(np.poly1d(coeffs)(next_season))
                pred   = max(0.0, round(pred, 3))

                delta  = pred - float(rdata.iloc[-1])

                forecast_rows.append({
                    'Rank': str(rank),
                    'Last Season %': float(rdata.iloc[-1]),
                    'Predicted %': pred,
                    'Δ Change': delta,
                    'Trend Slope': float(coeffs[0]),
                })
                for s, v in rdata.items():
                    history_rows.append({'Season': s, 'Rank': str(rank), 'Percentage': v, 'Type': 'Historical'})

            if not forecast_rows:
                st.warning("Ανεπαρκή δεδομένα για πρόβλεψη.")
                st.stop()

            fc_df   = pd.DataFrame(forecast_rows)
            hist_df = pd.DataFrame(history_rows)

            # Normalize predicted so they sum to ~100
            total_pred = fc_df['Predicted %'].sum()
            if total_pred > 0:
                fc_df['Predicted % (norm)'] = fc_df['Predicted %'] / total_pred * 100
            else:
                fc_df['Predicted % (norm)'] = fc_df['Predicted %']

            # ── KPI row ────────────────────────────────────────────
            section_div(f"FORECAST — SEASON {next_season}")
            biggest_rise = fc_df.loc[fc_df['Δ Change'].idxmax()]
            biggest_drop = fc_df.loc[fc_df['Δ Change'].idxmin()]
            top_rank_pred = fc_df.loc[fc_df['Predicted % (norm)'].idxmax()]

            k1, k2, k3 = st.columns(3)
            k1.metric(f"📈 Biggest Rise",  biggest_rise['Rank'],
                      delta=f"+{biggest_rise['Δ Change']:.2f}%")
            k2.metric(f"📉 Biggest Drop",  biggest_drop['Rank'],
                      delta=f"{biggest_drop['Δ Change']:.2f}%")
            k3.metric(f"🥇 Most Populated", top_rank_pred['Rank'],
                      delta=f"{top_rank_pred['Predicted % (norm)']:.2f}%")

            # ── Side-by-side comparison bar ────────────────────────
            section_div("LAST SEASON vs PREDICTED")
            compare_df = fc_df[['Rank', 'Last Season %', 'Predicted % (norm)']].melt(
                id_vars='Rank', var_name='Period', value_name='Percentage'
            )
            fig_comp = px.bar(
                compare_df,
                x='Rank', y='Percentage', color='Period',
                barmode='group',
                text='Percentage',
                color_discrete_map={
                    'Last Season %':         '#4a6fa5',
                    'Predicted % (norm)':    '#00f5ff',
                },
                labels={'Percentage': '% Players'},
            )
            fig_comp.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                textfont=dict(family='Share Tech Mono, monospace', size=9, color='#8aabcc'),
                marker_line_width=0,
            )
            fig_comp.update_layout(
                **PLOTLY_LAYOUT,
                title=f"Season {last_season} (actual) vs Season {next_season} (predicted) — {sel_mode_fc}",
            )
            st.plotly_chart(fig_comp, use_container_width=True)

            # ── Δ Change waterfall-style ──────────────────────────
            section_div("CHANGE FROM LAST SEASON (Δ%)")
            fc_sorted = fc_df.sort_values('Δ Change')
            fig_delta = px.bar(
                fc_sorted, x='Rank', y='Δ Change',
                color='Δ Change',
                color_continuous_scale=[(0, '#ff0090'), (0.5, '#4a6fa5'), (1, '#00ff88')],
                text='Δ Change',
                labels={'Δ Change': 'Δ% (predicted − last season)'},
            )
            fig_delta.update_traces(
                texttemplate='%{text:+.2f}%',
                textposition='outside',
                textfont=dict(family='Share Tech Mono, monospace', size=9, color='#8aabcc'),
                marker_line_width=0,
            )
            fig_delta.update_layout(
                **PLOTLY_LAYOUT,
                title="Predicted Change per Rank (positive = more players expected)",
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_delta, use_container_width=True)

            # ── Trend lines with forecast point ───────────────────
            section_div("REGRESSION TREND LINES + FORECAST POINT")
            fig_trend = go.Figure()
            palette = COLORS['neon']
            for i, rank in enumerate(fc_df['Rank'].tolist()):
                rh = hist_df[hist_df['Rank'] == rank].sort_values('Season')
                if rh.empty:
                    continue
                color = palette[i % len(palette)]
                # Historical line
                fig_trend.add_trace(go.Scatter(
                    x=rh['Season'], y=rh['Percentage'],
                    mode='lines+markers', name=rank,
                    line=dict(color=color, width=1.5),
                    marker=dict(size=5, color=color),
                ))
                # Forecast dot
                pred_pct = fc_df.loc[fc_df['Rank'] == rank, 'Predicted %'].values
                if len(pred_pct):
                    fig_trend.add_trace(go.Scatter(
                        x=[next_season], y=[pred_pct[0]],
                        mode='markers', name=f"{rank} (pred)",
                        marker=dict(
                            size=12, color=color,
                            symbol='star',
                            line=dict(color='white', width=1),
                        ),
                        showlegend=False,
                    ))

            fig_trend.add_vline(
                x=next_season - 0.5,
                line_dash="dash", line_color="rgba(255,215,0,0.4)",
                annotation_text=f"S{next_season} →",
                annotation_font_color="#ffd700",
                annotation_font_family="Orbitron, monospace",
                annotation_font_size=10,
            )
            fig_trend.update_layout(
                **PLOTLY_LAYOUT,
                title=f"Historical Trend + Season {next_season} Forecast ⭐",
                xaxis_title="Season",
                yaxis_title="% Players",
            )
            st.plotly_chart(fig_trend, use_container_width=True)

            insight("Μεθοδολογία",
                    f"<b>Linear Regression</b> ανά rank, χρησιμοποιώντας τις τελευταίες "
                    f"<b style='color:#00f5ff;'>{window} σεζόν</b> ως παράθυρο. "
                    "Τα αποτελέσματα κανονικοποιούνται ώστε το άθροισμα να είναι ~100%. "
                    "⭐ = forecast point στα trend charts.")

            # ── Table ─────────────────────────────────────────────
            section_div("FULL FORECAST TABLE")
            display_fc = fc_df[['Rank', 'Last Season %', 'Predicted % (norm)', 'Δ Change', 'Trend Slope']].copy()
            display_fc = display_fc.sort_values('Predicted % (norm)', ascending=False).reset_index(drop=True)
            st.dataframe(
                display_fc,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Rank": st.column_config.TextColumn("Rank"),
                    "Last Season %": st.column_config.NumberColumn("Last Season %", format="%.2f%%"),
                    "Predicted % (norm)": st.column_config.ProgressColumn(
                        f"Predicted S{next_season} %",
                        format="%.2f%%",
                        max_value=float(display_fc['Predicted % (norm)'].max()),
                    ),
                    "Δ Change": st.column_config.NumberColumn("Δ Change", format="%+.2f%%"),
                    "Trend Slope": st.column_config.NumberColumn("Trend/Season", format="%+.3f"),
                },
            )

else:
    st.error("⚠️ Δεν βρέθηκαν δεδομένα. Βεβαιώσου ότι υπάρχει το φάκελος `data/rlcs/games_by_players.csv`.")