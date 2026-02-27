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

# --- 1. KISHORE (API) - REFINED FOR MULTIPLE ROWS ---
if role == "API (Kishore)":
    st.header("API Site Entry - Kishore Anchor")
    
    # Critical Purchase Dependency
    st.subheader("Operational & Purchase Integration")
    has_dependency = st.radio("Any Critical Purchase Dependency?", ["NO", "YES"], horizontal=True)
    if has_dependency == "YES":
        st.info("💡 Enter multiple requirements below (e.g., Project vs Plate/Pipe specs)")
        # Use data_editor for multiple rows of dependencies
        dep_df = pd.DataFrame([{"Project Name": "", "Requirement": ""}])
        edited_dep = st.data_editor(dep_df, num_rows="dynamic", use_container_width=True, key="api_dep_table")

    with st.form("api_form"):
        st.subheader("Enquiry & Design Tracking")
        st.write("📝 **List New Enquiries & Design Status**")
        # Multiple rows for enquiries
        enq_df = pd.DataFrame([{"Enquiry/Client": "", "Offers Issued": 0, "Status": "Review", "Dwg Released": 0}])
        api_enq_data = st.data_editor(enq_df, num_rows="dynamic", use_container_width=True, key="api_enq_table")
        
        st.subheader("Technical & Manufacturing Progress")
        c1, c2 = st.columns(2)
        eng_clar = c1.text_area("Engineering Clarifications Pending")
        mfg_plan = c2.text_area("Manufacturing Planned vs Actual")

        st.subheader("Deviations & Management")
        c3, c4, c5 = st.columns(3)
        dev_cat = c3.selectbox("Deviation Category", ["N.A", "Manpower", "Design", "Material"])
        ncr_open = c4.text_input("NCR Open (Details)")
        f_dec = c5.selectbox("Founder Decision Required", ["NO", "YES"])
        
        dec_det = st.text_input("Decision Details / Context")

        if st.form_submit_button("Sync API Report"):
            st.success("Kishore's API Data recorded.")

# --- 2. AMMU (ZLD) - REFINED FOR MULTIPLE PROJECTS ---
elif role == "ZLD (Ammu)":
    st.header("ZLD Site Entry - Ammu Anchor")
    
    # Purchase Integration
    st.subheader("Purchase Integration")
    has_dep_zld = st.radio("Any Critical Purchase Dependency?", ["NO", "YES"], horizontal=True)
    if has_dep_zld == "YES":
        dep_zld_df = pd.DataFrame([{"Project": "", "Component/PO Required": ""}])
        edited_zld_dep = st.data_editor(dep_zld_df, num_rows="dynamic", use_container_width=True, key="zld_dep_table")

    with st.form("zld_form"):
        st.subheader("Enquiry & Design Status")
        st.write("📝 **Current Enquiries & Design Load**")
        # Allows multiple enquiries to be entered
        zld_enq_df = pd.DataFrame([{"Client/Enquiry": "", "Offer Status": "Pending", "Design Stage": "Initial"}])
        zld_enq_data = st.data_editor(zld_enq_df, num_rows="dynamic", use_container_width=True, key="zld_enq_table")

        st.subheader("Project Execution & Schedule Risks")
        st.write("🏗️ **Active Projects Tracking**")
        # Allows entering multiple projects with their specific stages and risks
        zld_proj_df = pd.DataFrame([{
            "Project Name": "150 KLD MEE-MSN", 
            "Current Stage": "Fabrication", 
            "Schedule Risk": "NO",
            "Risk/Bottleneck Details": ""
        }])
        zld_proj_data = st.data_editor(zld_proj_df, num_rows="dynamic", use_container_width=True, key="zld_proj_table")

        updates = st.text_area("'UPDATES' (Major Site Events)")
        
        st.subheader("Management & Decisions")
        f_dec_z = st.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det_z = st.text_input("Decision Details")

        if st.form_submit_button("Sync ZLD Report"):
            st.success("Ammu's ZLD Report successfully synced.")

# --- 3. PURCHASE (SANTHOSHI) ---
elif role == "Purchase (Santhoshi)":
    st.header("Purchase & Operations Entry - Santhoshi")
    with st.form("purchase_form"):
        p1, p2 = st.columns(2)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        
        st.subheader("Operations Status")
        p4, p5 = st.columns(2)
        crit_machines = p4.text_input("Critical Machines Status")
        downtime = p5.text_input("Breakdown / Downtime")
        
        if st.form_submit_button("Sync Purchase Log"):
            st.success("Santhoshi's Operations Log Updated.")

# --- 4. MANAGEMENT DASHBOARD ---
else:
    st.header("B&G Management Analytics")
    st.info("Consolidated View of ZLD Projects and API Deviations.")
    # Here we would eventually load the CSVs and show the combined tables
    st.write("Awaiting data sync from anchors...")
