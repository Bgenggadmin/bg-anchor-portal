import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
from github import Github
import io
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="B&G Digital Portal", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(IST)

# --- 2. GITHUB SYNC ENGINE ---
def sync_data_to_github(repo_name, file_name, new_data_df, anchor_name):
    try:
        # Connect using Secrets
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(f"Bgenggadmin/{repo_name}")
        
        # Get existing file
        file_contents = repo.get_contents(file_name)
        existing_data = pd.read_csv(io.StringIO(file_contents.decoded_content.decode()))
        
        # Add metadata
        new_data_df['Timestamp'] = datetime.now(IST).strftime("%Y-%m-%d %H:%M")
        new_data_df['Submitted_By'] = anchor_name
        
        # Merge and Push
        updated_df = pd.concat([existing_data, new_data_df], ignore_index=True)
        repo.update_file(
            path=file_contents.path,
            message=f"EOD Update from {anchor_name} - {datetime.now(IST).strftime('%Y-%m-%d')}",
            content=updated_df.to_csv(index=False),
            sha=file_contents.sha
        )
        return True
    except Exception as e:
        st.error(f"Sync Failed for {file_name}: {e}")
        return False

# --- 3. WHATSAPP NOTIFICATION HELPER ---
def trigger_founder_alert(anchor, context):
    # This uses a generic Webhook/API approach (e.g., UltraMsg or Twilio)
    # For now, it logs the alert; we can link your API key here
    alert_msg = f"🚨 *B&G FOUNDER ALERT*\nAnchor: {anchor}\nContext: {context}\nTime: {datetime.now(IST).strftime('%H:%M')}"
    st.warning("📲 WhatsApp Notification Sent to Founder.")
    # Example: requests.post(st.secrets["WHATSAPP_URL"], data={"msg": alert_msg})

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

st.divider()

# --- 5. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")

    # Critical Purchase Integration
    st.subheader("🔴 Critical Purchase Dependencies")
    api_dep_df = pd.DataFrame([{"Project/Job": "", "Material": "", "Req_Date": "", "Priority": "High"}])
    api_dep_data = st.data_editor(api_dep_df, num_rows="dynamic", use_container_width=True, key="api_dep")

    with st.form("api_master_form"):
        st.subheader("📊 Technical & Manufacturing Progress")
        
        st.write("🔍 **Engineering Clarifications**")
        eng_df = pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0}])
        api_eng_data = st.data_editor(eng_df, num_rows="dynamic", use_container_width=True, key="api_eng")

        st.write("🏗️ **Manufacturing Status**")
        mfg_df = pd.DataFrame([{"Job_Code": "", "Planned": "", "Actual": "", "Delay_Reason": ""}])
        api_mfg_data = st.data_editor(mfg_df, num_rows="dynamic", use_container_width=True, key="api_mfg")

        st.subheader("🧠 Management Decisions")
        c1, c2 = st.columns(2)
        f_dec = c1.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = c2.text_area("Decision Context / Details")

        if st.form_submit_button("🚀 Sync API Master Report"):
            # A. Trigger Alert if YES
            if f_dec == "YES":
                trigger_founder_alert("Kishore (API)", dec_context)

            # B. Sync Tables
            success_count = 0
            # Clean and Sync Engineering Table
            valid_eng = api_eng_data[api_eng_data["Job"] != ""]
            if not valid_eng.empty:
                if sync_data_to_github("bg-api-logs", "engineering_audit.csv", valid_eng, "Kishore"):
                    success_count += 1
            
            # Clean and Sync Purchase Dependencies
            valid_dep = api_dep_data[api_dep_data["Project/Job"] != ""]
            if not valid_dep.empty:
                if sync_data_to_github("bg-purchase-master", "dependencies.csv", valid_dep, "Kishore"):
                    success_count += 1

            if success_count > 0:
                st.success(f"✅ {success_count} Tables Synced to GitHub.")
                st.balloons()

# --- 6. ROLE: ZLD (AMMU) ---
elif role == "ZLD (Ammu)":
    st.header("💧 ZLD Site Entry - Ammu Anchor")
    # (Similar structure for ZLD with sync_data_to_github calls)
    # ... code for ZLD tables ...
    st.info("ZLD Module Ready for Sync.")

# --- 7. MANAGEMENT DASHBOARD ---
else:
    st.header("📊 B&G Management Analytics")
    st.write(f"Data Refresh: {now_ist.strftime('%Y-%m-%d %H:%M')}")
    # Here we would use pd.read_csv from GitHub to show your total logs
    st.info("Management Dashboard will pull latest data from engineering_audit.csv and dependencies.csv")
