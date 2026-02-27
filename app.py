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

# --- 1. KISHORE (API) - REFINED & OPTIMIZED ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")

    # Critical Purchase Integration (The "Trigger" for Santhoshi)
    st.subheader("🔴 Critical Purchase Dependencies")
    # Added Required Date and PO Ref for better integration
    api_dep_df = pd.DataFrame([{
        "Project/Job": "", 
        "Material Required": "", 
        "Required by Date": "", 
        "PO/PR Ref": "Pending",
        "Urgency": "High"
    }])
    api_dep_data = st.data_editor(api_dep_df, num_rows="dynamic", use_container_width=True, key="api_dep_table")

    with st.form("api_master_form"):
        # Section A: Sales & Offers
        st.subheader("📊 Sales & Enquiry Tracking")
        c1, c2 = st.columns(2)
        with c1:
            st.write("📝 New Enquiries & Offers")
            enq_df = pd.DataFrame([{"Client": "", "Offers Issued": 0, "Offer Status": "Review"}])
            api_enq_stats = st.data_editor(enq_df, num_rows="dynamic", use_container_width=True, key="api_enq")
        with c2:
            st.write("📐 Drawings & Design Status")
            dwg_df = pd.DataFrame([{"Job Code": "", "Dwg Released": 0, "Design Status": "Pending"}])
            api_dwg_stats = st.data_editor(dwg_df, num_rows="dynamic", use_container_width=True, key="api_dwg")

        # Section B: Technical & Manufacturing (MULTI-ROW)
        st.subheader("🛠️ Technical & Manufacturing Progress")
        st.write("🔍 **Engineering Clarifications Pending**")
        eng_df = pd.DataFrame([{"Job/Project": "", "Clarification Needed": "", "Ageing (Days)": 0, "Priority": "High"}])
        api_eng_data = st.data_editor(eng_df, num_rows="dynamic", use_container_width=True, key="api_eng")

        st.write("🏗️ **Manufacturing Planned vs Actual**")
        mfg_df = pd.DataFrame([{"Job Code": "", "Planned Activity": "", "Actual Status": "In Progress", "Delay Reason": ""}])
        api_mfg_data = st.data_editor(mfg_df, num_rows="dynamic", use_container_width=True, key="api_mfg")

        # Section C: Deviations & NCR (MULTI-ROW)
        st.subheader("⚠️ Deviations & Quality (NCR)")
        dev_df = pd.DataFrame([{"Category": "Material", "Detail": "", "Impact": "NO", "NCR Status": "Open"}])
        api_dev_data = st.data_editor(dev_df, num_rows="dynamic", use_container_width=True, key="api_dev")

        # Section D: Decisions
        st.subheader("🧠 Management & Decisions")
        c3, c4 = st.columns(2)
        with c3:
            client_calls = st.number_input("Client Calls Today", min_value=0)
            founder_dec = st.selectbox("Founder Decision Required?", ["NO", "YES"])
        with c4:
            key_disc = st.text_area("Key Client Discussion Points")
            dec_context = st.text_area("Decision Context (If YES above)")

        if st.form_submit_button("🚀 Sync API Master Report"):
            st.success("API Data Prepared for Sync.")

# --- 2. AMMU (ZLD) - REFINED FOR PROJECT EXECUTION ---
elif role == "ZLD (Ammu)":
    st.header("💧 ZLD Site Entry - Ammu Anchor")

    st.subheader("🔴 Purchase Integration")
    zld_dep_df = pd.DataFrame([{"Project": "", "Component Required": "", "Required Date": "", "Urgency": "Medium"}])
    zld_dep_data = st.data_editor(zld_dep_df, num_rows="dynamic", use_container_width=True, key="zld_dep")

    with st.form("zld_form"):
        st.subheader("📈 Enquiry & Design Status")
        zld_enq_df = pd.DataFrame([{"Client/Enquiry": "", "Offer Status": "Pending", "Design Stage": "Initial"}])
        zld_enq_data = st.data_editor(zld_enq_df, num_rows="dynamic", use_container_width=True, key="zld_enq")

        st.subheader("🏗️ Project Execution & Risks")
        zld_proj_df = pd.DataFrame([{
            "Project Name": "", 
            "Current Stage": "Fabrication", 
            "Schedule Risk": "NO",
            "Bottleneck Details": ""
        }])
        zld_proj_data = st.data_editor(zld_proj_df, num_rows="dynamic", use_container_width=True, key="zld_proj")

        updates = st.text_area("'UPDATES' (Major Site Events)")
        
        c5, c6 = st.columns(2)
        f_dec_z = c5.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det_z = c6.text_input("Decision Details")

        if st.form_submit_button("Sync ZLD Report"):
            st.success("Ammu's ZLD Report successfully synced.")

# --- 3. SANTHOSHI (PURCHASE) - REFINED OPERATIONS ---
elif role == "Purchase (Santhoshi)":
    st.header("📦 Purchase & Operations - Santhoshi")
    
    # NEW: Live Dependency Feed (In a real app, this pulls from the CSVs)
    st.warning("🔔 Check Management Dashboard for High-Priority Project Dependencies flagged by Technical Anchors.")

    with st.form("purchase_form"):
        st.subheader("👷 Manpower Tracking")
        p1, p2, p3 = st.columns(3)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        temp_mp = p3.selectbox("Temp Manpower Used", ["No", "Yes"])

        st.subheader("⚙️ Operations & Site Status")
        st.write("📊 **Machine & Transport Status**")
        ops_df = pd.DataFrame([{"Asset/Service": "Plasma Machine", "Status": "Working", "Issue/Downtime": "None"}])
        ops_data = st.data_editor(ops_df, num_rows="dynamic", use_container_width=True, key="ops_table")

        absentees = st.text_area("Absentees Details (List names if any)")

        st.subheader("🧠 Management & Decisions")
        f_dec_p = st.selectbox("Founder Decision Required", ["No", "Yes"])
        dec_det_p = st.text_input("Decision Details")
        
        if st.form_submit_button("Sync Purchase Log"):
            st.success("Santhoshi's Operations Log Updated.")

# --- 4. MANAGEMENT DASHBOARD ---
else:
    st.header("📊 B&G Management Analytics")
    st.write(f"Reporting Date: {now_ist.strftime('%Y-%m-%d')}")
    
    st.info("Consolidated View: Project Risks, Engineering Bottlenecks, and Purchase Status.")
    # Placeholders for future data tables
    st.write("---")
    st.button("📥 Download Master EOD Report (Excel)")
