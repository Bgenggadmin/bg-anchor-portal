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
    with st.form("api_form"):
        st.subheader("Sales & Technical Tracking")
        c1, c2 = st.columns(2)
        new_enq = c1.text_input("New Enquiries")
        off_iss = c2.number_input("Offers Issued (Nos)", min_value=0, step=1)
        
        eng_clar = st.text_area("Engineering Clarifications Pending")
        clar_age = st.text_area("Clarification Ageing (Days)")
        mfg_plan = st.text_area("Manufacturing Planned vs Actual")

        st.subheader("Operational & Purchase Integration")
        proj_code = st.text_input("Project Code(s)", placeholder="e.g. BG-01, BG-05")
        
        # CONDITIONAL TRIGGER
        has_dependency = st.radio("Any Critical Purchase Dependency?", ["NO", "YES"], horizontal=True)
        
        if has_dependency == "YES":
            crit_dep = st.text_area("🔴 List Items & Affected Project Codes", 
                placeholder="e.g.\n1. 8mm 316 Plate (Codes: BG-01, BG-02)\n2. 5HP Motor (Code: BG-05)")
        else:
            st.info("No purchase dependencies flagged for these projects.")

        st.subheader("Management & Decisions")
        f_dec = st.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det = st.text_input("Decision Details / Context")

        if st.form_submit_button("Sync API Report"):
            st.success("API Data recorded.")

# --- 2. AMMU (ZLD) ---
elif role == "ZLD (Ammu)":
    st.header("ZLD Site Entry - Ammu Anchor")
    with st.form("zld_form"):
        st.subheader("Project Execution")
        z1, z2 = st.columns(2)
        proj_code = z1.text_input("Project Code(s)")
        stage = z2.text_input("Project Stage")

        updates = st.text_area("'UPDATES' (Major Site Events)")
        
        # CONDITIONAL TRIGGER
        has_dep_zld = st.radio("Any Critical Purchase Dependency?", ["NO", "YES"], horizontal=True)
        
        if has_dep_zld == "YES":
            crit_dep_zld = st.text_area("🔴 List Items & Affected Project Codes", 
                placeholder="Enter specific material needs here...")
        
        if st.form_submit_button("Sync ZLD Report"):
            st.success("ZLD Report successfully synced.")

# --- 3. SANTHOSHI (PURCHASE) ---
elif role == "Purchase (Santhoshi)":
    st.header("Purchase & Operations Control")
    
    st.subheader("⚠️ High-Priority Site Dependencies")
    st.error("Site Anchors will flag 'YES' if they are stuck for materials like 316 Plates or Motors.")
    
    with st.form("purchase_form"):
        p1, p2 = st.columns(2)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        
        absentees = st.text_area("Absentees Details")
        
        if st.form_submit_button("Sync Purchase Log"):
            st.success("Daily Operations Log Updated.")

# --- 4. MANAGEMENT DASHBOARD ---
else:
    st.header("B&G Management Analytics")
    st.write("Reviewing EOD logs across all Project Codes.")
