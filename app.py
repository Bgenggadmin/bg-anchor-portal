import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="B&G Digital Portal", layout="wide")

# India Standard Time for the 5:30 PM Nudge
IST = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(IST)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Your Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

# 5:30 PM EOD Nudge
if now_ist.hour >= 17 and now_ist.minute >= 30:
    st.sidebar.warning("⏰ **EOD REMINDER:** Please submit your site report before leaving.")

st.divider()

# --- 1. DATA ENTRY FIELDS (Kishore & Ammu) ---
if role in ["API (Kishore)", "ZLD (Ammu)"]:
    st.header(f"Site Entry Form - {role}")
    with st.form("site_entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            project = st.selectbox("Select Project", ["30KL OIL SYSTEM", "MSN REACTORS", "DIVIS UNIT-II", "Other"])
            stage = st.text_input("Current Stage of Work", placeholder="e.g., Fabrication")
        with col2:
            manpower = st.number_input("Manpower on Site", min_value=0, step=1)
            dependency = st.text_area("Critical Purchase Dependency", placeholder="What do you need from Santhoshi?")
        
        submitted = st.form_submit_button("Sync to Master Log")
        if submitted:
            st.success(f"✅ Data for {project} recorded!")

# --- 2. PURCHASE VIEW (Santhoshi) ---
elif role == "Purchase (Santhoshi)":
    st.header("Purchase & Operations Entry")
    st.subheader("⚠️ Pending Indents from API/ZLD")
    # This will show the data entered by Kishore/Ammu above
    st.info("Once Kishore or Ammu submits data, it will appear here in a table.")
    
    with st.expander("Update Purchase Status"):
        st.text_input("Enter Update (e.g., PO Issued)")
        st.button("Update Sites")

# --- 3. MANAGEMENT VIEW ---
else:
    st.header("Management Dashboard")
    st.write("Summary of all site activities.")
    st.download_button("📥 Download Excel Report", "Date,Project,Dependency\n2026-02-27,MSN,Centrifugal Pumps", "bg_report.csv")
