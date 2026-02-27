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
        
        new_data_df['Timestamp'] = datetime.now(IST).strftime("%Y-%m-%d %H:%M")
        new_data_df['Anchor'] = anchor_name
        
        updated_df = pd.concat([existing_data, new_data_df], ignore_index=True)
        repo.update_file(
            path=file_contents.path,
            message=f"Update from {anchor_name} - {datetime.now(IST).strftime('%Y-%m-%d')}",
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
    
    # Critical Purchase Integration
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
        st.write("🔍 **Engineering Clarifications**")
        eng_df = pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Priority": "High"}])
        api_eng_data = st.data_editor(eng_df, num_rows="dynamic", use_container_width=True, key="api_eng")

        st.write("🏗️ **Manufacturing Planned vs Actual**")
        mfg_df = pd.DataFrame([{"Job_Code": "", "Planned": "", "Actual": "", "Delay_Reason": ""}])
        api_mfg_data = st.data_editor(mfg_df, num_rows="dynamic", use_container_width=True, key="api_mfg")

        st.subheader("⚠️ Deviations & Quality (NCR)")
        dev_df = pd.DataFrame([{"Category": "Material", "Detail": "", "Impact": "NO", "NCR Status": "Open"}])
        api_dev_data = st.data_editor(dev_df, num_rows="dynamic", use_container_width=True, key="api_dev")

        st.subheader("🧠 Management Decisions")
        c3, c4 = st.columns(2)
        client_calls = c3.number_input("Client Calls Today", min_value=0)
        founder_dec = c3.selectbox("Founder Decision Required?", ["NO", "YES"])
        key_disc = c4.text_area("Key Client Discussion Points")
        dec_context = c4.text_area("Decision Context (Detailed)")

        if st.form_submit_button("🚀 Sync API Master Report"):
            if founder_dec == "YES":
                trigger_whatsapp_notification("Kishore (API)", dec_context)
            
            # Sync Engineering Logic
            valid_eng = api_eng_data[api_eng_data["Job"] != ""]
            if not valid_eng.empty:
                sync_data_to_github("bg-api-logs", "engineering_audit.csv", valid_eng, "Kishore")
            
            st.success("API Report Synced!")
            st.rerun() # This clears the cells after success

# --- 5. ROLE: ZLD (AMMU) ---
elif role == "ZLD (Ammu)":
    st.header("💧 ZLD Site Entry - Ammu Anchor")
    st.subheader("🔴 Purchase Integration")
    zld_dep_df = pd.DataFrame([{"Project": "", "Component Required": "", "Required Date": "", "Urgency": "Medium"}])
    zld_dep_data = st.data_editor(zld_dep_df, num_rows="dynamic", use_container_width=True, key="zld_dep")

    with st.form("zld_form"):
        st.subheader("📈 Enquiry & Design Status")
        zld_enq_df = pd.DataFrame([{"Client/Enquiry": "", "Offer Status": "Pending", "Design Stage": "Initial"}])
        zld_enq_data = st.data_editor(zld_enq_df, num_rows="dynamic", use_container_width=True, key="zld_enq")

        st.subheader("🏗️ Project Execution & Risks")
        zld_proj_df = pd.DataFrame([{"Project Name": "", "Current Stage": "Fabrication", "Schedule Risk": "NO", "Bottleneck Details": ""}])
        zld_proj_data = st.data_editor(zld_proj_df, num_rows="dynamic", use_container_width=True, key="zld_proj")

        updates = st.text_area("'UPDATES' (Major Site Events)")
        f_dec_z = st.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det_z = st.text_input("Decision Details")

        if st.form_submit_button("Sync ZLD Report"):
            valid_zld = zld_proj_data[zld_proj_data["Project Name"] != ""]
            if not valid_zld.empty:
                sync_data_to_github("bg-zld-logs", "project_execution.csv", valid_zld, "Ammu")
            st.success("ZLD Data Synced!")
            st.rerun()

# --- 6. ROLE: PURCHASE (SANTHOSHI) ---
elif role == "Purchase (Santhoshi)":
    st.header("📦 Purchase & Operations - Santhoshi")
    with st.form("purchase_form"):
        st.subheader("👷 Manpower Tracking")
        p1, p2, p3 = st.columns(3)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        temp_mp = p3.selectbox("Temp Manpower Used", ["No", "Yes"])

        st.subheader("⚙️ Operations & Site Status")
        ops_df = pd.DataFrame([{"Asset": "Plasma Machine", "Status": "Working", "Issue": "None"}])
        ops_data = st.data_editor(ops_df, num_rows="dynamic", use_container_width=True, key="ops_table")

        absentees = st.text_area("Absentees Details")
        f_dec_p = st.selectbox("Founder Decision Required", ["No", "Yes"])
        dec_det_p = st.text_input("Decision Details")
        
        if st.form_submit_button("Sync Purchase Log"):
            st.success("Operations Log Updated.")
            st.rerun()

# --- 7. MANAGEMENT DASHBOARD ---
else:
    st.header("📊 B&G Management Analytics")
    st.write(f"Reporting Date: {now_ist.strftime('%Y-%m-%d')}")
    
    st.subheader("🏗️ API Engineering Logs")
    df_api = fetch_logs("bg-api-logs", "engineering_audit.csv")
    if not df_api.empty:
        st.dataframe(df_api.sort_values(by="Timestamp", ascending=False), use_container_width=True)
    
    st.subheader("💧 ZLD Project Status")
    df_zld = fetch_logs("bg-zld-logs", "project_execution.csv")
    if not df_zld.empty:
        st.dataframe(df_zld.sort_values(by="Timestamp", ascending=False), use_container_width=True)

    st.divider()
    st.button("📥 Download Master EOD Report (Excel)")

# --- 8. GLOBAL SUMMARY TABLE (SHOWS AT BOTTOM OF ALL PAGES) ---
st.divider()
st.subheader("📋 Live Factory Overview (EOD Summary)")
all_api = fetch_logs("bg-api-logs", "engineering_audit.csv")
if not all_api.empty:
    st.write("**Recent Engineering Clarifications:**")
    st.dataframe(all_api.tail(5), use_container_width=True)
