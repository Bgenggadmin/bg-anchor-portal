import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="B&G Digital Portal", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(IST)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

st.divider()

# --- 1. KISHORE (API) ---
if role == "API (Kishore)":
    st.header("API Site Entry - Kishore Anchor")
    
    st.subheader("Operational & Purchase Integration")
    # MOVE TRIGGER OUTSIDE THE FORM TO FORCE REFRESH
    has_dependency = st.radio("Any Critical Purchase Dependency?", ["NO", "YES"], horizontal=True, key="api_dep")
    
    # Conditional text area appears immediately
    crit_dep_value = ""
    if has_dependency == "YES":
        crit_dep_value = st.text_area("🔴 List: Project Name vs Requirement", 
            placeholder="e.g.\nMSN Maithri: 8mm 316 Plate\n30KL Oil System: 5HP Motor", height=150)

    # All other fields stay inside the form
    with st.form("api_form"):
        st.subheader("Sales & Technical Tracking")
        c1, c2 = st.columns(2)
        new_enq = c1.text_input("New Enquiries")
        off_iss = c2.number_input("Offers Issued (Nos)", min_value=0, step=1)
        
        eng_clar = st.text_area("Engineering Clarifications Pending")
        clar_age = st.text_area("Clarification Ageing (Days)")
        mfg_plan = st.text_area("Manufacturing Planned vs Actual")

        st.subheader("Management & Decisions")
        f_dec = st.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det = st.text_input("Decision Details / Context")

        if st.form_submit_button("Sync API Report"):
            st.success("API Data recorded.")

# --- 2. AMMU (ZLD) ---
elif role == "ZLD (Ammu)":
    st.header("ZLD Site Entry - Ammu Anchor")
    
    # MOVE TRIGGER OUTSIDE THE FORM
    has_dep_zld = st.radio("Any Critical Purchase Dependency?", ["NO", "YES"], horizontal=True, key="zld_dep")
    
    crit_dep_zld_val = ""
    if has_dep_zld == "YES":
        crit_dep_zld_val = st.text_area("🔴 List: Project Name vs Requirement", 
            placeholder="e.g. MSN Oncology: Centrifugal Pump PO")

    with st.form("zld_form"):
        st.subheader("Project Execution")
        stage = st.text_input("Project Stage (e.g. Commissioning)")
        updates = st.text_area("'UPDATES' (Major Site Events)")
        
        if st.form_submit_button("Sync ZLD Report"):
            st.success("ZLD Report successfully synced.")

# --- 3. SANTHOSHI (PURCHASE) ---
elif role == "Purchase (Santhoshi)":
    st.header("Purchase & Operations Control")
    st.subheader("⚠️ High-Priority Site Dependencies")
    st.info("If Kishore or Ammu flagged 'YES', their Project vs Requirement list will appear here.")
    
    with st.form("purchase_form"):
        p1, p2 = st.columns(2)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        
        absentees = st.text_area("Absentees Details")
        crit_machines = st.text_input("Critical Machines Status")
        
        if st.form_submit_button("Sync Purchase Log"):
            st.success("Daily Operations Log Updated.")

# --- 4. MANAGEMENT DASHBOARD ---
else:
    st.header("B&G Management Analytics")
    st.write("Reviewing EOD logs for B&G Engineering Industries.")
