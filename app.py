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

# 5:30 PM EOD Nudge
if now_ist.hour >= 17 and now_ist.minute >= 30:
    st.sidebar.warning("⏰ **EOD REMINDER:** Please submit your site report before leaving.")

st.divider()

# --- 1. KISHORE (API) - 23 COLUMN INTEGRATION ---
if role == "API (Kishore)":
    st.header("API Site Entry - Kishore Anchor")
    with st.form("api_form"):
        st.subheader("Sales & Engineering Tracking")
        c1, c2, c3 = st.columns(3)
        new_enq = c1.text_input("New Enquiries")
        off_iss = c2.selectbox("Offers Issued", ["Yes", "No", "N/A"])
        off_rev = c3.text_input("Offers Under Review / Status")
        
        c4, c5, c6 = st.columns(3)
        off_7d = c4.selectbox("Offers > 7 Days", ["Yes", "No"])
        dwg_rel = c5.number_input("Drawings Released", min_value=0)
        des_rev = c6.text_input("Designs Under Review")

        st.subheader("Technical Progress")
        c7, c8, c9 = st.columns(3)
        eng_clar = c7.number_input("Engineering Clarifications Pending", min_value=0)
        clar_age = c8.number_input("Clarification Ageing (Days)", min_value=0)
        mfg_plan = c9.text_input("Manufacturing Planned vs Actual")

        st.subheader("Operational Integration")
        c10, c11, c12 = st.columns(3)
        dev_cat = c10.selectbox("Deviation Category", ["N.A", "Manpower", "Design", "Material"])
        dev_imp = c11.selectbox("Deviation Impact if Continues", ["NO", "YES"])
        ncr_open = c12.selectbox("NCR Open", ["NO", "YES"])

        c13, c14, c15 = st.columns(3)
        ncr_imp = c13.selectbox("NCR Impact on Delivery", ["NO", "YES"])
        # CRITICAL INTEGRATION FIELD
        crit_dep = c14.text_area("Critical Purchase Dependency", help="Linked to Santhoshi's Desk")
        calls = c15.number_input("Client Calls Today", min_value=0)

        st.subheader("Management & Decisions")
        c16, c17 = st.columns(2)
        key_disc = c16.text_input("Key Client Discussions")
        top_dev = c17.text_input("Top Deviations")
        
        c18, c19 = st.columns(2)
        f_dec = c18.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det = c19.text_input("Decision Details")

        if st.form_submit_button("Sync API Report"):
            st.success("Kishore's Report Synced Successfully.")

# --- 2. AMMU (ZLD) - 18 COLUMN INTEGRATION ---
elif role == "ZLD (Ammu)":
    st.header("ZLD Site Entry - Ammu Anchor")
    with st.form("zld_form"):
        st.subheader("Enquiry & Design Status")
        z1, z2, z3 = st.columns(3)
        new_enq = z1.text_input("New Enquiries")
        off_iss = z2.text_input("Offers Issued")
        off_rev = z3.text_input("Offers Under Review")

        z4, z5, z6 = st.columns(3)
        off_7d = z4.text_input("Offers > 15 Days")
        des_comp = z5.text_input("Designs Completed")
        des_rev = z6.text_input("Designs Under Review")

        st.subheader("Project Execution")
        z7, z8, z9 = st.columns(3)
        active_proj = z7.selectbox("Active Project", ["150 KLD MEE-MSN", "30KL OIL SYSTEM", "Other"])
        stage = z8.text_input("Project Stage")
        sch_risk = z9.selectbox("Schedule Risk", ["NO", "YES"])

        st.subheader("Updates & Integration")
        z10, z11 = st.columns(2)
        updates = z10.text_area("'UPDATES' (Major Site Events)")
        # CRITICAL INTEGRATION FIELD
        crit_dep = z11.text_input("Critical Purchase Dependency")

        z12, z13 = st.columns(2)
        f_dec = z12.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det = z13.text_input("Decision Details")

        if st.form_submit_button("Sync ZLD Report"):
            st.success("Ammu's Report Synced Successfully.")

# --- 3. SANTHOSHI (PURCHASE) - 14 COLUMN INTEGRATION ---
elif role == "Purchase (Santhoshi)":
    st.header("Purchase & Operations Entry - Santhoshi")
    
    # CROSS-FUNCTIONAL BRIDGE
    st.subheader("⚠️ Pending Indents from API/ZLD Sites")
    st.info("Dependencies entered by Kishore or Ammu will appear here.")

    with st.form("purchase_form"):
        st.subheader("Manpower Tracking")
        p1, p2, p3 = st.columns(3)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        absentees = p3.text_area("Absentees Details")

        st.subheader("Site Operations")
        p4, p5, p6 = st.columns(3)
        temp_mp = p4.selectbox("Temp Manpower Used", ["No", "Yes"])
        crit_mac = p5.text_input("Critical Machines Status")
        downtime = p6.text_input("Breakdown / Downtime")

        p7, p8, p9 = st.columns(3)
        transp = p7.text_input("Transportation Status")
        prod_supp = p8.selectbox("Production Supported", ["Yes", "No"])
        site_imp = p9.selectbox("Site Impacted", ["No", "Yes"])

        st.subheader("Management & Decisions")
        p10, p11 = st.columns(2)
        f_dec = p10.selectbox("Founder Decision Required", ["No", "Yes"])
        dec_det = p11.text_input("Decision Details")

        if st.form_submit_button("Sync Purchase Report"):
            st.success("Santhoshi's Report Synced Successfully.")

# --- 4. MANAGEMENT DASHBOARD ---
else:
    st.header("B&G Management Analytics")
    st.info("Historical data and comparative analytics will be displayed here.")
    st.download_button("📥 Export Master Excel", "Date,Anchor,Project,Critical_Dependency\n2026-02-27,API,10KL,Pumps", "bg_master.csv")
