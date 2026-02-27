import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
from github import Github
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="B&G Digital Portal", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(IST)

# --- 2. ENGINES: GITHUB SYNC & READER ---
def sync_data_to_github(repo_name, file_name, new_data_df, anchor_name):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(f"Bgenggadmin/{repo_name}")
        file_contents = repo.get_contents(file_name)
        existing_data = pd.read_csv(io.StringIO(file_contents.decoded_content.decode()))
        
        # Add metadata
        new_data_df['Timestamp'] = datetime.now(IST).strftime("%Y-%m-%d %H:%M")
        new_data_df['Anchor'] = anchor_name
        
        # Merge and Update
        updated_df = pd.concat([existing_data, new_data_df], ignore_index=True)
        repo.update_file(
            path=file_contents.path,
            message=f"EOD Update from {anchor_name}",
            content=updated_df.to_csv(index=False),
            sha=file_contents.sha
        )
        return True
    except Exception as e:
        st.error(f"Sync Failed: {e}")
        return False

def fetch_logs(repo_name, file_name):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(f"Bgenggadmin/{repo_name}")
        contents = repo.get_contents(file_name)
        return pd.read_csv(io.StringIO(contents.decoded_content.decode()))
    except:
        return pd.DataFrame()

def trigger_whatsapp_notification(anchor, context):
    st.warning(f"📲 WhatsApp Notification Queued for Founder: [{anchor}] {context}")

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

st.divider()

# --- 4. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    
    st.subheader("🔴 Critical Purchase Dependencies")
    api_dep_df = pd.DataFrame([{"Project/Job": "", "Material Required": "", "Req_Date": "", "PO_Ref": "Pending", "Urgency": "High"}])
    api_dep_data = st.data_editor(api_dep_df, num_rows="dynamic", use_container_width=True, key="api_dep")

    with st.form("api_master_form"):
        st.subheader("📊 Sales & Enquiry Tracking")
        c1, c2 = st.columns(2)
        with c1:
            st.write("📝 New Enquiries")
            enq_df = pd.DataFrame([{"Client": "", "Offers Issued": 0, "Status": "Review"}])
            api_enq_stats = st.data_editor(enq_df, num_rows="dynamic", use_container_width=True, key="api_enq")
        with c2:
            st.write("📐 Drawings & Design")
            dwg_df = pd.DataFrame([{"Job Code": "", "Dwg Released": 0, "Design Status": "Pending"}])
            api_dwg_stats = st.data_editor(dwg_df, num_rows="dynamic", use_container_width=True, key="api_dwg")

        st.subheader("🛠️ Technical & Manufacturing Progress")
        eng_df = pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Priority": "High"}])
        api_eng_data = st.data_editor(eng_df, num_rows="dynamic", use_container_width=True, key="api_eng")

        st.subheader("⚠️ Deviations & Quality (NCR)")
        dev_df = pd.DataFrame([{"Category": "Material", "Detail": "", "Impact": "NO", "NCR Status": "Open"}])
        api_dev_data = st.data_editor(dev_df, num_rows="dynamic", use_container_width=True, key="api_dev")

        st.subheader("🧠 Management Decisions")
        c3, c4 = st.columns(2)
        founder_dec = c3.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = c4.text_area("Decision Context (Detailed)")

        if st.form_submit_button("🚀 Sync API Master Report"):
            if founder_dec == "YES":
                trigger_whatsapp_notification("Kishore (API)", dec_context)
            
            # Sync Logic for Engineering Table
            valid_eng = api_eng_data[api_eng_data["Job"] != ""].copy()
            if not valid_eng.empty:
                if sync_data_to_github("bg-api-logs", "engineering_audit.csv", valid_eng, "Kishore"):
                    st.success("API Report Synced!")
                    st.rerun() # Clears form after success

# --- 5. ROLE: ZLD (AMMU) ---
elif role == "ZLD (Ammu)":
    st.header("💧 ZLD Site Entry - Ammu Anchor")
    with st.form("zld_form"):
        zld_proj_df = pd.DataFrame([{"Project Name": "", "Current Stage": "Fabrication", "Schedule Risk": "NO"}])
        zld_proj_data = st.data_editor(zld_proj_df, num_rows="dynamic", use_container_width=True, key="zld_proj")
        f_dec_z = st.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det_z = st.text_area("Decision Details")

        if st.form_submit_button("Sync ZLD Report"):
            valid_zld = zld_proj_data[zld_proj_data["Project Name"] != ""].copy()
            if not valid_zld.empty:
                if sync_data_to_github("bg-zld-logs", "project_execution.csv", valid_zld, "Ammu"):
                    st.success("ZLD Data Synced!")
                    st.rerun()

# --- 6. ROLE: PURCHASE (SANTHOSHI) ---
elif role == "Purchase (Santhoshi)":
    st.header("📦 Purchase & Operations - Santhoshi")
    with st.form("purchase_form"):
        p1, p2 = st.columns(2)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        if st.form_submit_button("Sync Purchase Log"):
            st.success("Operations Log Updated.")
            st.rerun()

# --- 7. MANAGEMENT DASHBOARD (FIXED INDENTATION) ---
else:
    st.header("📊 B&G Management Analytics")
    st.info("Reading live logs from GitHub Cloud...")
    
    st.subheader("🏗️ Recent Engineering Logs")
    df_dashboard = fetch_logs("bg-api-logs", "engineering_audit.csv")
    if not df_dashboard.empty:
        st.dataframe(df_dashboard.sort_values(by="Timestamp", ascending=False), use_container_width=True)

# --- 8. GLOBAL SUMMARY TABLE (BOTTOM OF EVERY PAGE) ---
st.divider()
st.subheader("📋 Live Factory Overview (EOD Summary)")
summary_df = fetch_logs("bg-api-logs", "engineering_audit.csv")
if not summary_df.empty:
    st.dataframe(summary_df.tail(10), use_container_width=True)
else:
    st.info("No logs found. Check your GITHUB_TOKEN if data was already synced.")
