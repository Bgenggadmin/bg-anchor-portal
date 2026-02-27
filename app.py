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

# --- 1. KISHORE (API) - ALL 23 COLUMNS ---
if role == "API (Kishore)":
    st.header("API Site Entry - Kishore Anchor")
    
    # TRIGGER OUTSIDE FORM FOR INSTANT PROMPT
    st.subheader("Operational & Purchase Integration")
    has_dependency = st.radio("Any Critical Purchase Dependency?", ["NO", "YES"], horizontal=True, key="api_dep")
    if has_dependency == "YES":
        crit_dep = st.text_area("🔴 List: Project Name vs Requirement", placeholder="e.g. MSN Maithri: 8mm 316 Plate")

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
        eng_clar = st.text_area("Engineering Clarifications Pending")
        clar_age = st.text_area("Clarification Ageing (Days)")
        mfg_plan = st.text_area("Manufacturing Planned vs Actual")

        st.subheader("Deviations & NCR")
        c10, c11, c12 = st.columns(3)
        dev_cat = c10.selectbox("Deviation Category", ["N.A", "Manpower", "Design", "Material"])
        dev_imp = c11.selectbox("Deviation Impact if Continues", ["NO", "YES"])
        ncr_open = st.text_input("NCR Open (Details)")
        
        c13, c14 = st.columns(2)
        ncr_imp = c13.selectbox("NCR Impact on Delivery", ["NO", "YES"])
        calls = c14.number_input("Client Calls Today", min_value=0)

        st.subheader("Management & Decisions")
        key_disc = st.text_input("Key Client Discussions")
        top_dev = st.text_input("Top Deviations")
        f_dec = st.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det = st.text_input("Decision Details / Context")

        if st.form_submit_button("Sync API Report"):
            st.success("API Data recorded.")

# --- 2. AMMU (ZLD) - ALL 18 COLUMNS ---
elif role == "ZLD (Ammu)":
    st.header("ZLD Site Entry - Ammu Anchor")
    
    st.subheader("Purchase Integration")
    has_dep_zld = st.radio("Any Critical Purchase Dependency?", ["NO", "YES"], horizontal=True, key="zld_dep")
    if has_dep_zld == "YES":
        crit_dep_zld = st.text_area("🔴 List: Project Name vs Requirement")

    with st.form("zld_form"):
        st.subheader("Enquiry & Design Status")
        z1, z2, z3 = st.columns(3)
        new_enq_z = z1.text_input("New Enquiries")
        off_iss_z = z2.text_input("Offers Issued")
        off_rev_z = z3.text_input("Offers Under Review")

        st.subheader("Project Execution")
        z4, z5, z6 = st.columns(3)
        active_proj = z4.selectbox("Active Project", ["150 KLD MEE-MSN", "30KL OIL SYSTEM", "Other"])
        stage = z5.text_input("Project Stage")
        sch_risk = z6.selectbox("Schedule Risk", ["NO", "YES"])

        updates = st.text_area("'UPDATES' (Major Site Events)")
        f_dec_z = st.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det_z = st.text_input("Decision Details")

        if st.form_submit_button("Sync ZLD Report"):
            st.success("ZLD Report successfully synced.")

# --- 3. SANTHOSHI (PURCHASE) - ALL 14 COLUMNS ---
elif role == "Purchase (Santhoshi)":
    st.header("Purchase & Operations Control")
    st.info("Dependencies from Kishore/Ammu will reflect here.")

    with st.form("purchase_form"):
        st.subheader("Manpower & Site Status")
        p1, p2, p3 = st.columns(3)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        temp_mp = p3.selectbox("Temp Manpower Used", ["No", "Yes"])

        st.subheader("Operations Tracking")
        p4, p5, p6 = st.columns(3)
        crit_machines = p4.text_input("Critical Machines Status")
        downtime = p5.text_input("Breakdown / Downtime")
        transp = p6.text_input("Transportation Status")

        p7, p8 = st.columns(2)
        prod_supp = p7.selectbox("Production Supported", ["Yes", "No"])
        site_imp = p8.selectbox("Site Impacted", ["No", "Yes"])
        
        absentees = st.text_area("Absentees Details")
        f_dec_p = st.selectbox("Founder Decision Required", ["No", "Yes"])
        dec_det_p = st.text_input("Decision Details")
        
        if st.form_submit_button("Sync Purchase Log"):
            st.success("Daily Operations Log Updated.")

# --- 4. MANAGEMENT DASHBOARD ---
else:
    st.header("B&G Management Analytics")
    st.write("Full EOD report summary.")
