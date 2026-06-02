import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE SETUP
st.set_page_config(
    page_title="BFSI RFP Intelligence System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom visual overrides
st.markdown("""
    <style>
    .metric-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #0066cc; }
    </style>
""", unsafe_allow_html=True)

# 2. SIDEBAR NAVIGATION & FILTERS
st.sidebar.title("🔍 Navigation & Filters")
st.sidebar.markdown("Use these parameters to segment live market opportunities.")

priority_filter = st.sidebar.multiselect(
    "Priority Tier",
    options=["HIGH", "MEDIUM", "LOW"],
    default=["HIGH", "MEDIUM"]
)

verticals_list = [
    "BANKING", "FINANCIAL SERVICES", "INSURANCE", 
    "STOCK EXCHANGES", "CAPITAL MARKETS", "WEALTH MANAGEMENT", 
    "ASSET MANAGEMENT", "FINTECH", "ESG & SUSTAINABILITY"
]
selected_vertical = st.sidebar.selectbox("BFSI Vertical Segment", ["ALL"] + verticals_list)
min_score = st.sidebar.slider("Minimum Quality Score", min_value=0, max_value=100, value=25)

# 3. BASELINE DATA PIPELINE
# Mock dataset matching your exact 100-point taxonomy rules
df = pd.DataFrame([
    {
        "rfp_id": 1, "source_portal": "GeM Portal", "unique_tender_id": "GEM/2026/B/8821",
        "title": "Core Banking Analytics Implementation for Credit Risk & NPA Predictive Platforms",
        "organization": "State Bank of India", "geography": "India", "estimated_budget_inr": 4500000.00,
        "submission_deadline": "2026-06-09", "total_score": 88, "priority_level": "HIGH",
        "matched_verticals": ["BANKING", "FINANCIAL SERVICES"], "matched_keywords": "credit risk, npa analytics"
    },
    {
        "rfp_id": 2, "source_portal": "CPPP Portal", "unique_tender_id": "CPPP/IRDAI/2026/04",
        "title": "Actuarial Valuation Engines & ESG BRSR Sustainability Compliance Automation Suite",
        "organization": "IRDAI Authority", "geography": "India", "estimated_budget_inr": 12000000.00,
        "submission_deadline": "2026-06-21", "total_score": 79, "priority_level": "HIGH",
        "matched_verticals": ["INSURANCE", "ESG & SUSTAINABILITY"], "matched_keywords": "actuarial analytics, brsr reporting"
    },
    {
        "rfp_id": 3, "source_portal": "World Bank Dev", "unique_tender_id": "WB-MENA-9912",
        "title": "Digital Lending Infrastructure & Microfinance Data Framework for Neobanks",
        "organization": "International Finance Corporation", "geography": "MENA", "estimated_budget_inr": 2200000.00,
        "submission_deadline": "2026-07-01", "total_score": 62, "priority_level": "MEDIUM",
        "matched_verticals": ["FINTECH"], "matched_keywords": "digital lending analytics"
    }
])

# Apply Sidebar Filters to Data Frame
filtered_df = df[
    (df['total_score'] >= min_score) & 
    (df['priority_level'].isin(priority_filter))
]

if selected_vertical != "ALL":
    filtered_df = filtered_df[filtered_df['matched_verticals'].apply(lambda x: selected_vertical in x)]

# 4. MAIN DASHBOARD CONTENT DISPLAY
st.title("💼 BFSI RFP Monitoring & Intelligence Hub")
st.markdown("Automated algorithmic scoring engine for tracking global financial tenders.")
st.hr()

# High-Level Metrics Row
if not filtered_df.empty:
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='metric-card'><h4>📦 Active RFPs Listed</h4><h2>{len(filtered_df)}</h2></div>", unsafe_allow_html=True)
    with m2:
        high_count = len(filtered_df[filtered_df['priority_level'] == 'HIGH'])
        st.markdown(f"<div class='metric-card' style='border-left-color: #ff3333;'><h4>🚨 High Priority Pipeline</h4><h2>{high_count}</h2></div>", unsafe_allow_html=True)
    with m3:
        total_value = filtered_df['estimated_budget_inr'].sum()
        st.markdown(f"<div class='metric-card' style='border-left-color: #2ecc71;'><h4>💰 Tracked Pipeline Value</h4><h2>₹{total_value:,.2f}</h2></div>", unsafe_allow_html=True)
    with m4:
        avg_score = filtered_df['total_score'].mean()
        st.markdown(f"<div class='metric-card' style='border-left-color: #f1c40f;'><h4>🎯 Avg Intelligence Match</h4><h2>{avg_score:.1f}/100</h2></div>", unsafe_allow_html=True)

st.write(" ")

# 5. GRAPH VISUALIZATIONS
st.subheader("📊 Architectural Pipeline Breakdown")
c1, c2 = st.columns(2)

with c1:
    fig_score = px.histogram(filtered_df, x="total_score", nbins=5, title="RFP Score Density Profile", color_discrete_sequence=['#0066cc'])
    fig_score.update_layout(xaxis_title="Engine Match Score", yaxis_title="RFP Count")
    st.plotly_chart(fig_score, use_container_width=True)

with c2:
    fig_geo = px.pie(filtered_df, names="geography", values="estimated_budget_inr", title="Pipeline Budget Allocation by Region", hole=0.4)
    st.plotly_chart(fig_geo, use_container_width=True)

st.hr()

# 6. INTERACTIVE DATAGRID TABLE
st.subheader("📋 Screened Opportunity Pipeline Tracker")

# Format rendering for list strings
view_df = filtered_df.copy()
view_df['matched_verticals'] = view_df['matched_verticals'].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

st.dataframe(
    view_df[[
        "total_score", "priority_level", "title", "organization", 
        "estimated_budget_inr", "submission_deadline", "source_portal", "matched_verticals", "matched_keywords"
    ]],
    column_config={
        "total_score": st.column_config.ProgressColumn("Engine Score", format="%d", min_value=0, max_value=100),
        "priority_level": st.column_config.TextColumn("Priority Category"),
        "title": st.column_config.TextColumn("Project Scope / RFP Title", width="large"),
        "organization": st.column_config.TextColumn("Issuing Entity"),
        "estimated_budget_inr": st.column_config.NumberColumn("Estimated Budget (INR)", format="₹%,.2f"),
        "submission_deadline": st.column_config.DateColumn("Submission Due Date"),
        "source_portal": st.column_config.TextColumn("Source Origin Portal"),
        "matched_verticals": st.column_config.TextColumn("Taxonomy Buckets Map"),
        "matched_keywords": st.column_config.TextColumn("Taxonomy Keywords Matched")
    },
    hide_index=True,
    use_container_width=True
)

# 7. EXPORT MECHANISM
st.write(" ")
csv_data = view_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Export Screened Active Pipeline Records to CSV Sheet",
    data=csv_data,
    file_name='bfsi_rfp_monitored_pipeline.csv',
    mime='text/csv',
)
