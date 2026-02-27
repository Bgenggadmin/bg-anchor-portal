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
# This must come BEFORE any widgets are created
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

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

st.divider()

# --- 5. ROLE: API (KISHORE) - FULL FIELDS RESTORED ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    sk = st.session_state.sync_count # Secret for clearing cells

    st.subheader("🔴 Critical Purchase Dependencies")
    api_dep_data = st.data_editor(pd.DataFrame([{"Project/Job": "", "Material Required": "", "Req_Date": "", "PO_Ref": "Pending", "Urgency": "High"}]), num_rows="dynamic", use_container_width=True, key=f"api_dep_{sk}")

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

    with st.form(f"api_mgmt_form_{sk}"):
        st.subheader("🧠 Management Decisions")
        c3, c4 = st.columns(2)
        f_dec = c3.selectbox("Founder Decision Required?", ["NO", "YES"], key=f"fdec_{sk}")
        dec_context = c4.text_area("Decision Context (Detailed)", key=f"ctxt_{sk}")

        if st.form_submit_button("🚀 Sync to Master Log"):
            valid_eng = api_eng_data[api_eng_data["Job"] != ""].copy()
            
            # Attaching form data to the table for the master log
            valid_eng["Founder_Decision"] = f_dec
            valid_eng["Decision_Details"] = dec_context

            if not valid_eng.empty:
                if sync_to_master_log(valid_eng, "Kishore"):
                    st.success("✅ Synced! Refreshing...")
                    st.session_state.sync_count += 1
                    st.rerun()

# --- 6. ROLE: ZLD (AMMU) - FULL FIELDS ---
elif role == "ZLD (Ammu)":
    st.header("💧 ZLD Site Entry - Ammu Anchor")
    sk = st.session_state.sync_count

    zld_proj_data = st.data_editor(pd.DataFrame([{"Project Name": "", "Current Stage": "Fabrication", "Schedule Risk": "NO"}]), num_rows="dynamic", use_container_width=True, key=f"zld_proj_{sk}")

    if st.button("Sync ZLD Report"):
        valid_zld = zld_proj_data[zld_proj_data["Project Name"] != ""].copy()
        if not valid_zld.empty:
            if sync_to_master_log(valid_zld, "Ammu"):
                st.success("✅ ZLD Data Synced!")
                st.session_state.sync_count += 1
                st.rerun()

# --- 7. ROLE: PURCHASE (SANTHOSHI) - FULL FIELDS ---
elif role == "Purchase (Santhoshi)":
    st.header("📦 Purchase & Operations - Santhoshi")
    sk = st.session_state.sync_count
    planned = st.number_input("Planned Manpower", value=62, key=f"pman_{sk}")
    actual = st.number_input("Actual Manpower", value=52, key=f"aman_{sk}")
    
    if st.button("Sync Purchase Log"):
        # Create a dummy row for Santhoshi since she has numeric inputs
        pur_data = pd.DataFrame([{"Manpower_Planned": planned, "Manpower_Actual": actual}])
        if sync_to_master_log(pur_data, "Santhoshi"):
            st.success("✅ Log Synced!")
            st.session_state.sync_count += 1
            st.rerun()

# --- 8. MANAGEMENT DASHBOARD ---
else:
    st.header("📊 B&G Management Analytics")
    master_df = fetch_master_logs()
    if not master_df.empty:
        st.dataframe(master_df, use_container_width=True)

# --- 9. LIVE SUMMARY (BOTTOM - SHOWS ALL COLUMNS) ---
st.divider()
st.subheader("📋 Live Factory Overview (EOD Summary)")
summary_df = fetch_master_logs()

if not summary_df.empty:
    # Shows all columns in master_log.csv without filtering
    st.dataframe(summary_df.head(10), use_container_width=True)
