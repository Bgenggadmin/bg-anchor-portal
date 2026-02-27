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

# --- 2. GITHUB ENGINES ---
def sync_data_to_github(repo_name, file_name, new_data_df, anchor_name):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(f"Bgenggadmin/{repo_name}")
        file_contents = repo.get_contents(file_name)
        existing_data = pd.read_csv(io.StringIO(file_contents.decoded_content.decode()))
        
        new_data_df['Timestamp'] = datetime.now(IST).strftime("%Y-%m-%d %H:%M")
        new_data_df['Anchor'] = anchor_name
        
        updated_df = pd.concat([existing_data, new_data_df], ignore_index=True)
        repo.update_file(
            path=file_contents.path,
            message=f"Update from {anchor_name}",
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

# --- 3. SIDEBAR ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

st.divider()

# --- 4. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore")
    
    # Tables for entry
    api_eng_data = st.data_editor(pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0}]), num_rows="dynamic", key="api_eng")

    if st.button("🚀 Sync API Master Report"):
        valid_data = api_eng_data[api_eng_data["Job"] != ""]
        if not valid_data.empty:
            if sync_data_to_github("bg-api-logs", "engineering_audit.csv", valid_data, "Kishore"):
                st.success("Data Synced!")
                st.rerun() # This clears the cells automatically

# --- 5. ROLE: ZLD (AMMU) ---
elif role == "ZLD (Ammu)":
    st.header("💧 ZLD Site Entry - Ammu")
    zld_proj_data = st.data_editor(pd.DataFrame([{"Project": "", "Stage": "", "Risk": "NO"}]), num_rows="dynamic", key="zld_proj")

    if st.button("Sync ZLD Report"):
        valid_zld = zld_proj_data[zld_proj_data["Project"] != ""]
        if not valid_zld.empty:
            if sync_data_to_github("bg-zld-logs", "project_execution.csv", valid_zld, "Ammu"):
                st.success("ZLD Data Synced!")
                st.rerun() # Clears form

# --- 6. ROLE: PURCHASE ---
elif role == "Purchase (Santhoshi)":
    st.header("📦 Purchase & Ops - Santhoshi")
    # Add your manpower/ops fields here
    if st.button("Sync Purchase Log"):
        st.success("Log Synced!")
        st.rerun()

# --- 7. MANAGEMENT DASHBOARD (THE FIX) ---
else:
    st.header("📊 B&G Management Analytics")
    
    st.subheader("🏗️ Recent Engineering Logs")
    df_api = fetch_logs("bg-api-logs", "engineering_audit.csv")
    if not df_api.empty:
        st.dataframe(df_api.sort_values(by="Timestamp", ascending=False), use_container_width=True)
    else:
        st.info("No logs found in bg-api-logs/engineering_audit.csv")

    st.subheader("💧 Recent ZLD Project Status")
    df_zld = fetch_logs("bg-zld-logs", "project_execution.csv")
    if not df_zld.empty:
        st.dataframe(df_zld.sort_values(by="Timestamp", ascending=False), use_container_width=True)
