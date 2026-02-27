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

# --- 1. KISHORE (API) - 23 COLUMN INTEGRATION ---
if role == "API (Kishore)":
    st.header("API Site Entry - Kishore Anchor")
    # Wrap everything in a single form
    with st.form("api_form"):
        st.subheader("Sales & Engineering")
        c1, c2, c3 = st.columns(3)
        new_enq = c1.text_input("New Enquiries")
        # UPDATED: Numeric entry as requested
        off_iss = c2.number_input("Offers Issued (Nos)", min_value=0, step=1)
        off_7d = c3.number_input("Offers > 7 Days (Nos)", min_value=0, step=1)

        st.subheader("Technical Progress")
        # UPDATED: Text areas for detailed rows
        eng_clar = st.text_area("Engineering Clarifications Pending")
        clar_age = st.text_area("Clarification Ageing (Days)")
        mfg_plan = st.text_area("Manufacturing Planned vs Actual")

        st.subheader("Operational & Purchase Integration")
        # THE CONDITIONAL TRIGGER
        has_dependency = st.radio("Any Critical Purchase Dependency?", ["NO", "YES"], horizontal=True)
        
        # This creates the dynamic prompt inside the form
        if has_dependency == "YES":
            crit_dep = st.text_area("🔴 List: Project Name vs Requirement", 
                placeholder="e.g. MSN Maithri: 8mm 316 Plate")
        
        ncr_open = st.text_input("NCR Open (Text Entry)") #

        st.subheader("Management & Decisions")
        f_dec = st.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det = st.text_input("Decision Details / Context")

        if st.form_submit_button("Sync API Report"):
            st.success("API Data recorded successfully.")

# --- 2. AMMU (ZLD) - 18 COLUMN INTEGRATION ---
elif role == "ZLD (Ammu)":
    st.header("ZLD Site Entry - Ammu Anchor")
    with st.form("zld_form"):
        st.subheader("Project Execution")
        stage = st.text_input("Project Stage") #
        updates = st.text_area("'UPDATES' (Major Site Events)")
        
        has_dep_zld = st.radio("Any Critical Purchase Dependency?", ["NO", "YES"], horizontal=True)
        
        if has_dep_zld == "YES":
            crit_dep_zld = st.text_area("🔴 List: Project Name vs Requirement")
        
        if st.form_submit_button("Sync ZLD Report"):
            st.success("ZLD Report successfully synced.")

# --- 3. SANTHOSHI (PURCHASE) - 14 COLUMN INTEGRATION ---
elif role == "Purchase (Santhoshi)":
    st.header("Purchase & Operations Entry - Santhoshi")
    
    st.subheader("⚠️ Pending Site Dependencies")
    st.info("Dependencies entered by Kishore or Ammu will appear here.") #

    with st.form("purchase_form"):
        p1, p2 = st.columns(2)
        planned = p1.number_input("Planned Manpower", value=62) #
        actual = p2.number_input("Actual Manpower", value=52) #
        
        absentees = st.text_area("Absentees Details") #
        
        if st.form_submit_button("Sync Purchase Log"):
            st.success("Daily Operations Log Updated.")

# --- 4. MANAGEMENT DASHBOARD ---
else:
    st.header("B&G Management Analytics")
    st.write("EOD review across all B&G Engineering sites.")
