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

# --- 2. SESSION STATE (FIXES EVERYTHING BREAKING) ---
if "sync_count" not in st.session_state:
    st.session_state.sync_count = 0

# --- 3. MASTER LOG ENGINES ---
def sync_to_master_log(new_data_df, anchor_name):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo("Bgenggadmin/bg-anchor-portal")
        
        # Add core tracking metadata
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

def trigger_whatsapp_alert(anchor, context):
    st.warning(f"📲 WhatsApp Notification Queued for Founder: [{anchor}] {context}")

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

st.divider()

# --- 5. ROLE: API (KISHORE) - ALL FIELDS RESTORED & CLEANED ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    sk = st.session_state.sync_count # Secret to clearing cells

    st.subheader("🔴 Critical Purchase Dependencies")
    api_dep_data = st.data_editor(pd.DataFrame([{"Project/Job": "", "Material Required": "", "Req_Date": "", "PO_Ref": "Pending", "Urgency": "High"}]), num_rows="dynamic", use_container_width=True, key=f"api_dep_{sk}")

    with st.form("api_master_form"):
        st.subheader("📊 Sales & Enquiry Tracking")
        c1, c2 = st.columns(2)
        with c1:
            st.write("📝 New Enquiries")
            api_enq = st.data_editor(pd.DataFrame([{"Client": "", "Offers Issued": 0, "Status": "Review"}]), num_rows="dynamic", use_container_width=True, key=f"api_enq_{sk}")
        with c2:
            st.write("📐 Drawings & Design")
            api_dwg = st.data_editor(pd.DataFrame([{"Job Code": "", "Dwg Released": 0, "Design Status": "Pending"}]), num_rows="dynamic", use_container_width=True, key=f"api_dwg_{sk}")

        st.subheader("🛠️ Technical & Manufacturing Progress")
        api_eng_data = st.data_editor(pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Priority": "High"}]), num_rows="dynamic", use_container_width=True, key=f"api_eng_{sk}")

        st.subheader("⚠️ Deviations & Quality (NCR)")
        api_dev_data = st.data_editor(pd.DataFrame([{"Category": "Material", "Detail": "", "Impact": "NO", "NCR Status": "Open"}]), num_rows="dynamic", use_container_width=True, key=f"api_dev_{sk}")

        st.subheader("🧠 Management Decisions")
        c3, c4 = st.columns(2)
        founder_dec = c3.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = c4.text_area("Decision Context (Detailed)")

        if st.form_submit_button("🚀 Sync to Master Log"):
            if founder_dec == "YES":
                trigger_whatsapp_alert("Kishore (API)", dec_context)
            
            # Filter main engineering data only
            valid_eng = api_eng_data[api_eng_data["Job"] != ""].copy()
            if not valid_eng.empty:
                if sync_to_master_log(valid_eng, "Kishore"):
                    st.success("✅ Synced! Clearing cells...")
                    st.session_state.sync_count += 1
                    st.rerun()

# --- 6. ROLE: ZLD (AMMU) ---
elif role == "ZLD (Ammu)":
    st.header("💧 ZLD Site Entry - Ammu Anchor")
    # ... code for ZLD fields ...

# --- 7. MANAGEMENT DASHBOARD ---
elif role == "Management Dashboard":
    st.header("📊 B&G Management Analytics")
    master_df = fetch_master_logs()
    if not master_df.empty:
        st.dataframe(master_df, use_container_width=True)

# --- 8. LIVE SUMMARY (BOTTOM - ONLY SHOWS RELEVANT API FIELDS) ---
st.divider()
st.subheader("📋 Live Factory Overview (EOD Summary)")
summary_df = fetch_master_logs()

if not summary_df.empty:
    # CLEANUP: Only show API-related columns if Kishore is logged in
    if role == "API (Kishore)":
        api_view = summary_df[summary_df["Anchor"] == "Kishore"]
        # Only show the columns Kishore needs
        cols_to_show = ["Job", "Clarification", "Ageing", "Priority", "Timestamp"]
        # Filter only existing columns from that list
        existing_cols = [c for c in cols_to_show if c in api_view.columns]
        st.dataframe(api_view[existing_cols].head(10), use_container_width=True)
    else:
        st.dataframe(summary_df.head(10), use_container_width=True)
