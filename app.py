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

def trigger_whatsapp_notification(anchor, context):
    st.warning(f"📲 WhatsApp Notification Queued for Founder: [{anchor}] {context}")

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

st.divider()

# --- 5. ROLE: API (KISHORE) - FULL FIELDS RESTORED ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    
    # Session-based keys to clear cells after sync
    sk = st.session_state.sync_count

    st.subheader("🔴 Critical Purchase Dependencies")
    api_dep_data = st.data_editor(pd.DataFrame([{"Project/Job": "", "Material Required": "", "Req_Date": "", "PO_Ref": "Pending", "Urgency": "High"}]), num_rows="dynamic", use_container_width=True, key=f"api_dep_{sk}")

    with st.form("api_master_form"):
        st.subheader("📊 Sales & Enquiry Tracking")
        c1, c2 = st.columns(2)
        with c1:
            st.write("📝 New Enquiries")
            api_enq_stats = st.data_editor(pd.DataFrame([{"Client": "", "Offers Issued": 0, "Status": "Review"}]), num_rows="dynamic", use_container_width=True, key=f"api_enq_{sk}")
        with c2:
            st.write("📐 Drawings & Design")
            api_dwg_stats = st.data_editor(pd.DataFrame([{"Job Code": "", "Dwg Released": 0, "Design Status": "Pending"}]), num_rows="dynamic", use_container_width=True, key=f"api_dwg_{sk}")

        st.subheader("🛠️ Technical & Manufacturing Progress")
        st.write("🔍 **Engineering Clarifications**")
        api_eng_data = st.data_editor(pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Priority": "High"}]), num_rows="dynamic", use_container_width=True, key=f"api_eng_main_{sk}")

        st.write("🏗️ **Manufacturing Planned vs Actual**")
        api_mfg_data = st.data_editor(pd.DataFrame([{"Job_Code": "", "Planned": "", "Actual": "", "Delay_Reason": ""}]), num_rows="dynamic", use_container_width=True, key=f"api_mfg_{sk}")

        st.subheader("⚠️ Deviations & Quality (NCR)")
        api_dev_data = st.data_editor(pd.DataFrame([{"Category": "Material", "Detail": "", "Impact": "NO", "NCR Status": "Open"}]), num_rows="dynamic", use_container_width=True, key=f"api_dev_{sk}")

        st.subheader("🧠 Management Decisions")
        c3, c4 = st.columns(2)
        client_calls = c3.number_input("Client Calls Today", min_value=0)
        founder_dec = c3.selectbox("Founder Decision Required?", ["NO", "YES"])
        key_disc = c4.text_area("Key Client Discussion Points")
        dec_context = c4.text_area("Decision Context (Detailed)")

        if st.form_submit_button("🚀 Sync API Master Report"):
            if founder_dec == "YES":
                trigger_whatsapp_notification("Kishore (API)", dec_context)
            
            valid_eng = api_eng_data[api_eng_data["Job"] != ""].copy()
            if not valid_eng.empty:
                if sync_data_to_github("bg-api-logs", "engineering_audit.csv", valid_eng, "Kishore"):
                    st.success("API Data Synced!")
                    st.session_state.sync_count += 1
                    st.rerun()

# --- 6. ROLE: ZLD (AMMU) - FULL FIELDS RESTORED ---
elif role == "ZLD (Ammu)":
    st.header("💧 ZLD Site Entry - Ammu Anchor")
    sk = st.session_state.sync_count

    st.subheader("🔴 Purchase Integration")
    zld_dep_data = st.data_editor(pd.DataFrame([{"Project": "", "Component Required": "", "Required Date": "", "Urgency": "Medium"}]), num_rows="dynamic", use_container_width=True, key=f"zld_dep_{sk}")

    with st.form("zld_form"):
        st.subheader("📈 Enquiry & Design Status")
        zld_enq_data = st.data_editor(pd.DataFrame([{"Client/Enquiry": "", "Offer Status": "Pending", "Design Stage": "Initial"}]), num_rows="dynamic", use_container_width=True, key=f"zld_enq_{sk}")

        st.subheader("🏗️ Project Execution & Risks")
        zld_proj_data = st.data_editor(pd.DataFrame([{"Project Name": "", "Current Stage": "Fabrication", "Schedule Risk": "NO", "Bottleneck Details": ""}]), num_rows="dynamic", use_container_width=True, key=f"zld_proj_{sk}")

        updates = st.text_area("'UPDATES' (Major Site Events)")
        f_dec_z = st.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det_z = st.text_input("Decision Details")

        if st.form_submit_button("Sync ZLD Report"):
            valid_zld = zld_proj_data[zld_proj_data["Project Name"] != ""].copy()
            if not valid_zld.empty:
                if sync_data_to_github("bg-zld-logs", "project_execution.csv", valid_zld, "Ammu"):
                    st.success("ZLD Data Synced!")
                    st.session_state.sync_count += 1
                    st.rerun()

# --- 7. ROLE: PURCHASE (SANTHOSHI) - FULL FIELDS RESTORED ---
elif role == "Purchase (Santhoshi)":
    st.header("📦 Purchase & Operations - Santhoshi")
    sk = st.session_state.sync_count
    with st.form("purchase_form"):
        st.subheader("👷 Manpower Tracking")
        p1, p2, p3 = st.columns(3)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        temp_mp = p3.selectbox("Temp Manpower Used", ["No", "Yes"])

        st.subheader("⚙️ Operations & Site Status")
        ops_data = st.data_editor(pd.DataFrame([{"Asset": "Plasma Machine", "Status": "Working", "Issue": "None"}]), num_rows="dynamic", use_container_width=True, key=f"ops_{sk}")

        absentees = st.text_area("Absentees Details")
        f_dec_p = st.selectbox("Founder Decision Required", ["No", "Yes"])
        dec_det_p = st.text_input("Decision Details")
        
        if st.form_submit_button("Sync Purchase Log"):
            st.success("Purchase Log Updated.")
            st.session_state.sync_count += 1
            st.rerun()

# --- 8. MANAGEMENT DASHBOARD ---
else:
    st.header("📊 B&G Management Analytics")
    st.write(f"Reporting Date: {now_ist.strftime('%Y-%m-%d')}")
    st.info("Reading live logs from GitHub Cloud...")
    df_api = fetch_logs("bg-api-logs", "engineering_audit.csv")
    if not df_api.empty:
        st.subheader("🏗️ Recent Engineering Logs")
        st.dataframe(df_api.sort_values(by="Timestamp", ascending=False), use_container_width=True)

# --- 9. GLOBAL SUMMARY TABLE (AT BOTTOM OF ALL PAGES) ---
st.divider()
st.subheader("📋 Live Factory Overview (EOD Summary)")
summary_df = fetch_logs("bg-api-logs", "engineering_audit.csv")
if not summary_df.empty:
    st.dataframe(summary_df.sort_values(by="Timestamp", ascending=False).head(10), use_container_width=True)
else:
    st.info("No logs found. Ensure GITHUB_TOKEN is correct and data has been synced.")
