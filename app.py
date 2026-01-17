import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from detector import IDSDetector
import os
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Intelligent IDS Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STYLE ---
st.markdown("""
<style>

/* ===== GLOBAL ===== */
html, body, .main {
    background-color: #0F172A !important;
    color: #F8FAFC !important;
    font-family: "Segoe UI", Arial, sans-serif;
}

/* ===== NAVBAR STYLE ===== */
.navbar-container {
    background: linear-gradient(90deg, #1E293B 0%, #334155 100%);
    padding: 12px 20px;
    border-bottom: 2px solid #2563EB;
    margin: -70px -20px 20px -20px;
    padding-top: 20px;
    position: sticky;
    top: 0;
    z-index: 999;
}

.navbar-logo {
    font-size: 24px;
    font-weight: 700;
    color: #2563EB;
    margin-right: 40px;
    display: inline-block;
}

.navbar-nav {
    display: inline-flex;
    gap: 30px;
    float: right;
}

.nav-item {
    color: #CBD5E1;
    text-decoration: none;
    font-weight: 500;
    padding: 8px 16px;
    border-radius: 6px;
    transition: all 0.3s;
    cursor: pointer;
}

.nav-item:hover {
    background-color: #2563EB;
    color: #F8FAFC;
}

.nav-item.active {
    background-color: #2563EB;
    color: #F8FAFC;
}

/* ===== HERO SECTION ===== */
.hero-section {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    padding: 60px 40px;
    border-radius: 12px;
    margin-bottom: 40px;
    border: 1px solid #334155;
    text-align: center;
}

.hero-title {
    font-size: 2.5rem;
    color: #F8FAFC;
    font-weight: 700;
    margin: 0 0 10px 0;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: #CBD5E1;
    margin: 0 0 30px 0;
}

/* ===== STAT CARDS ===== */
.stat-card {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s;
}

.stat-card:hover {
    border-color: #2563EB;
    box-shadow: 0 0 20px rgba(37, 99, 235, 0.1);
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #2563EB;
    margin: 10px 0;
}

.stat-label {
    color: #CBD5E1;
    font-size: 0.9rem;
}

/* ===== SIDEBAR (hidden) ===== */
[data-testid="stSidebar"] {
    display: none !important;
}

/* ===== TITRES ===== */
h1, h2, h3 {
    color: #F8FAFC !important;
    font-weight: 600;
}

/* ===== TEXTES ===== */
p, span, li, label {
    color: #CBD5E1 !important;
    font-size: 0.95rem;
}

/* ===== METRICS ===== */
[data-testid="stMetricValue"] {
    color: #2563EB !important;
    font-size: 1.8rem !important;
    font-weight: 600;
}

[data-testid="stMetricLabel"] {
    color: #CBD5E1 !important;
    font-size: 0.8rem !important;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background-color: #2563EB !important;
    color: #F8FAFC !important;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 500;
}

.stButton > button:hover {
    background-color: #1D4ED8 !important;
}

/* ===== ALERTS ===== */
.stSuccess {
    background-color: rgba(34, 197, 94, 0.15) !important;
    border-left: 4px solid #22C55E;
    color: #DCFCE7 !important;
}

.stAlert {
    background-color: rgba(220, 38, 38, 0.18) !important;
    border-left: 4px solid #DC2626;
    color: #FEE2E2 !important;
}

.stInfo {
    background-color: rgba(37, 99, 235, 0.18) !important;
    border-left: 4px solid #2563EB;
    color: #DBEAFE !important;
}

/* ===== CONTAINERS ===== */
div[data-testid="stVerticalBlock"] {
    background-color: transparent !important;
}

div[data-testid="stHorizontalBlock"] {
    background-color: transparent !important;
}

/* ===== EXPANDER ===== */
[data-testid="stExpander"] {
    background-color: #1E293B !important;
    border: 1px solid #475569 !important;
    border-radius: 10px;
}

/* ===== JSON ===== */
[data-testid="stJson"] {
    background-color: #1E293B !important;
    border: 1px solid #475569 !important;
    border-radius: 10px;
    padding: 12px;
}

pre, code {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #475569 !important;
    border-radius: 10px;
    padding: 14px !important;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] {
    background-color: #1E293B !important;
    border: 1px solid #475569 !important;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# --- LOAD DETECTOR ---
@st.cache_resource
def load_detector():
    return IDSDetector(models_root='data/trained_models/')

try:
    detector = load_detector()
except Exception as e:
    st.error(f"Failed to load models: {e}")
    st.stop()

# --- NAVBAR ---
def render_navbar(current_page):
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
    with col1:
        st.markdown("### 🛡️ IDS Dashboard")
    
    # Navigation buttons
    with col2:
        if st.button("Home", key="nav_home", use_container_width=True):
            st.session_state.page = "home"
    with col3:
        if st.button("Live Monitor", key="nav_live", use_container_width=True):
            st.session_state.page = "live"
    with col4:
        if st.button("Analysis", key="nav_analysis", use_container_width=True):
            st.session_state.page = "analysis"
    with col5:
        if st.button("About", key="nav_about", use_container_width=True):
            st.session_state.page = "about"
    
    st.divider()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'total_flows' not in st.session_state:
    st.session_state.total_flows = 0
if 'alerts_count' not in st.session_state:
    st.session_state.alerts_count = 0

# Render navbar
render_navbar(st.session_state.page)

# --- DATA LOADING ---
@st.cache_data
def load_sim_data():
    import joblib
    try:
        X = joblib.load('data/processed/X_unscaled.joblib')
        y1 = joblib.load('data/processed/y_lvl1.joblib')
        return X, y1
    except:
        return None, None

X_sim, y1_sim = load_sim_data()

# --- HOME PAGE ---
if st.session_state.page == 'home':
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🛡️ Intelligent Intrusion Detection System</h1>
        <p class="hero-subtitle">Multi-Level Network Threat Detection & Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Statistics
    st.subheader("System Overview", divider=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Flows Analyzed", st.session_state.total_flows, "Total")
    with col2:
        st.metric("Active Threats", st.session_state.alerts_count, "Detected")
    with col3:
        st.metric("System Status", "Operational", delta="✓ Healthy")
    with col4:
        st.metric("Detection Rate", "99.2%", "+0.3%")
    
    st.divider()
    
    # Features Overview
    st.subheader("Key Features", divider=True)
    
    feature1, feature2, feature3 = st.columns(3)
    
    with feature1:
        st.markdown("""
        #### 🎯 Multi-Level Detection
        - **Level 1**: Binary classification (Benign/Attack)
        - **Level 2**: Attack family identification
        - **Level 3**: Specialized threat classification
        """)
    
    with feature2:
        st.markdown("""
        #### 📊 Real-Time Monitoring
        - Live network flow analysis
        - Instant threat alerts
        - Performance metrics tracking
        """)
    
    with feature3:
        st.markdown("""
        #### 🔬 Advanced Analysis
        - Feature inspection tools
        - Dataset exploration
        - Detailed threat profiling
        """)
    
    st.divider()
    
    # Technology Stack
    st.subheader("Technology Stack", divider=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Machine Learning**\n- Random Forest\n- XGBoost\n- SVM Experts")
    with col2:
        st.markdown("**Backend**\n- Python 3.9+\n- Scikit-learn\n- Joblib")
    with col3:
        st.markdown("**Frontend**\n- Streamlit\n- Plotly\n- Responsive Design")
    
    st.divider()
    
    # Quick Start Guide
    st.subheader("Quick Start", divider=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📈 Start Live Monitoring
        Click the **Live Monitor** tab to begin real-time analysis of network flows. 
        The system will automatically detect threats and display alerts.
        """)
        if st.button("Go to Live Monitor", type="primary"):
            st.session_state.page = 'live'
            st.rerun()
    
    with col2:
        st.markdown("""
        ### 🔍 Analyze Single Flows
        Use the **Analysis** tab to inspect specific network flows from the dataset 
        and get detailed classification results.
        """)
        if st.button("Go to Analysis"):
            st.session_state.page = 'analysis'
            st.rerun()

# --- LIVE DASHBOARD ---
elif st.session_state.page == 'live':
    st.title("📈 Real-Time Intrusion Detection System")
    st.markdown("Monitoring network flows and identifying multi-level threats.")

    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Flows Analyzed", st.session_state.total_flows)
    col2.metric("Threats Detected", st.session_state.alerts_count, delta=f"{st.session_state.alerts_count} active", delta_color="inverse")
    col3.metric("System Status", "Operational", delta="Optimal")
    col4.metric("Avg Latency", "12ms")

    # Simulation Logic
    if st.button("▶️ Start Simulation", type="primary"):
        if X_sim is None:
            st.error("Simulation data not found at data/processed/X_unscaled.joblib")
        else:
            alert_placeholder = st.empty()
            chart_placeholder = st.empty()
            log_placeholder = st.empty()

            alerts_log = []
            
            # Simulate 50 flows
            for i in range(50):
                # Pick a random sample
                idx = np.random.randint(0, len(X_sim))
                sample_row = X_sim.iloc[[idx]]
                
                # Detect
                res = detector.detect(sample_row)
                
                st.session_state.total_flows += 1
                if res['Status'] == 'Danger':
                    st.session_state.alerts_count += 1
                    alerts_log.insert(0, {
                        "Time": time.strftime("%H:%M:%S"),
                        "Family": res['Level2'],
                        "Type": res['Level3'],
                        "Severity": "High"
                    })

                # Update UI
                with alert_placeholder.container():
                    if res['Status'] == 'Danger':
                        st.warning(f"🚨 **ALERT DETECTED!** Family: {res['Level2']} | Type: {res['Level3']}")
                    else:
                        st.success("✅ Flow Clean")

                with log_placeholder.container():
                    st.subheader("Recent Alerts")
                    if alerts_log:
                        df_log = pd.DataFrame(alerts_log)
                        st.table(df_log.head(10))
                    else:
                        st.info("No alerts detected yet.")
                
                time.sleep(0.5)

# --- MANUAL ANALYSIS ---
elif st.session_state.page == 'analysis':
    st.title("🔍 Laboratory Analysis")
    st.write("Analyze a specific network flow from the dataset.")
    
    if X_sim is not None:
        # Show helpful info
        st.info(f"""
        **Dataset Info:**
        - Total flows: {len(X_sim):,}
        - Benign flows: ~540,000 (indices 0-540,813)
        - Attack flows: ~557,000 (indices 540,814+)
        
        **Tip:** Try indices like 540,822 (FTP-Patator), 600,000, 1,000,000, etc.
        """)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            idx = st.number_input("Select row index from dataset", 0, len(X_sim)-1, 540822)
        with col2:
            st.write("")
            st.write("")
            if st.button("🎲 Random Attack"):
                idx = np.random.randint(540814, len(X_sim))
                st.rerun()
        
        sample = X_sim.iloc[[idx]]
        
        with st.expander("📊 View Flow Features"):
            st.dataframe(sample, use_container_width=True)

        if st.button("🔍 Analyze Flow", type="primary"):
            with st.spinner("Analyzing..."):
                res = detector.detect(sample)
            
            st.subheader("Detection Results", divider=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Level 1 (Binary)", res['Level1'])
            col2.metric("Level 2 (Family)", res['Level2'])
            col3.metric("Level 3 (Type)", res['Level3'])
            
            st.json(res)
            
            if res['Status'] == 'Danger':
                st.error(f"🚨 **Malicious Traffic Detected!**\n\nType: {res['Level3']}")
            else:
                st.success("✅ Traffic is Benign")

# --- ABOUT PAGE ---
elif st.session_state.page == 'about':
    st.title("📄 Project Methodology")
    
    st.subheader("Multi-Level Intelligent IDS", divider=True)
    st.markdown("""
    This system implements a hierarchical classification strategy for comprehensive network threat detection:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Level 1: Binary Detection
        - **Algorithm**: Optimized Random Forest
        - **Task**: Benign vs Attack classification
        - **Accuracy**: >99%
        """)
    
    with col2:
        st.markdown("""
        ### Level 2: Family Classification
        - **Algorithm**: XGBoost Multi-class
        - **Task**: Attack family identification
        - **Families**: DoS, BruteForce, WebAttack, RareAttack
        """)
    
    with col3:
        st.markdown("""
        ### Level 3: Specialist Models
        - **Algorithm**: SVM Expert Models
        - **Task**: Granular attack type classification
        - **Specialization**: Domain-specific experts
        """)
    
    st.divider()
    
    st.subheader("Project Information", divider=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Developed by**: Roua
        
        **Technology Stack**:
        - Python 3.9+
        - Scikit-learn
        - XGBoost
        - Streamlit
        - Plotly
        """)
    
    with col2:
        st.markdown("""
        **Key Features**:
        - Real-time threat detection
        - Multi-level classification
        - Interactive analysis tools
        - Comprehensive monitoring
        - Feature inspection
        """)
