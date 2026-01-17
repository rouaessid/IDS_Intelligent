# app.py

import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from detector import IDSDetector
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Intelligent IDS Dashboard",
    page_icon="🛡️",
    layout="wide",
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

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background-color: #1E293B !important;
    border-right: 1px solid #334155;
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
    color: #F8FAFC !important;
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

/* ===== SUCCESS ===== */
.stSuccess {
    background-color: rgba(34, 197, 94, 0.15) !important;
    border-left: 4px solid #22C55E;
    color: #DCFCE7 !important;
}

/* ===== ALERT ===== */
.stAlert {
    background-color: rgba(220, 38, 38, 0.18) !important;
    border-left: 4px solid #DC2626;
    color: #FEE2E2 !important;
}

/* ===== INFO ===== */
.stInfo {
    background-color: rgba(37, 99, 235, 0.18) !important;
    border-left: 4px solid #2563EB;
    color: #DBEAFE !important;
}



/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
     background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #334155;
}

/* ===== INPUTS ===== */
input, textarea {
    background-color: #0F172A !important;
    color: #F8FAFC !important;
    border: 1px solid #334155 !important;
}

/* ===== REMOVE WHITE AREAS ===== */
section[data-testid="stMain"] {
    background-color: #0F172A !important;
}

/* ===== SUBHEADERS ===== */
.stMarkdown h2, .stMarkdown h3 {
    background-color: transparent !important;
    color: #F8FAFC !important;
}

/* ===== CONTAINERS ===== */
div[data-testid="stVerticalBlock"] {
    background-color: transparent !important;
}

div[data-testid="stHorizontalBlock"] {
    background-color: transparent !important;
}

/* ===== JSON VIEWER ===== */
/* ===== JSON / CODE BLOCKS FIX ===== */
pre, code {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #475569 !important;
    border-radius: 10px;
    padding: 14px !important;
    font-size: 0.9rem;
}

/* Streamlit JSON container */
[data-testid="stJson"] {
    background-color: #1E293B !important;
    border: 1px solid #475569 !important;
    border-radius: 10px;
    padding: 12px;
}

/* JSON keys / values */
[data-testid="stJson"] span {
    color: #F8FAFC !important;
}

/* Remove inner white layers */
[data-testid="stJson"] * {
    background-color: transparent !important;
}

/* ===== EXPANDER CONTAINER ===== */
[data-testid="stExpander"] {
    background-color: #1E293B !important;
    border: 1px solid #475569 !important;
    border-radius: 10px;
}

/* Expander header */
[data-testid="stExpander"] summary {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
}

/* ===== DATAFRAME - SIMPLE APPROACH ===== */
[data-testid="stDataFrame"] {
    background-color: #1E293B !important;
    border: 1px solid #475569;
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

# --- SIDEBAR ---
st.sidebar.title("🛡️ IDS Control Center")
st.sidebar.markdown("---")
mode = st.sidebar.radio("Select Mode", ["Live Dashboard", "Manual Analysis", "Project Info"])

# --- DATA LOADING (Simulation) ---
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

# --- MAIN PAGE ---
if mode == "Live Dashboard":
    st.title("🛡️ Real-time Intrusion Detection System")
    st.markdown("Monitoring network flows and identifying multi-level threats.")

    # Top Metrics
    m1, m2, m3, m4 = st.columns(4)
    total_flows = st.session_state.get('total_flows', 0)
    alerts_count = st.session_state.get('alerts_count', 0)
    
    m1.metric("Flows Analyzed", total_flows)
    m2.metric("Threats Detected", alerts_count, delta=f"{alerts_count} active", delta_color="inverse")
    m3.metric("System Status", "Operational", delta="Optimal")
    m4.metric("Avg Latency", "12ms")

    # Simulation Logic
    if st.button("Start Simulation"):
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
                
                total_flows += 1
                if res['Status'] == 'Danger':
                    alerts_count += 1
                    alerts_log.insert(0, {
                        "Time": time.strftime("%H:%M:%S"),
                        "Family": res['Level2'],
                        "Type": res['Level3'],
                        "Severity": "High"
                    })
                
                st.session_state['total_flows'] = total_flows
                st.session_state['alerts_count'] = alerts_count

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

elif mode == "Manual Analysis":
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
                import numpy as np
                idx = np.random.randint(540814, len(X_sim))
                st.experimental_rerun()
        
        sample = X_sim.iloc[[idx]]
        
        with st.expander("📊 View Flow Features"):
            st.dataframe(sample, use_container_width=True)


        if st.button("🔍 Analyze Flow", type="primary"):
            with st.spinner("Analyzing..."):
                res = detector.detect(sample)
            
            st.markdown("""
            <div style='background-color: #0F172A; padding: 20px; border-radius: 8px; margin: 20px 0;'>
                <h3 style='color: #F8FAFC; margin: 0 0 15px 0;'>Detection Results</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Level 1", res['Level1'])
            col2.metric("Level 2", res['Level2'])
            col3.metric("Level 3", res['Level3'])
            
            st.json(res)
            
            if res['Status'] == 'Danger':
                st.error(f"🚨 **Malicious Traffic Detected!**\n\nType: {res['Level3']}")
            else:
                st.success("✅ Traffic is Benign")

elif mode == "Project Info":
    st.title("📄 Project Methodology")
    st.markdown("""
    ### Multi-Level Intelligent IDS
    This system implements a hierarchical classification strategy:
    
    1. **Level 1 (Binary)**: Binary classification using optimized Random Forest.
    2. **Level 2 (Family)**: Multi-class classification to identify the attack family.
    3. **Level 3 (Specialist)**: Specific expert models for granular attack identification (DoS, BruteForce, WebAttack).
    
    **Developed by**: Roua
    **Stack**: Python, Scikit-learn, XGBoost, Streamlit.
    """)
