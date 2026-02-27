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

# --- 2. SESSION STATE FOR CLEARING CELLS ---
# This must come AFTER 'import streamlit as st'
if "sync_count" not in st.session_state:
    st.session_state.sync_count = 0

# --- 3. ENGINES: GITHUB SYNC & READER ---
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

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

st.divider()

# --- 5. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    
    # DYNAMIC KEY: This changes after sync to clear the table
    form_key = f"api_form_{st.session_state.sync_count}"
    
    st.subheader("🛠️ Technical & Manufacturing Progress")
    api_eng_data = st.data_editor(
        pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Priority": "High"}]), 
        num_rows="dynamic", 
        use_container_width=True, 
        key=form_key
    )

    if st.button("🚀 Sync API Master Report"):
        valid_data = api_eng_data[api_eng_data["Job"] != ""].copy()
        if not valid_data.empty:
            if sync_data_to_github("bg-api-logs", "engineering_audit.csv", valid_data, "Kishore"):
                st.success("✅ Data Synced Successfully!")
                # Increment count to change the key and clear cells
                st.session_state.sync_count += 1
                st.rerun() 
        else:
            st.warning("⚠️ Please enter data before syncing.")

# --- 6. MANAGEMENT DASHBOARD ---
elif role == "Management Dashboard":
    st.header("📊 B&G Management Analytics")
    df_api = fetch_logs("bg-api-logs", "engineering_audit.csv")
    if not df_api.empty:
        st.dataframe(df_api.sort_values(by="Timestamp", ascending=False), use_container_width=True)

# --- 7. GLOBAL SUMMARY TABLE (BOTTOM OF EVERY PAGE) ---
st.divider()
st.subheader("📋 Live Factory Overview (EOD Summary)")
summary_df = fetch_logs("bg-api-logs", "engineering_audit.csv")
if not summary_df.empty:
    st.dataframe(summary_df.sort_values(by="Timestamp", ascending=False).head(10), use_container_width=True)
else:
    st.info("No logs found. Please check your GITHUB_TOKEN if sync previously failed.")
