import streamlit as st
import pandas as pd
from datetime import datetime, date
import pytz
from github import Github
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="B&G Digital Portal", layout="wide")
IST = pytz.timezone('Asia/Kolkata')

# --- 2. SESSION STATE ---
if "sync_count" not in st.session_state:
    st.session_state.sync_count = 0

# --- 3. MULTI-FILE SYNC ENGINE ---
def sync_to_private_file(df, filename):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo("Bgenggadmin/bg-anchor-portal")
        df['Entry_Date'] = datetime.now(IST).strftime("%Y-%m-%d")
        df['Timestamp'] = datetime.now(IST).strftime("%H:%M")
        try:
            file_contents = repo.get_contents(filename)
            existing_data = pd.read_csv(io.StringIO(file_contents.decoded_content.decode()))
            updated_df = pd.concat([df, existing_data], ignore_index=True)
            repo.update_file(file_contents.path, f"Update: {filename}", updated_df.to_csv(index=False), file_contents.sha)
        except:
            repo.create_file(filename, f"Initial {filename}", df.to_csv(index=False))
        return True
    except Exception as e:
        st.error(f"Sync Failed for {filename}: {e}")
        return False

def fetch_logs(filename):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo("Bgenggadmin/bg-anchor-portal")
        contents = repo.get_contents(filename)
        return pd.read_csv(io.StringIO(contents.decoded_content.decode()))
    except:
        return pd.DataFrame()

# --- 4. SIDEBAR (UPDATED TO INCLUDE ALL ANCHORS) ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Founder Dashboard"])
sk = st.session_state.sync_count 

# --- 5. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    # [Your existing 5 tables for Kishore go here]
    api_pur = st.data_editor(pd.DataFrame([{"Job": "", "Material": "", "Req_Date": date.today(), "Urgency": "High"}]), 
                             num_rows="dynamic", use_container_width=True, key=f"pur_{sk}",
                             column_config={"Req_Date": st.column_config.DateColumn("Required Date", format="YYYY-MM-DD")})
    
    api_sales = st.data_editor(pd.DataFrame([{"Client": "", "Offers": 0, "Status": "Review"}]), 
                               num_rows="dynamic", use_container_width=True, key=f"sales_{sk}")

    api_mfg = st.data_editor(pd.DataFrame([{"Job Code": "", "Planned": "", "Actual": "", "Delay_Reason": ""}]), 
                               num_rows="dynamic", use_container_width=True, key=f"mfg_{sk}")

    api_ncr = st.data_editor(pd.DataFrame([{"Category": "Material", "Detail": "", "Impact": "NO"}]), 
                               num_rows="dynamic", use_container_width=True, key=f"ncr_{sk}")

    with st.form(f"mgmt_form_{sk}"):
        f_dec = st.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = st.text_area("Decision Context")
        if st.form_submit_button("🚀 SYNC ALL TABLES"):
            sync_to_private_file(api_pur[api_pur["Job"] != ""], "api_purchase.csv")
            sync_to_private_file(api_sales[api_sales["Client"] != ""], "api_sales.csv")
            sync_to_private_file(api_mfg[api_mfg["Job Code"] != ""], "api_manufacturing.csv")
            sync_to_private_file(api_ncr[api_ncr["Detail"] != ""], "api_ncr.csv")
            sync_to_private_file(pd.DataFrame([{"Decision_Req": f_dec, "Context": dec_context}]), "api_management.csv")
            st.success("✅ Reports Synced!")
            st.session_state.sync_count += 1
            st.rerun()

    # Summary Tabs for Kishore
    st.divider()
    tabs = st.tabs(["Purchase", "Sales", "Mfg", "NCR", "Mgmt"])
    tabs[0].dataframe(fetch_logs("api_purchase.csv"), use_container_width=True)
    tabs[1].dataframe(fetch_logs("api_sales.csv"), use_container_width=True)
    tabs[2].dataframe(fetch_logs("api_manufacturing.csv"), use_container_width=True)
    tabs[3].dataframe(fetch_logs("api_ncr.csv"), use_container_width=True)
    tabs[4].dataframe(fetch_logs("api_management.csv"), use_container_width=True)

# --- 6. ROLE: ZLD (AMMU) ---
elif role == "ZLD (Ammu)":
    st.header("💧 ZLD Site Entry - Ammu Anchor")
    sk = st.session_state.sync_count 

    # 1. PURCHASE INTEGRATION
    st.subheader("🔴 1. Purchase Integration (ZLD)")
    zld_pur_df = pd.DataFrame([{"Project": "", "Component": "", "Req_Date": date.today(), "Urgency": "Medium"}])
    zld_pur = st.data_editor(zld_pur_df, num_rows="dynamic", use_container_width=True, key=f"z_pur_{sk}",
                             column_config={"Req_Date": st.column_config.DateColumn("Required Date", format="YYYY-MM-DD")})

    # 2. ENQUIRY & DESIGN STATUS
    st.subheader("📈 2. Enquiry & Design Status")
    c1, c2 = st.columns(2)
    with c1:
        st.write("📝 Sales Tracking")
        z_enq = st.data_editor(pd.DataFrame([{"Client": "", "Offer_Status": "Pending"}]), num_rows="dynamic", key=f"z_enq_{sk}")
    with c2:
        st.write("📐 Design Stage")
        z_dwg = st.data_editor(pd.DataFrame([{"Project": "", "Dwg_Stage": "Initial"}]), num_rows="dynamic", key=f"z_dwg_{sk}")

    # 3. PROJECT EXECUTION & RISKS
    st.subheader("🏗️ 3. Project Execution & Risks")
    zld_proj_df = pd.DataFrame([{"Project_Name": "", "Stage": "Fabrication", "Target_Date": date.today(), "Risk": "No"}])
    zld_proj = st.data_editor(zld_proj_df, num_rows="dynamic", use_container_width=True, key=f"z_proj_{sk}",
                              column_config={"Target_Date": st.column_config.DateColumn("Target Date", format="YYYY-MM-DD")})

    # 4. SITE UPDATES & FOUNDER DECISIONS
    st.subheader("🧠 4. Site Updates & Decisions")
    with st.form(f"zld_form_{sk}"):
        zld_updates = st.text_area("Major Site Events / Bottlenecks Today")
        f_dec_z = st.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context_z = st.text_area("Decision Context (if YES)")

        if st.form_submit_button("🚀 Sync ZLD Report"):
            # Sync tables to separate CSVs to keep them clean
            sync_to_private_file(zld_pur[zld_pur["Project"] != ""], "zld_purchase.csv")
            sync_to_private_file(z_enq[z_enq["Client"] != ""], "zld_enquiries.csv")
            sync_to_private_file(z_dwg[z_dwg["Project"] != ""], "zld_drawings.csv")
            
            # Combine execution and decision into one report
            valid_zld = zld_proj[zld_proj["Project_Name"] != ""].copy()
            valid_zld["Updates"] = zld_updates
            valid_zld["Decision_Req"] = f_dec_z
            valid_zld["Decision_Details"] = dec_context_z
            
            if sync_to_private_file(valid_zld, "zld_report.csv"):
                st.success("✅ ZLD Data Synced Successfully!")
                st.session_state.sync_count += 1
                st.rerun()

    # 5. ZLD SUMMARY TABLES
    st.divider()
    st.subheader("📋 Your Recent ZLD Submission Logs")
    tabs = st.tabs(["Purchase", "Sales", "Projects", "Updates"])
    tabs[0].dataframe(fetch_logs("zld_purchase.csv"), use_container_width=True)
    tabs[1].dataframe(fetch_logs("zld_enquiries.csv"), use_container_width=True)
    tabs[2].dataframe(fetch_logs("zld_report.csv"), use_container_width=True)
    
    # ZLD EXCEL DOWNLOAD
    z_buffer = io.BytesIO()
    with pd.ExcelWriter(z_buffer, engine='xlsxwriter') as writer:
        fetch_logs("zld_purchase.csv").to_excel(writer, sheet_name='Purchase', index=False)
        fetch_logs("zld_report.csv").to_excel(writer, sheet_name='Projects', index=False)
    
    st.download_button(label="📥 Download My ZLD Log (Excel)", data=z_buffer.getvalue(),
                       file_name=f"Ammu_ZLD_Report_{date.today()}.xlsx", mime="application/vnd.ms-excel")

# --- 7. ROLE: PURCHASE (SANTHOSHI) ---
elif role == "Purchase (Santhoshi)":
    st.header("📦 Purchase & Operations - Santhoshi")
    c1, c2 = st.columns(2)
    p_man = c1.number_input("Planned Manpower", value=62, key=f"p_{sk}")
    a_man = c2.number_input("Actual Manpower", value=52, key=f"a_{sk}")
    
    ops_df = st.data_editor(pd.DataFrame([{"Asset": "Plasma Machine", "Status": "Working"}]), num_rows="dynamic", key=f"ops_{sk}")
    
    if st.button("🚀 Sync Purchase Report"):
        valid_pur = ops_df.copy()
        valid_pur["Planned"] = p_man
        valid_pur["Actual"] = a_man
        if sync_to_private_file(valid_pur, "purchase_report.csv"):
            st.success("✅ Purchase Log Updated!")
            st.session_state.sync_count += 1
            st.rerun()

    st.subheader("📋 Your Recent Purchase Logs")
    st.dataframe(fetch_logs("purchase_report.csv"), use_container_width=True)

# --- 8. FOUNDER DASHBOARD ---
else:
    st.header("📊 Founder Master Overview")
    # Excel Download Logic (combining all files)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        fetch_logs("api_purchase.csv").to_excel(writer, sheet_name='API_Pur', index=False)
        fetch_logs("zld_report.csv").to_excel(writer, sheet_name='ZLD_Report', index=False)
        fetch_logs("purchase_report.csv").to_excel(writer, sheet_name='Purchase_Ops', index=False)
    
    st.download_button(label="📥 Download Master Excel Report", data=buffer.getvalue(),
                       file_name=f"BG_Master_{date.today()}.xlsx", mime="application/vnd.ms-excel")
