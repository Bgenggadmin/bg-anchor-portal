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

# --- 2. SESSION STATE (FIXES NameError & CELL CLEARING) ---
if "sync_count" not in st.session_state:
    st.session_state.sync_count = 0

# --- 3. MASTER LOG ENGINES ---
def sync_to_master_log(new_data_df, anchor_name):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo("Bgenggadmin/bg-anchor-portal")
        
        # Add tracking metadata
        new_data_df['Date'] = datetime.now(IST).strftime("%Y-%m-%d")
        new_data_df['Timestamp'] = datetime.now(IST).strftime("%H:%M")
        new_data_df['Anchor'] = anchor_name

        file_contents = repo.get_contents("master_log.csv")
        existing_data = pd.read_csv(io.StringIO(file_contents.decoded_content.decode()))
        
        # Merge new data at the top
        updated_df = pd.concat([new_data_df, existing_data], ignore_index=True)
        
        repo.update_file(
            path="master_log.csv",
            message=f"Sync from {anchor_name}",
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

# --- 5. ROLE: API (KISHORE) - ALL FIELDS & AUTO-CLEAR ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    
    # DYNAMIC KEY: Changes after every sync to force-clear all cells
    sk = st.session_state.sync_count 

    st.subheader("🛠️ Technical & Manufacturing Progress")
    api_eng_data = st.data_editor(
        pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Priority": "High"}]), 
        num_rows="dynamic", use_container_width=True, key=f"api_table_{sk}"
    )

    with st.form(f"api_form_{sk}"):
        st.subheader("🧠 Management Decisions")
        c1, c2 = st.columns(2)
        f_dec = c1.selectbox("Founder Decision Required?", ["NO", "YES"], key=f"fdec_{sk}")
        dec_context = c2.text_area("Decision Context (Detailed)", key=f"ctxt_{sk}")

        if st.form_submit_button("🚀 Sync to Master Log"):
            valid_eng = api_eng_data[api_eng_data["Job"] != ""].copy()
            
            # Combine decision details into the data for the CSV
            valid_eng["Founder_Decision"] = f_dec
            valid_eng["Decision_Details"] = dec_context

            if not valid_eng.empty:
                if sync_to_master_log(valid_eng, "Kishore"):
                    st.success("✅ Synced Successfully! Resetting Form...")
                    # Incrementing the count changes all keys, making cells go blank
                    st.session_state.sync_count += 1
                    st.rerun()

# --- 6. MANAGEMENT DASHBOARD ---
elif role == "Management Dashboard":
    st.header("📊 B&G Management Analytics")
    master_df = fetch_master_logs()
    if not master_df.empty:
        st.dataframe(master_df, use_container_width=True)

# --- 7. LIVE SUMMARY (BOTTOM - SHOWS ALL COLUMNS) ---
st.divider()
st.subheader("📋 Live Factory Overview (EOD Summary)")
summary_df = fetch_master_logs()

if not summary_df.empty:
    # We no longer filter columns; this shows EVERYTHING in the master log
    st.dataframe(summary_df.head(10), use_container_width=True)
else:
    st.info("No logs found. Please sync data to view the summary.")
