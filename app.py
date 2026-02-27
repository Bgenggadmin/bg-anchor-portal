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

    # 1. SALES TRACKING (NEW FIELDS ADDED)
    st.subheader("📈 1. Sales & Enquiry Tracking")
    s1, s2, s3, s4 = st.columns(4)
    offers_sub = s1.number_input("Offers Submitted Today", min_value=0, value=0, key=f"z_off_{sk}")
    new_enq = s2.number_input("New Enquiries Today", min_value=0, value=0, key=f"z_enq_n_{sk}")
    client_calls = s3.number_input("Client Calls Made", min_value=0, value=0, key=f"z_calls_{sk}")
    
    # Specific Sales Table for Key Feedbacks
    z_sales_df = pd.DataFrame([{"Client": "", "No_of_Days_Pending": 0, "Key_Feedback": "", "Offer_Status": "Pending"}])
    z_sales_data = st.data_editor(z_sales_df, num_rows="dynamic", use_container_width=True, key=f"z_sales_edit_{sk}")

    # 2. DESIGN STAGE (NEW FIELDS ADDED)
    st.subheader("📐 2. Design & Engineering Status")
    d1, d2 = st.columns(2)
    designs_review = d1.number_input("Designs Under Review", min_value=0, value=0, key=f"z_rev_{sk}")
    clarifications_pending = d2.number_input("Clarifications Pending", min_value=0, value=0, key=f"z_clar_{sk}")
    
    z_dwg_data = st.data_editor(pd.DataFrame([{"Project": "", "Dwg_Stage": "Initial", "Issue": ""}]), 
                                num_rows="dynamic", use_container_width=True, key=f"z_dwg_edit_{sk}")

    # 3. PROJECT EXECUTION & RISKS
    st.subheader("🏗️ 3. Project Execution & Risks")
    zld_proj_df = pd.DataFrame([{"Project_Name": "", "Stage": "Fabrication", "Target_Date": date.today(), "Risk": "No"}])
    zld_proj = st.data_editor(zld_proj_df, num_rows="dynamic", use_container_width=True, key=f"z_proj_edit_{sk}",
                              column_config={"Target_Date": st.column_config.DateColumn("Target Date", format="YYYY-MM-DD")})

    # 4. SITE UPDATES & FOUNDER DECISIONS
    st.subheader("🧠 4. Site Updates & Decisions")
    with st.form(f"zld_form_{sk}"):
        zld_updates = st.text_area("Major Site Events / Bottlenecks Today")
        f_dec_z = st.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context_z = st.text_area("Decision Context (if YES)")

        if st.form_submit_button("🚀 Sync ZLD Report"):
            # Prepare the main dataframe
            valid_zld = zld_proj[zld_proj["Project_Name"] != ""].copy()
            
            # If no specific project updated, create a summary row
            if valid_zld.empty:
                valid_zld = pd.DataFrame([{"Project_Name": "General ZLD Update"}])
            
            # Attach all new Sales & Design metrics
            valid_zld["Offers_Today"] = offers_sub
            valid_zld["New_Enq_Today"] = new_enq
            valid_zld["Client_Calls"] = client_calls
            valid_zld["Designs_Under_Review"] = designs_review
            valid_zld["Clarifications_Pending"] = clarifications_pending
            valid_zld["Daily_Updates"] = zld_updates
            valid_zld["Founder_Decision"] = f_dec_z
            valid_zld["Decision_Details"] = dec_context_z
            
            # Sync to main ZLD file
            if sync_to_private_file(valid_zld, "zld_report.csv"):
                # Also sync the detailed sales feedback table
                if not z_sales_data[z_sales_data["Client"] != ""].empty:
                    sync_to_private_file(z_sales_data[z_sales_data["Client"] != ""], "zld_sales_feedback.csv")
                
                st.success("✅ ZLD Data Synced Successfully!")
                st.session_state.sync_count += 1
                st.rerun()

    # --- 5. SUBHEADING WISE SUMMARY TABLES ---
    st.divider()
    st.subheader("📋 ZLD Submission Summary")
    zld_history = fetch_logs("zld_report.csv")
    zld_sales = fetch_logs("zld_sales_feedback.csv")
    
    if not zld_history.empty:
        z_tab1, z_tab2, z_tab3 = st.tabs(["📈 Sales & Design", "🏗️ Project Logs", "🧠 Management"])
        
        with z_tab1:
            sales_cols = ["Entry_Date", "Offers_Today", "New_Enq_Today", "Client_Calls", "Designs_Under_Review", "Clarifications_Pending"]
            st.write("#### Key Metrics")
            st.dataframe(zld_history[sales_cols].drop_duplicates(), use_container_width=True)
            st.write("#### Detailed Client Feedback")
            st.dataframe(zld_sales, use_container_width=True)
            
        with z_tab2:
            st.dataframe(zld_history[["Entry_Date", "Project_Name", "Stage", "Target_Date", "Risk"]], use_container_width=True)
            
        with z_tab3:
            st.dataframe(zld_history[["Entry_Date", "Daily_Updates", "Founder_Decision", "Decision_Details"]].drop_duplicates(), use_container_width=True)

        # ANCHOR EXCEL DOWNLOAD
        z_buffer = io.BytesIO()
        with pd.ExcelWriter(z_buffer, engine='xlsxwriter') as writer:
            zld_history.to_excel(writer, sheet_name='ZLD_Master_Log', index=False)
            if not zld_sales.empty: zld_sales.to_excel(writer, sheet_name='Sales_Feedback', index=False)
        
        st.download_button(label="📥 Download ZLD Excel", data=z_buffer.getvalue(),
                           file_name=f"Ammu_ZLD_Log_{date.today()}.xlsx", mime="application/vnd.ms-excel")

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

    # 2. CRITICAL MACHINERY RUNNING STATUS
    st.subheader("⚙️ 2. Critical Machinery Running Status")
    # Default rows provided for ease of use
    ops_df = pd.DataFrame([
        {"Asset": "Plasma Machine", "Status": "Working", "Production_Impacted": "No", "Risks_Next_2_3_Days": "Low", "Issue": ""},
        {"Asset": "EOT Crane", "Status": "Working", "Production_Impacted": "No", "Risks_Next_2_3_Days": "Low", "Issue": ""},
        {"Asset": "Site Vehicle", "Status": "Working", "Production_Impacted": "No", "Risks_Next_2_3_Days": "Low", "Issue": ""}
    ])
    
    ops_data = st.data_editor(
        ops_df, 
        num_rows="dynamic", 
        use_container_width=True, 
        key=f"ops_edit_{sk}",
        column_config={
            "Status": st.column_config.SelectboxColumn("Status", options=["Working", "Breakdown", "Under Maintenance"]),
            "Production_Impacted": st.column_config.SelectboxColumn("Production Impacted?", options=["No", "Yes", "Partial"]),
            "Risks_Next_2_3_Days": st.column_config.SelectboxColumn("Risk Level", options=["Low", "Medium", "High"])
        }
    )

    # 3. SITE REMARKS & DECISIONS
    st.subheader("🧠 3. Operations & Management")
    with st.form(f"pur_form_{sk}"):
        absentees = st.text_area("Absentees Details / Reasons for Low Manpower")
        site_events = st.text_area("Major Operations Updates")
        f_dec_p = st.selectbox("Founder Decision Required?", ["No", "Yes"])
        dec_det_p = st.text_area("Decision Details (if Yes)")

        if st.form_submit_button("🚀 Sync Purchase Report"):
            # FIX: Filter rows to only save machines that are NOT "Working" or have an "Issue" typed
            valid_machinery = ops_data[(ops_data["Status"] != "Working") | (ops_data["Issue"] != "")].copy()
            
            # If all machines are working fine, we create a single row for Manpower/Updates
            if valid_machinery.empty:
                final_sync_df = pd.DataFrame([{"Asset": "General Site Update", "Status": "Working"}])
            else:
                final_sync_df = valid_machinery

            # Attach Manpower and Remarks to the synced rows
            final_sync_df["Planned_MP"] = planned
            final_sync_df["Actual_MP"] = actual
            final_sync_df["Temp_Used"] = temp_mp
            final_sync_df["Absentees"] = absentees
            final_sync_df["Operations_Updates"] = site_events
            final_sync_df["Founder_Decision"] = f_dec_p
            final_sync_df["Decision_Context"] = dec_det_p

            if sync_to_private_file(final_sync_df, "purchase_report.csv"):
                st.success("✅ Purchase Log Updated! Data Cleared.")
                st.session_state.sync_count += 1
                st.rerun()

    # --- 4. SUBHEADING WISE SUMMARY TABLES ---
    st.divider()
    st.subheader("📋 Purchase Submission Summary")
    pur_history = fetch_logs("purchase_report.csv")
    
    if not pur_history.empty:
        p_tab1, p_tab2, p_tab3 = st.tabs(["👷 Manpower Logs", "⚙️ Machinery Status", "🧠 Management Decisions"])
        
        with p_tab1:
            manpower_cols = ["Entry_Date", "Timestamp", "Planned_MP", "Actual_MP", "Temp_Used", "Absentees"]
            st.dataframe(pur_history[manpower_cols].drop_duplicates(), use_container_width=True)
            
        with p_tab2:
            machinery_cols = ["Entry_Date", "Asset", "Status", "Production_Impacted", "Risks_Next_2_3_Days", "Issue"]
            # Only show rows that actually reported a machine status/issue
            st.dataframe(pur_history[pur_history["Asset"] != "General Site Update"][machinery_cols], use_container_width=True)
            
        with p_tab3:
            decision_cols = ["Entry_Date", "Operations_Updates", "Founder_Decision", "Decision_Context"]
            st.dataframe(pur_history[decision_cols].drop_duplicates(), use_container_width=True)

        # ANCHOR EXCEL DOWNLOAD
        p_buffer = io.BytesIO()
        with pd.ExcelWriter(p_buffer, engine='xlsxwriter') as writer:
            pur_history.to_excel(writer, sheet_name='Purchase_Full_Log', index=False)
        
        st.download_button(label="📥 Download My Purchase Log (Excel)", data=p_buffer.getvalue(),
                           file_name=f"Santhoshi_Purchase_Log_{date.today()}.xlsx", mime="application/vnd.ms-excel")

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
