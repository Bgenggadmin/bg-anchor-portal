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

# --- 2. ENGINES: GITHUB SYNC & WHATSAPP ---
def sync_data_to_github(repo_name, file_name, new_data_df, anchor_name):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(f"Bgenggadmin/{repo_name}")
        
        # Get existing file content
        file_contents = repo.get_contents(file_name)
        existing_data = pd.read_csv(io.StringIO(file_contents.decoded_content.decode()))
        
        # Add timestamp and metadata
        new_data_df['Timestamp'] = datetime.now(IST).strftime("%Y-%m-%d %H:%M")
        new_data_df['Anchor'] = anchor_name
        
        # Merge and Update
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

def trigger_whatsapp_notification(anchor, context):
    # This is a placeholder for your WhatsApp API call
    # Logic: If Founder Decision == YES, trigger this
    st.warning(f"📲 WhatsApp Notification Queued for Founder: [{anchor}] {context}")

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

st.divider()

# --- 4. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")

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
            
            # Filter and Sync logic here
            st.success("API Master Report Sync Initiated...")
            st.balloons()

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
        
        c5, c6 = st.columns(2)
        f_dec_z = c5.selectbox("Founder Decision Required", ["NO", "YES"])
        dec_det_z = c6.text_input("Decision Details")

        if st.form_submit_button("Sync ZLD Report"):
            if f_dec_z == "YES":
                trigger_whatsapp_notification("Ammu (ZLD)", dec_det_z)
            st.success("ZLD Data Synced.")

# --- 6. ROLE: PURCHASE (SANTHOSHI) ---
elif role == "Purchase (Santhoshi)":
    st.header("📦 Purchase & Operations - Santhoshi")
    st.warning("🔔 Check Management Dashboard for technical dependencies.")

    with st.form("purchase_form"):
        st.subheader("👷 Manpower Tracking")
        p1, p2, p3 = st.columns(3)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        temp_mp = p3.selectbox("Temp Manpower Used", ["No", "Yes"])

        st.subheader("⚙️ Operations & Site Status")
        st.write("📊 **Machine & Transport Status**")
        ops_df = pd.DataFrame([{"Asset": "Plasma Machine", "Status": "Working", "Issue": "None"}])
        ops_data = st.data_editor(ops_df, num_rows="dynamic", use_container_width=True, key="ops_table")

        absentees = st.text_area("Absentees Details")

        st.subheader("🧠 Management & Decisions")
        f_dec_p = st.selectbox("Founder Decision Required", ["No", "Yes"])
        dec_det_p = st.text_input("Decision Details")
        
        if st.form_submit_button("Sync Purchase Log"):
            if f_dec_p == "Yes":
                trigger_whatsapp_notification("Santhoshi (Purchase)", dec_det_p)
            st.success("Operations Log Updated.")

# --- 7. MANAGEMENT DASHBOARD (UPDATED) ---
# --- 1. SESSION STATE FOR FORM RESET ---
if "form_cleared" not in st.session_state:
    st.session_state.form_cleared = False

def clear_form():
    st.session_state.form_cleared = True

# --- 7. MANAGEMENT DASHBOARD (FIXED READER) ---
else:
    st.header("📊 B&G Management Analytics")
    
    # Reader Engine
    def load_logs(repo, file):
        try:
            g = Github(st.secrets["GITHUB_TOKEN"])
            r = g.get_repo(f"Bgenggadmin/{repo}")
            c = r.get_contents(file)
            return pd.read_csv(io.StringIO(c.decoded_content.decode()))
        except:
            return pd.DataFrame() # Returns empty if file not found

    # SHOW TABLES
    st.subheader("🏗️ Recent API Site Logs")
    api_df = load_logs("bg-api-logs", "engineering_audit.csv")
    if not api_df.empty:
        st.dataframe(api_df.sort_values(by="Timestamp", ascending=False), use_container_width=True)
    else:
        st.info("No logs found. Ensure Kishore has synced data to 'engineering_audit.csv' on GitHub.")

    st.subheader("💧 Recent ZLD Project Status")
    zld_df = load_logs("bg-zld-logs", "project_execution.csv")
    if not zld_df.empty:
        st.dataframe(zld_df.sort_values(by="Timestamp", ascending=False), use_container_width=True)

# --- UPDATED SYNC BUTTON (Inside Kishore/Ammu Section) ---
# When you define your form, add the 'clear_on_submit' or use this logic:
if st.form_submit_button("🚀 Sync API Master Report"):
    # ... (Your existing Sync Logic) ...
    
    st.success("✅ Sync Successful! Clearing form for next entry...")
    st.balloons()
    
    # Force a rerun to clear the cells
    st.rerun()
