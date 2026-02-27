import streamlit as st
import pandas as pd
from datetime import datetime, date
import pytz
from github import Github
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="B&G Digital Portal", layout="wide")
IST = pytz.timezone('Asia/Kolkata')

# --- 2. SESSION STATE (FIXES CELL CLEARING) ---
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
    except: return pd.DataFrame()

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Founder Dashboard"])
sk = st.session_state.sync_count 

# --- 5. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    api_pur = st.data_editor(pd.DataFrame([{"Job": "", "Material": "", "Req_Date": date.today(), "Urgency": "High"}]), 
                             num_rows="dynamic", use_container_width=True, key=f"pur_{sk}",
                             column_config={"Req_Date": st.column_config.DateColumn("Required Date", format="YYYY-MM-DD")})
    api_sales = st.data_editor(pd.DataFrame([{"Client": "", "Offers": 0, "Status": "Review"}]), 
                               num_rows="dynamic", use_container_width=True, key=f"sales_{sk}")
    api_mfg = st.data_editor(pd.DataFrame([{"Job Code": "", "Planned": "", "Actual": "", "Delay_Reason": ""}]), 
                             num_rows="dynamic", use_container_width=True, key=f"mfg_{sk}")
    api_ncr = st.data_editor(pd.DataFrame([{"Category": "Material", "Detail": "", "Impact": "NO"}]), 
                             num_rows="dynamic", use_container_width=True, key=f"ncr_{sk}")

    with st.form(f"api_f_{sk}"):
        f_dec = st.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = st.text_area("Decision Context")
        if st.form_submit_button("🚀 SYNC ALL TABLES"):
            sync_to_private_file(api_pur[api_pur["Job"] != ""], "api_purchase.csv")
            sync_to_private_file(api_sales[api_sales["Client"] != ""], "api_sales.csv")
            sync_to_private_file(api_mfg[api_mfg["Job Code"] != ""], "api_manufacturing.csv")
            sync_to_private_file(api_ncr[api_ncr["Detail"] != ""], "api_ncr.csv")
            sync_to_private_file(pd.DataFrame([{"Decision_Req": f_dec, "Context": dec_context}]), "api_management.csv")
            st.session_state.sync_count += 1
            st.rerun()

    st.divider()
    st.subheader("📋 API Submission Summary")
    tabs = st.tabs(["🔴 Purchase", "📊 Sales", "🛠️ Mfg", "⚠️ NCR", "🧠 Mgmt"])
    tabs[0].dataframe(fetch_logs("api_purchase.csv"), use_container_width=True)
    tabs[1].dataframe(fetch_logs("api_sales.csv"), use_container_width=True)
    tabs[2].dataframe(fetch_logs("api_manufacturing.csv"), use_container_width=True)
    tabs[3].dataframe(fetch_logs("api_ncr.csv"), use_container_width=True)
    tabs[4].dataframe(fetch_logs("api_management.csv"), use_container_width=True)

# --- 6. ROLE: ZLD (AMMU) ---
elif role == "ZLD (Ammu)":
    st.header("💧 ZLD Site Entry - Ammu Anchor")
    zld_pur = st.data_editor(pd.DataFrame([{"Project": "", "Material": "", "Req_Date": date.today(), "Urgency": "High"}]), 
                             num_rows="dynamic", use_container_width=True, key=f"z_pur_{sk}",
                             column_config={"Req_Date": st.column_config.DateColumn("Required Date", format="YYYY-MM-DD")})
    
    s1, s2, s3 = st.columns(3)
    offers_sub = s1.number_input("Offers Submitted Today", min_value=0, value=0, key=f"z_off_{sk}")
    new_enq = s2.number_input("New Enquiries Today", min_value=0, value=0, key=f"z_enq_n_{sk}")
    client_calls = s3.number_input("Client Calls Made", min_value=0, value=0, key=f"z_calls_{sk}")
    z_sales_data = st.data_editor(pd.DataFrame([{"Client": "", "No_of_Days_Pending": 0, "Key_Feedback": "", "Offer_Status": "Pending"}]), 
                                  num_rows="dynamic", use_container_width=True, key=f"z_sales_{sk}")
    
    d1, d2 = st.columns(2)
    designs_review = d1.number_input("Designs Under Review", min_value=0, value=0, key=f"z_rev_{sk}")
    clar_pending = d2.number_input("Clarifications Pending", min_value=0, value=0, key=f"z_clar_{sk}")
    zld_proj_data = st.data_editor(pd.DataFrame([{"Project_Name": "", "Stage": "Fabrication", "Target_Date": date.today(), "Risk": "No"}]), 
                                   num_rows="dynamic", use_container_width=True, key=f"z_proj_{sk}",
                                   column_config={"Target_Date": st.column_config.DateColumn("Target Date", format="YYYY-MM-DD")})

    with st.form(f"zld_f_{sk}"):
        zld_updates = st.text_area("Site Updates / Bottlenecks")
        f_dec_z = st.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context_z = st.text_area("Decision Context (if YES)")
        if st.form_submit_button("🚀 Sync ZLD Report"):
            sync_to_private_file(zld_pur[zld_pur["Project"] != ""], "zld_purchase.csv")
            sync_to_private_file(z_sales_data[z_sales_data["Client"] != ""], "zld_sales_feedback.csv")
            valid_zld = zld_proj_data[zld_proj_data["Project_Name"] != ""].copy()
            if valid_zld.empty: valid_zld = pd.DataFrame([{"Project_Name": "General Update"}])
            valid_zld.update({"Offers_Today": offers_sub, "New_Enq_Today": new_enq, "Client_Calls": client_calls, "Designs_Review": designs_review, "Clar_Pending": clar_pending, "Updates": zld_updates, "Decision_Req": f_dec_z, "Decision_Details": dec_context_z})
            sync_to_private_file(valid_zld, "zld_report.csv")
            st.session_state.sync_count += 1
            st.rerun()

    st.divider()
    z_tabs = st.tabs(["🔴 Purchase", "📈 Sales/Design", "🏗️ Projects", "🧠 Mgmt"])
    z_tabs[0].dataframe(fetch_logs("zld_purchase.csv"), use_container_width=True)
    z_tabs[1].dataframe(fetch_logs("zld_sales_feedback.csv"), use_container_width=True)
    z_tabs[2].dataframe(fetch_logs("zld_report.csv"), use_container_width=True)
    z_tabs[3].dataframe(fetch_logs("zld_report.csv"), use_container_width=True)

# --- 7. ROLE: PURCHASE (SANTHOSHI) ---
elif role == "Purchase (Santhoshi)":
    st.header("📦 Purchase & Operations - Santhoshi")
    p1, p2, p3 = st.columns(3)
    planned = p1.number_input("Planned Manpower", value=62, key=f"p_man_{sk}")
    actual = p2.number_input("Actual Manpower", value=52, key=f"a_man_{sk}")
    temp_mp = p3.selectbox("Temp Manpower Used?", ["No", "Yes"], key=f"temp_{sk}")

    st.subheader("⚙️ 2. Critical Machinery Running Status")
    ops_df = pd.DataFrame([{"Asset": "Plasma Machine", "Status": "Working", "Production_Impacted": "No", "Risks_Next_2_3_Days": "Low", "Issue": ""},
                           {"Asset": "EOT Crane", "Status": "Working", "Production_Impacted": "No", "Risks_Next_2_3_Days": "Low", "Issue": ""},
                           {"Asset": "Site Vehicle", "Status": "Working", "Production_Impacted": "No", "Risks_Next_2_3_Days": "Low", "Issue": ""}])
    ops_data = st.data_editor(ops_df, num_rows="dynamic", use_container_width=True, key=f"ops_edit_{sk}",
                              column_config={"Status": st.column_config.SelectboxColumn("Status", options=["Working", "Breakdown", "Under Maintenance"]),
                                             "Production_Impacted": st.column_config.SelectboxColumn("Production Impacted?", options=["No", "Yes", "Partial"]),
                                             "Risks_Next_2_3_Days": st.column_config.SelectboxColumn("Risk Level", options=["Low", "Medium", "High"])})

    with st.form(f"pur_f_{sk}"):
        absentees = st.text_area("Absentees Details / Reasons for Low Manpower")
        site_events = st.text_area("Major Operations Updates")
        f_dec_p = st.selectbox("Founder Decision Required?", ["No", "Yes"])
        dec_det_p = st.text_area("Decision Details (if Yes)")
        if st.form_submit_button("🚀 Sync Purchase Report"):
            valid_machinery = ops_data[(ops_data["Status"] != "Working") | (ops_data["Issue"] != "")].copy()
            final_df = valid_machinery if not valid_machinery.empty else pd.DataFrame([{"Asset": "General Update", "Status": "Working"}])
            final_df.update({"Planned_MP": planned, "Actual_MP": actual, "Temp_Used": temp_mp, "Absentees": absentees, "Updates": site_events, "Founder_Decision": f_dec_p, "Decision_Context": dec_det_p})
            sync_to_private_file(final_df, "purchase_report.csv")
            st.session_state.sync_count += 1
            st.rerun()

    st.divider()
    p_tabs = st.tabs(["👷 Manpower Logs", "⚙️ Machinery Status", "🧠 Management Decisions"])
    p_history = fetch_logs("purchase_report.csv")
    if not p_history.empty:
        p_tabs[0].dataframe(p_history[["Entry_Date", "Timestamp", "Planned_MP", "Actual_MP", "Temp_Used", "Absentees"]].drop_duplicates(), use_container_width=True)
        p_tabs[1].dataframe(p_history[p_history["Asset"] != "General Update"][["Entry_Date", "Asset", "Status", "Production_Impacted", "Risks_Next_2_3_Days", "Issue"]], use_container_width=True)
        p_tabs[2].dataframe(p_history[["Entry_Date", "Updates", "Founder_Decision", "Decision_Context"]].drop_duplicates(), use_container_width=True)

# --- 8. FOUNDER DASHBOARD ---
else:
    st.header("📊 Founder Master Overview")
    api_p, api_m, zld_r, pur_r = fetch_logs("api_purchase.csv"), fetch_logs("api_manufacturing.csv"), fetch_logs("zld_report.csv"), fetch_logs("purchase_report.csv")
    period = st.radio("Select View:", ["Today", "This Week", "This Month", "All Time"], horizontal=True)
    def filter_data(df):
        if df.empty: return df
        df['Date'] = pd.to_datetime(df['Entry_Date'])
        if period == "Today": return df[df['Date'].dt.date == date.today()]
        elif period == "This Week": return df[df['Date'] > (pd.Timestamp.now() - pd.Timedelta(days=7))]
        elif period == "This Month": return df[df['Date'].dt.month == date.today().month]
        return df

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        filter_data(api_p).to_excel(writer, sheet_name='API_Purchase', index=False)
        filter_data(api_m).to_excel(writer, sheet_name='API_Mfg', index=False)
        filter_data(zld_r).to_excel(writer, sheet_name='ZLD_Report', index=False)
        filter_data(pur_r).to_excel(writer, sheet_name='Purchase_Ops', index=False)
    
    st.download_button(label=f"📥 Download {period} Master Report (Excel)", data=buffer.getvalue(), file_name=f"BG_{period}_Report_{date.today()}.xlsx", mime="application/vnd.ms-excel")
    st.divider()
    t1, t2, t3 = st.tabs(["🏗️ API (Kishore)", "💧 ZLD (Ammu)", "📦 Purchase (Santhoshi)"])
    t1.dataframe(filter_data(api_m), use_container_width=True)
    t2.dataframe(filter_data(zld_r), use_container_width=True)
    t3.dataframe(filter_data(pur_r), use_container_width=True)
