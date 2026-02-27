import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIG ---
IST = pytz.timezone('Asia/Kolkata')

# --- 1. KISHORE (API) - REFINED & OPTIMIZED ---
st.header("🏢 API Site Entry - Kishore Anchor")

# Instant Trigger for Purchase Integration
st.subheader("🔴 Critical Purchase Dependencies")
dep_df = pd.DataFrame([{"Project/Job": "", "Material Required": "", "Urgency": "Medium"}])
api_dep_data = st.data_editor(dep_df, num_rows="dynamic", use_container_width=True, key="api_dep_table")

with st.form("api_master_form"):
    # Section A: Sales & Offers
    st.subheader("📊 Sales & Enquiry Tracking")
    c1, c2 = st.columns(2)
    with c1:
        st.write("New Enquiries & Offers")
        enq_df = pd.DataFrame([{"Client": "", "Offers Issued": 0, "Offer Status": "Review"}])
        api_enq_stats = st.data_editor(enq_df, num_rows="dynamic", use_container_width=True)
    with c2:
        st.write("Offers > 7 Days & Drawing Status")
        dwg_df = pd.DataFrame([{"Job Code": "", "Dwg Released": 0, "Design Status": "Pending"}])
        api_dwg_stats = st.data_editor(dwg_df, num_rows="dynamic", use_container_width=True)

    st.divider()

    # Section B: Engineering & Manufacturing (NOW MULTI-ROW)
    st.subheader("🛠️ Technical & Manufacturing Progress")
    
    st.write("🔍 **Engineering Clarifications Pending**")
    eng_df = pd.DataFrame([{"Job/Project": "", "Clarification Needed": "", "Ageing (Days)": 0, "Priority": "High"}])
    api_eng_data = st.data_editor(eng_df, num_rows="dynamic", use_container_width=True)

    st.write("🏗️ **Manufacturing Planned vs Actual**")
    mfg_df = pd.DataFrame([{"Job Code": "", "Planned Activity": "", "Actual Status": "In Progress", "Delay Reason": ""}])
    api_mfg_data = st.data_editor(mfg_df, num_rows="dynamic", use_container_width=True)

    st.divider()

    # Section C: Deviations & NCR (NOW MULTI-ROW)
    st.subheader("⚠️ Deviations & Quality (NCR)")
    st.write("List all open Deviations or NCRs")
    dev_df = pd.DataFrame([{"Category": "Material", "Detail": "", "Impact": "NO", "NCR Status": "Open"}])
    api_dev_data = st.data_editor(dev_df, num_rows="dynamic", use_container_width=True)

    # Section D: Management Decisions
    st.subheader("🧠 Management & Decisions")
    c3, c4 = st.columns(2)
    with c3:
        client_calls = st.number_input("Client Calls Today", min_value=0)
        founder_dec = st.selectbox("Founder Decision Required?", ["NO", "YES"])
    with c4:
        key_disc = st.text_area("Key Client Discussion Points")
        dec_context = st.text_area("Decision Context (If YES above)")

    if st.form_submit_button("🚀 Sync API Master Report"):
        st.success("API Anchor Data Prepared for Sync.")
