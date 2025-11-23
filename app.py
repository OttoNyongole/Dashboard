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


#st.title("Decision Executive dashboard for WATASHA")
#st.caption("Strategic Intelligence for commercial timber ptoduction")
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