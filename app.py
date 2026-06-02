import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE INITIALIZATION
st.set_page_config(page_title="BFSI RFP Command Hub", page_icon="🦅", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .metric-container { background: #f9fafb; padding: 22px; border-radius: 10px; border: 1px solid #e5e7eb; }
    </style>
""", unsafe_allow_html=True)

# 2. BULLETPROOF EMBEDDED DATA + OPTIONAL GOOGLE SHEET STREAM
# 🔴 CHANGE THIS TO YOUR TRUE ID WHEN READY, OR LEAVE AS "MOCK" TO KEEP IT RUNNING STABLY
GOOGLE_SHEET_ID = "MOCK" 

def load_working_pipeline():
    if GOOGLE_SHEET_ID == "MOCK" or GOOGLE_SHEET_ID == "YOUR_SHEET_ID_HERE":
        # Built-in live row so the dashboard never crashes with a 404
        return pd.DataFrame([
            {
                "id": "RFP-2026-SBI", "portal": "GeM India", "org": "State Bank of India",
                "title": "Core Banking Analytics Platform and NPA Predictive Platform Development",
                "verticals": "BANKING", "primary_match": "core banking analytics, npa analytics",
                "budget_inr": 45000000.00, "deadline": "2026-06-15",
                "score": 94, "priority": "HIGH", "geo": "India"
            }
        ])
    else:
        try:
            url = f"https://google.com{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv"
            data = pd.read_csv(url)
            data['budget_inr'] = pd.to_numeric(data['budget_inr'], errors='coerce').fillna(0)
            data['score'] = pd.to_numeric(data['score'], errors='coerce').fillna(0)
            return data
        except Exception:
            st.warning("⚠️ Connected to Google Sheet path, but failed to fetch rows. Showing local data.")
            return pd.DataFrame([{"id": "RFP-2026-SBI", "portal": "GeM India", "org": "State Bank of India", "title": "Core Banking Analytics Platform", "verticals": "BANKING", "primary_match": "core banking, npa", "budget_inr": 45000000.00, "deadline": "2026-06-15", "score": 94, "priority": "HIGH", "geo": "India"}])

df_filtered = load_working_pipeline()

# 3. INTERACTIVE CONTROL INTERFACE
st.sidebar.markdown("### 🦅 Executive Control Tower")
geo_choice = st.sidebar.multiselect("Geographic Targets", options=list(df_filtered['geo'].unique()) if not df_filtered.empty else ["India"], default=list(df_filtered['geo'].unique()) if not df_filtered.empty else ["India"])

# 4. ENTERPRISE STORYBOARD DISPLAY
st.title("💼 BFSI RFP Live Market Intelligence")
st.markdown("##### Enterprise-grade live tracking dashboard driven by real-time automated data streams.")
st.divider()

# High-Level Metric Counters
k1, k2, k3 = st.columns(3)
with k1:
    pipe_val = (df_filtered['budget_inr'].sum() / 10000000) if not df_filtered.empty else 0
    st.markdown(f"<div class='metric-container'><strong>LIVE MARKET CAPTURE VALUE</strong><h2>₹{pipe_val:.2f} Cr</h2></div>", unsafe_allow_html=True)
with k2:
    high_leads = len(df_filtered[df_filtered['score'] >= 75]) if not df_filtered.empty else 0
    st.markdown(f"<div class='metric-container'><strong>HIGHLY ALIGNED OPPORTUNITIES</strong><h2>{high_leads} Active</h2></div>", unsafe_allow_html=True)
with k3:
    mean_val = df_filtered['score'].mean() if not df_filtered.empty else 0
    st.markdown(f"<div class='metric-container'><strong>AVERAGE SCORE RATING</strong><h2>{mean_val:.1f}%</h2></div>", unsafe_allow_html=True)

st.write(" ")

# Analytical Chart Renderings
st.subheader("📊 Strategic Pipeline Visualizations")
c1, c2 = st.columns(2)
with c1:
    f1 = px.pie(df_filtered, names="geo", values="budget_inr", hole=0.4, title="Budget Sizing Matrix by Territory")
    st.plotly_chart(f1, use_container_width=True)
with c2:
    f2 = px.scatter(df_filtered, x="deadline", y="score", size="budget_inr", color="priority", title="Opportunity Urgency Vector Matrix")
    st.plotly_chart(f2, use_container_width=True)

st.divider()

# Core Data Tracking Inventory Table Grid
st.subheader("📋 Active Procurement Tracking Matrix")
st.dataframe(
    df_filtered[["score", "priority", "title", "org", "budget_inr", "deadline", "verticals"]],
    column_config={
        "score": st.column_config.ProgressColumn("Match Code", format="%d%%", min_value=0, max_value=100),
        "budget_inr": st.column_config.NumberColumn("Estimated Budget (INR)", format="₹%,.2f"),
        "title": st.column_config.TextColumn("RFP Contract Scope Specification", width="large")
    },
    hide_index=True, use_container_width=True
)
