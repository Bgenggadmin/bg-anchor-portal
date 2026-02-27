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

# --- 2. SESSION STATE (FIXED NameError) ---
if "sync_count" not in st.session_state:
    st.session_state.sync_count = 0

# --- 3. ENGINES: AUTO-CREATE SYNC ---
def sync_data_to_github(repo_name, file_name, new_data_df, anchor_name):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(f"Bgenggadmin/{repo_name}")
        
        # Metadata
        new_data_df['Timestamp'] = datetime.now(IST).strftime("%Y-%m-%d %H:%M")
        new_data_df['Anchor'] = anchor_name

        try:
            # Try to get existing file
            file_contents = repo.get_contents(file_name)
            existing_data = pd.read_csv(io.StringIO(file_contents.decoded_content.decode()))
            updated_df = pd.concat([existing_data, new_data_df], ignore_index=True)
            
            repo.update_file(
                path=file_contents.path,
                message=f"Update: {anchor_name}",
                content=updated_df.to_csv(index=False),
                sha=file_contents.sha
            )
        except:
            # FILE DOES NOT EXIST - CREATE IT NEW
            st.info(f"Creating new file: {file_name}")
            repo.create_file(
                path=file_name,
                message=f"Initial Creation: {file_name}",
                content=new_data_df.to_csv(index=False)
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

# --- 4. SIDEBAR ---
role = st.sidebar.radio("Select Anchor Role:", ["API (Kishore)", "ZLD (Ammu)", "Management Dashboard"])

# --- 5. ROLE: API (KISHORE) - ALL FIELDS ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    sk = st.session_state.sync_count

    st.subheader("🔴 Critical Purchase Dependencies")
    api_dep_data = st.data_editor(pd.DataFrame([{"Project/Job": "", "Material Required": "", "Req_Date": "", "PO_Ref": "Pending", "Urgency": "High"}]), num_rows="dynamic", use_container_width=True, key=f"api_dep_{sk}")

    with st.form("api_master_form"):
        st.subheader("📊 Sales & Enquiry Tracking")
        api_enq_data = st.data_editor(pd.DataFrame([{"Client": "", "Offers Issued": 0, "Status": "Review"}]), num_rows="dynamic", use_container_width=True, key=f"api_enq_{sk}")
        
        st.subheader("🛠️ Technical & Manufacturing Progress")
        api_eng_data = st.data_editor(pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Priority": "High"}]), num_rows="dynamic", use_container_width=True, key=f"api_eng_main_{sk}")

        # Founder Decisions
        founder_dec = st.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = st.text_area("Decision Context")

        if st.form_submit_button("🚀 Sync All API Fields"):
            # Combine tables if you want one big CSV, or sync separately
            valid_eng = api_eng_data[api_eng_data["Job"] != ""].copy()
            if not valid_eng.empty:
                if sync_data_to_github("bg-api-logs", "engineering_audit.csv", valid_eng, "Kishore"):
                    st.success("✅ Sync Successful!")
                    st.session_state.sync_count += 1
                    st.rerun()

# --- 6. GLOBAL SUMMARY TABLE (BOTTOM) ---
st.divider()
st.subheader("📋 Live Factory Overview (EOD Summary)")
summary_df = fetch_logs("bg-api-logs", "engineering_audit.csv")
if not summary_df.empty:
    st.dataframe(summary_df.sort_values(by="Timestamp", ascending=False), use_container_width=True)
else:
    st.info("Waiting for first sync to create 'engineering_audit.csv'...")
