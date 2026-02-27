import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="B&G Digital Portal", layout="wide")

# India Standard Time for the 5:30 PM Nudge
IST = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(IST)

# --- 1. FIXED STYLING SECTION ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR NAVIGATION & 5:30 PM NUDGE ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Your Role:", 
    ["Purchase (Santhoshi)", "API (Kishore)", "ZLD (Ammu)", "Management Dashboard"])

# 5:30 PM Nudge Logic
if now_ist.hour >= 17 and now_ist.minute >= 30:
    st.sidebar.warning("⏰ **EOD REMINDER:** Please submit your site report before leaving.")

st.divider()

# --- 3. PURCHASE BRIDGE (Santhoshi's View) ---
if role == "Purchase (Santhoshi)":
    st.header("Purchase & Operations Entry")
    st.subheader("⚠️ Pending Indents from API/ZLD")
    
    # This table will eventually pull from your master_log.csv
    st.info("The system is ready to receive dependencies from Kishore and Ammu.")
    
    with st.expander("Update Purchase Status"):
        st.text_input("Enter Status Update (e.g., PO Issued for Pumps)")
        st.button("Update Sites")

# --- 4. SITE ENTRIES (Kishore & Ammu) ---
elif role in ["API (Kishore)", "ZLD (Ammu)"]:
    st.header(f"Site Entry - {role}")
    with st.form("site_form"):
        project = st.selectbox("Project", ["30KL OIL SYSTEM", "MSN REACTORS", "DIVIS UNIT-II"])
        dependency = st.text_area("Critical Purchase Dependency", help="Items needed from Santhoshi")
        if st.form_submit_button("Sync to Master Log"):
            st.success("Report recorded successfully.")

# --- 5. MANAGEMENT DASHBOARD ---
else:
    st.header("B&G Management Dashboard")
    st.write("Summary of site progress and purchase delays.")
    st.download_button("📥 Download Master Log", "Date,Project,Status\n2026-02-27,MSN,Active", "bg_report.csv")
