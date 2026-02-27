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
    # ZLD Specific Tables
    zld_proj = st.data_editor(pd.DataFrame([{"Project": "", "Stage": "Fabrication", "Target_Date": date.today(), "Risk": "No"}]), 
                              num_rows="dynamic", use_container_width=True, key=f"zld_{sk}",
                              column_config={"Target_Date": st.column_config.DateColumn("Target Date", format="YYYY-MM-DD")})
    
    with st.form(f"zld_f_{sk}"):
        zld_updates = st.text_area("Site Updates / Bottlenecks")
        if st.form_submit_button("🚀 Sync ZLD Report"):
            valid_zld = zld_proj[zld_proj["Project"] != ""].copy()
            valid_zld["Updates"] = zld_updates
            if sync_to_private_file(valid_zld, "zld_report.csv"):
                st.success("✅ ZLD Data Synced!")
                st.session_state.sync_count += 1
                st.rerun()
    
    st.subheader("📋 Your Recent ZLD Logs")
    st.dataframe(fetch_logs("zld_report.csv"), use_container_width=True)

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
