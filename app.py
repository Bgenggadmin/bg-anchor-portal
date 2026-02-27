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

# --- 2. SESSION STATE (Prevents NameError) ---
if "sync_count" not in st.session_state:
    st.session_state.sync_count = 0

# --- 3. MASTER SYNC ENGINE ---
def sync_to_master_log(new_data_df, anchor_name):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        # Using your existing repository name
        repo = g.get_repo("Bgenggadmin/bg-anchor-portal")
        
        # Metadata for the master record
        new_data_df['Date'] = datetime.now(IST).strftime("%Y-%m-%d")
        new_data_df['Timestamp'] = datetime.now(IST).strftime("%H:%M")
        new_data_df['Anchor'] = anchor_name

        # Get existing master_log.csv
        file_contents = repo.get_contents("master_log.csv")
        existing_data = pd.read_csv(io.StringIO(file_contents.decoded_content.decode()))
        
        # Merge new entries at the top
        updated_df = pd.concat([new_data_df, existing_data], ignore_index=True)
        
        repo.update_file(
            path="master_log.csv",
            message=f"Update from {anchor_name}",
            content=updated_df.to_csv(index=False),
            sha=file_contents.sha
        )
        return True
    except Exception as e:
        st.error(f"Sync Failed: {e}")
        return False

def fetch_master_logs():
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo("Bgenggadmin/bg-anchor-portal")
        contents = repo.get_contents("master_log.csv")
        return pd.read_csv(io.StringIO(contents.decoded_content.decode()))
    except:
        return pd.DataFrame()

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

st.divider()

# --- 5. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    # Dynamic key reset to clear cells after sync
    sk = st.session_state.sync_count 

    # Restore all your original data editor fields
    api_eng_data = st.data_editor(
        pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Priority": "High"}]), 
        num_rows="dynamic", use_container_width=True, key=f"api_eng_{sk}"
    )

    if st.button("🚀 Sync to Master Log"):
        valid_data = api_eng_data[api_eng_data["Job"] != ""].copy()
        if not valid_data.empty:
            if sync_to_master_log(valid_data, "Kishore"):
                st.success("✅ Synced to Master Log!")
                st.session_state.sync_count += 1
                st.rerun()

# --- 6. MANAGEMENT DASHBOARD ---
elif role == "Management Dashboard":
    st.header("📊 B&G Management Analytics")
    master_df = fetch_master_logs()
    if not master_df.empty:
        st.dataframe(master_df, use_container_width=True)

# --- 7. LIVE SUMMARY (BOTTOM OF ALL PAGES) ---
st.divider()
st.subheader("📋 Live Factory Overview (EOD Summary)")
summary_df = fetch_master_logs()
if not summary_df.empty:
    # Showing the latest entries at the bottom as requested
    st.dataframe(summary_df.head(10), use_container_width=True)
