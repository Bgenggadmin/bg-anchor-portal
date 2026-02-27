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
    sk = st.session_state.sync_count 

    # 1. MANPOWER TRACKING
    st.subheader("👷 1. Manpower Tracking")
    p1, p2, p3 = st.columns(3)
    planned = p1.number_input("Planned Manpower", value=62, key=f"p_man_{sk}")
    actual = p2.number_input("Actual Manpower", value=52, key=f"a_man_{sk}")
    temp_mp = p3.selectbox("Temp Manpower Used?", ["No", "Yes"], key=f"temp_{sk}")

    # 2. MACHINE & TRANSPORT STATUS
    st.subheader("⚙️ 2. Machine & Transport Status")
    ops_df = pd.DataFrame([
        {"Asset": "Plasma Machine", "Status": "Working", "Issue": "None"},
        {"Asset": "EOT Crane", "Status": "Working", "Issue": "None"},
        {"Asset": "Site Vehicle", "Status": "Working", "Issue": "None"}
    ])
    ops_data = st.data_editor(ops_df, num_rows="dynamic", use_container_width=True, key=f"ops_edit_{sk}",
                              column_config={
                                  "Status": st.column_config.SelectboxColumn(
                                      "Status", options=["Working", "Breakdown", "Under Maintenance"]
                                  )
                              })

    # 3. SITE REMARKS & DECISIONS
    st.subheader("🧠 3. Operations & Management")
    with st.form(f"pur_form_{sk}"):
        absentees = st.text_area("Absentees Details / Reasons for Low Manpower")
        site_events = st.text_area("Major Operations Updates")
        f_dec_p = st.selectbox("Founder Decision Required?", ["No", "Yes"])
        dec_det_p = st.text_area("Decision Details (if Yes)")

        if st.form_submit_button("🚀 Sync Purchase Report"):
            # Prepare the final dataframe for the CSV
            valid_pur = ops_data.copy()
            valid_pur["Planned_MP"] = planned
            valid_pur["Actual_MP"] = actual
            valid_pur["Temp_Used"] = temp_mp
            valid_pur["Absentees"] = absentees
            valid_pur["Operations_Updates"] = site_events
            valid_pur["Founder_Decision"] = f_dec_p
            valid_pur["Decision_Context"] = dec_det_p

            if sync_to_private_file(valid_pur, "purchase_report.csv"):
                st.success("✅ Purchase Log Updated! Data Cleared.")
                st.session_state.sync_count += 1
                st.rerun()

    # 4. PURCHASE SUMMARY TABLE
    st.divider()
    st.subheader("📋 Your Recent Purchase Logs")
    pur_history = fetch_logs("purchase_report.csv")
    if not pur_history.empty:
        st.dataframe(pur_history, use_container_width=True)
        
        # ANCHOR EXCEL DOWNLOAD
        p_buffer = io.BytesIO()
        with pd.ExcelWriter(p_buffer, engine='xlsxwriter') as writer:
            pur_history.to_excel(writer, sheet_name='Purchase_Ops', index=False)
        
        st.download_button(label="📥 Download My Purchase Log (Excel)", data=p_buffer.getvalue(),
                           file_name=f"Santhoshi_Purchase_Log_{date.today()}.xlsx", mime="application/vnd.ms-excel")
# --- 8. FOUNDER DASHBOARD ---
# --- 8. FOUNDER DASHBOARD ---
else:
    st.header("📊 Founder Master Overview")
    
    # 1. FETCH ALL DATA STREAMS
    # We pull from the clean, isolated files in your repository
    api_p = fetch_logs("api_purchase.csv")
    api_m = fetch_logs("api_manufacturing.csv")
    api_s = fetch_logs("api_sales.csv")
    api_d = fetch_logs("api_drawings.csv")
    api_n = fetch_logs("api_ncr.csv")
    api_mg = fetch_logs("api_management.csv")
    
    zld_r = fetch_logs("zld_report.csv")
    pur_r = fetch_logs("purchase_report.csv")

    # 2. MASTER EXCEL DOWNLOAD (Multi-Sheet)
    st.subheader("📥 Export Master Data")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        if not api_p.empty: api_p.to_excel(writer, sheet_name='API_Purchase', index=False)
        if not api_m.empty: api_m.to_excel(writer, sheet_name='API_Manufacturing', index=False)
        if not zld_r.empty: zld_r.to_excel(writer, sheet_name='ZLD_Report', index=False)
        if not pur_r.empty: pur_r.to_excel(writer, sheet_name='Purchase_Ops', index=False)
    
    st.download_button(
        label="📥 Download Master Excel Report",
        data=buffer.getvalue(),
        file_name=f"BG_Master_Report_{date.today()}.xlsx",
        mime="application/vnd.ms-excel"
    )

    st.divider()

    # 3. LIVE DATA TABS (For Quick Review)
    st.subheader("📋 Live Site Feeds")
    t1, t2, t3 = st.tabs(["🏗️ API (Kishore)", "💧 ZLD (Ammu)", "📦 Purchase (Santhoshi)"])
    
    with t1:
        st.write("### Technical & Progress Logs")
        st.dataframe(api_m, use_container_width=True)
        st.write("### Purchase Dependencies")
        st.dataframe(api_p, use_container_width=True)
        st.write("### Management Decisions Requested")
        st.dataframe(api_mg, use_container_width=True)

    with t2:
        st.write("### ZLD Project Status")
        st.dataframe(zld_r, use_container_width=True)

    with t3:
        st.write("### Manpower & Asset Status")
        st.dataframe(pur_r, use_container_width=True)
