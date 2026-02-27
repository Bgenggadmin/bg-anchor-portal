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

# --- 1. KISHORE (API) - ENHANCED OPERATIONAL LOGIC ---
if role == "API (Kishore)":
    st.header("API Site Entry - Kishore Anchor")
    with st.form("api_form"):
        st.subheader("Sales & Enquiry Tracking")
        c1, c2, c3 = st.columns(3)
        new_enq = c1.text_input("New Enquiries")
        off_iss = c2.number_input("Offers Issued (Nos)", min_value=0, step=1)
        off_rev = c3.text_input("Offers Under Review / Status")
        
        c4, c5, c6 = st.columns(3)
        off_7d = c4.number_input("Offers > 7 Days (Nos)", min_value=0, step=1)
        dwg_rel = c5.number_input("Drawings Released", min_value=0)
        des_rev = c6.text_input("Designs Under Review")

        st.subheader("Technical & Manufacturing Progress")
        # Multi-row entry for clarifications
        eng_clar = st.text_area("Engineering Clarifications Pending (Details)", 
                                placeholder="List each clarification item here...")
        
        # UPDATED: Text area to match multiple clarifications listed above
        clar_age = st.text_area("Clarification Ageing (Days per Item)", 
                                 placeholder="e.g.\nItem 1: 5 Days\nItem 2: 12 Days")
        
        mfg_plan = st.text_area("Manufacturing Planned vs Actual (Detailed Points)", 
                                placeholder="Enter specific progress points...")

        st.subheader("Operational Integration")
        c10, c11, c12 = st.columns(3)
        # ADDED: Project Code field
        proj_code = c10.text_input("Project Code", placeholder="e.g., BG-API-2026-001")
        dev_cat = c11.selectbox("Deviation Category", ["N.A", "Manpower", "Design", "Material"])
        dev_imp = c12.selectbox("Deviation Impact if Continues", ["NO", "YES"])
        
        c13, c14, c15 = st.columns(3)
        ncr_open = c13.text_input("NCR Open (Enter Details)")
        ncr_imp = c14.selectbox("NCR Impact on Delivery", ["NO", "YES"])
        # CRITICAL INTEGRATION FIELD
        crit_dep = c15.text_area("Critical Purchase Dependency", help="Linked to Santhoshi's Desk")

        st.subheader("Management & Decisions")
        c16, c17 = st.columns(2)
        key_disc = c16.text_input("Key Client Discussions")
        top_dev = c17.text_input("Top Deviations")
        
        c18, c19 = st.columns(2)
        f_dec = c18.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det = c19.text_input("Decision Details")

        if st.form_submit_button("Sync API Report"):
            st.success("Kishore's Report Synced Successfully.")

# --- 2. AMMU (ZLD) ---
elif role == "ZLD (Ammu)":
    st.header("ZLD Site Entry - Ammu Anchor")
    with st.form("zld_form"):
        st.subheader("Project Execution")
        z1, z2, z3 = st.columns(3)
        # Standardized with Project Code logic
        zld_code = z1.text_input("Project Code")
        active_proj = z2.selectbox("Active Project", ["150 KLD MEE-MSN", "30KL OIL SYSTEM", "Other"])
        stage = z3.text_input("Project Stage")

        st.subheader("Updates & Integration")
        z10, z11 = st.columns(2)
        updates = z10.text_area("'UPDATES' (Major Site Events)")
        crit_dep = z11.text_input("Critical Purchase Dependency")

        if st.form_submit_button("Sync ZLD Report"):
            st.success("Ammu's Report Synced Successfully.")

# --- 3. SANTHOSHI (PURCHASE) ---
elif role == "Purchase (Santhoshi)":
    st.header("Purchase & Operations Entry - Santhoshi")
    
    # This acts as the bridge
    st.subheader("⚠️ Pending Indents from API/ZLD Sites")
    st.info("Dependencies entered by Kishore or Ammu will appear here.")

    with st.form("purchase_form"):
        p1, p2 = st.columns(2)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        
        crit_mac = st.text_input("Critical Machines Status")
        
        if st.form_submit_button("Sync Purchase Report"):
            st.success("Santhoshi's Report Synced Successfully.")

# --- 4. MANAGEMENT DASHBOARD ---
else:
    st.header("B&G Management Analytics")
    st.write("EOD Summary for B&G Engineering Industries.")
