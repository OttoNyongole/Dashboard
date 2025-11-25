import streamlit as st
import pandas as pd
from datetime import datetime
import time
import google.generativeai as genai
#from venv import load_venv
import os
#------------------------------------
# 1. CONFIG AND DATA
#------------------------------------
st.set_page_config(page_title="Dashboard", layout="wide")

#load data
@st.cache_data
def load_data():
    return pd.read_csv("data/mock_data.csv")

df = load_data()

#live clock
def get_time():
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")


st.title("Decision Executive dashboard for WATASHA")
st.caption("Strategic Intelligence for commercial timber ptoduction")
#st.success("Streamlit is working Ready for phase 3")

# 2. CUSTOME CSS (Tailwind-like cards)
#--------------------------------------
st.markdown("""
<style>
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        height: 100%;
    }
    .metric-label { font-size: 0.9rem; color: #64748B; margin-bottom: 0.5rem; }
    .metric-value { font-size: 2rem; font-weight: 700; color: #1E293B; }
    .trend-up { color: #10B981; }
    .trend-down { color: #EF4444; }
    .badge-urgent { background: #FECACA; color: #991B1B; padding: 0.25rem 0.5rem; border-radius: 999px; font-size: 0.75rem; }
    .badge-online { background: #BBF7D0; color: #166534; }
    .activity-item { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 0; border-bottom: 1px solid #E2E8F0; }
    .activity-time { font-size: 0.8rem; color: #94A3B8; }
</style>
""", unsafe_allow_html=True)
#--------------------------------------
# 3. HEADER
#--------------------------------------
col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    st.markdown("<h1 style='margin:0;'>DecisionAI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; color:#64748B;'>Strategic Decision Intelligence</p>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<p style='text-align:center; color:#1E40AF; font-weight:500;'>{get_time()}</p>", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style='text-align:right;'>
        <p style='margin:0; font-weight:600;'>Executive User</p>
        <p style='margin:0; font-size:0.9rem; color:#10B981;'>● Online</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
#--------------------------------------
# 4. TOP METRICS ROW
#--------------------------------------
metrics = ["Active Decisions", "Progress","Agent Items", "system Health"]
cols = st.colums(4)
for i, metric in enumerate(metrics):
    row = df[df["category"] == metric].iloc[0]
    with cols[i]:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">{metric}</div>
            <div class="metric-value">{row['value']} {row['unit']}</div>
            <div style="margin-top:0.5rem; font-size:0.9rem;">
                <span style="color:#64748B;">vs {row['target']} target</span>
                <span class="trend-{'up' if row['trend'] >= 0 else 'down'}">
                    {'↑' if row['trend'] >= 0 else '↓'} {abs(row['trend'])}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------
# 5. MAIN CONTENT: KPI GRID + ACTIVITY FEED
# -------------------------------------------------
left, right = st.columns([3, 1])

with left:
    st.markdown("<h3 style='margin-top:0;'>Key Performance Indicators</h3>", unsafe_allow_html=True)
    kpi_names = ["Quarterly Revenue", "Strategic Initiatives", "Decision Velocity",
                 "Risk Score", "Team Collaboration", "Market Position"]
    rows = st.columns(2)
    for i, name in enumerate(kpi_names):
        row = df[df["category"] == name].iloc[0]
        with rows[i % 2]:
            progress = row["progress"]
            color = "#10B981" if "On Track" in row["status"] else "#F59E0B" if progress < 80 else "#EF4444"
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">{name}</div>
                <div class="metric-value">{row['value']}{row['unit']}</div>
                <div style="margin:0.5rem 0;">
                    <div style="background:#E2E8F0; border-radius:999px; height:8px; overflow:hidden;">
                        <div style="background:{color}; width:{progress}%; height:100%; transition:0.3s;"></div>
                    </div>
                </div>
                <div style="font-size:0.9rem; color:#64748B;">
                    {row['status']}
                    <span class="trend-{'up' if row['trend'] >= 0 else 'down'}">
                        {'↑' if row['trend'] >= 0 else '↓'} {abs(row['trend'])}{' ' + row['unit'].replace('%','') if row['trend'] != 0 else ''}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if i % 2 == 1 and i != len(kpi_names) - 1:
                st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

with right:
    st.markdown("<h3 style='margin-top:0;'>Recent Activity</h3>", unsafe_allow_html=True)
    
    activities = [
        ("Market Expansion", "Decision updated", "16 min ago", True),
        ("Q4 Budget", "New comment by CFO", "32 min ago", False),
        ("Risk Assessment", "AI flagged anomaly", "1 hour ago", True),
        ("Team Sync", "2 new collaborators invited", "2 hours ago", False),
        ("Forecast Model", "Retrained with new data", "3 hours ago", False),
    ]
    
    st.markdown("<div class='card' style='height:100%;'>", unsafe_allow_html=True)
    for title, desc, time, urgent in activities:
        st.markdown(f"""
        <div class="activity-item">
            <div style="width:8px; height:8px; background:#1E40AF; border-radius:50%;"></div>
            <div style="flex:1;">
                <div style="font-weight:600; font-size:0.95rem;">{title}</div>
                <div style="font-size:0.85rem; color:#64748B;">{desc}</div>
            </div>
            <div class="activity-time">{time}</div>
        </div>
        """, unsafe_allow_html=True)
        if urgent:
            st.markdown("<span class='badge-urgent'>Urgent</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
#--------------------------------------
# 6. FOOTER
#--------------------------------------
st.markdown("---")
st.caption("Built with Streamlit • © 2024 WATASHA . Data auto-refresh every 60s")

# Auto-refresh every 60 seconds
time.sleep(1)
st.rerun()

#------------------------------------