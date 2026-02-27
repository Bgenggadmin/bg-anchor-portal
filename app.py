import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="B&G Digital Portal", layout="wide", initial_sidebar_state="expanded")

# Define India Standard Time for the 5:30 PM Nudge
IST = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(IST)
current_time = now_ist.time()

# --- STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_value=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
st.sidebar.subheader("Digital Reporting System")

role = st.sidebar.radio("Identify Your Role:", 
    ["API Anchor (Kishore)", "ZLD Anchor (Ammu)", "Purchase & Ops (Santhoshi)", "Founder Dashboard"])

# --- 5:30 PM NOTIFICATION LOGIC ---
reporting_window_start = datetime.strptime("17:30", "%H:%M").time()
if current_time >= reporting_window_start:
    st.sidebar.warning("⏰ **EOD NOTICE:** It is past 5:30 PM. Please ensure your daily report is submitted before closing work.")

st.divider()

# --- ROLE-BASED INTERFACE ---

# 1. TECHNICAL ANCHORS (Kishore & Ammu)
if role in ["API Anchor (Kishore)", "ZLD Anchor (Ammu)"]:
    st.header(f"Daily Site Report: {role}")
    
    with st.form("site_entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            project = st.selectbox("Project / Site Name", 
                ["30KL OIL SYSTEM", "MSN REACTORS", "DIVIS UNIT-II", "10 KL KETTLE", "Other"])
            stage = st.text_input("Current Stage of Work", placeholder="e.g., Fabrication, Testing")
        
        with col2:
            manpower = st.number_input("Manpower on Site Today", min_value=0, step=1)
            critical_need = st.text_area("Critical Purchase Dependency", 
                placeholder="List items needed from Santhoshi (e.g., Centrifugal Pumps, Gaskets)")

        decision_req = st.toggle("Founder Decision Required?", help="Switch ON if you need a direct decision from the owner.")
        
        submit = st.form_submit_button("Sync Report to Master Log")
        if submit:
            st.success(f"✅ Report for {project} has been recorded. Data is now visible to Purchase & Management.")

# 2. PURCHASE & OPS (Santhoshi)
elif role == "Purchase & Ops (Santhoshi)":
    st.header("Purchase & Operations Control")
    
    # Cross-Functional Visibility: See what Tech Anchors need
    st.subheader("⚠️ Pending Technical Dependencies")
    # Mock data representation of the "Bridge"
    pending_data = pd.DataFrame({
        "Date": [now_ist.strftime("%d-%m-%Y")],
        "From": ["Ammu (ZLD)"],
        "Project": ["30KL OIL SYSTEM"],
        "Dependency": ["Centrifugal Pumps PO Pending"]
    })
    st.table(pending_data)

    with st.expander("Update Purchase Status & Manpower"):
        actual_mp = st.number_input("Total B&G Manpower (Combined)", value=62)
        purchase_update = st.text_input("Enter Status Update for Tech Anchors")
        if st.button("Update System"):
            st.info("Status updated for all site anchors.")

# 3. FOUNDER DASHBOARD
elif role == "Founder Dashboard":
    st.header("B&G Management Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Daily Summary", "Weekly Trends", "Critical Decisions"])
    
    with tab1:
        st.subheader("Today's Site Overview")
        # Visual representation of the Master Log
        st.info("All 3 Anchors have reported for today.")
        
    with tab2:
        st.subheader("Manpower & Progress Trends")
        st.line_chart({"Manpower": [55, 58, 62, 60, 62, 65]})
        
    with tab3:
        st.subheader("Red-Flagged for Decision")
        st.warning("MSN REACTORS: Decision required on Material Grade change.")

    # REPLACING EXCEL: Download Button
    st.divider()
    st.download_button(
        label="📥 Download Full Master Log (Excel/CSV)",
        data="Date,Project,Anchor,Status\n2026-02-27,MSN,Kishore,Complete",
        file_name=f"BG_Master_Report_{now_ist.date()}.csv",
        mime="text/csv"
    )

# --- FOOTER ---
st.sidebar.markdown(f"""
---
**Status:** Connected  
**Last Sync:** {now_ist.strftime('%H:%M:%S')} IST
""")
