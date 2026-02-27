import streamlit as st
import pandas as pd
from datetime import datetime
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
        
        df['Date'] = datetime.now(IST).strftime("%Y-%m-%d")
        df['Timestamp'] = datetime.now(IST).strftime("%H:%M")

        try:
            file = repo.get_contents(filename)
            existing = pd.read_csv(io.StringIO(file.decoded_content.decode()))
            updated = pd.concat([df, existing], ignore_index=True)
            repo.update_file(file.path, f"Update: {filename}", updated.to_csv(index=False), file.sha)
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
        return pd.read_csv(io.StringIO(repo.get_contents(filename).decoded_content.decode()))
    except: return pd.DataFrame()

# --- 4. SIDEBAR ---
role = st.sidebar.radio("Role:", ["API (Kishore)", "Founder Dashboard"])
sk = st.session_state.sync_count 

# --- 5. ROLE: API (KISHORE) - 5 INDEPENDENT TABLES ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")

    # 1. Purchase Dependencies
    st.subheader("🔴 Critical Purchase Dependencies")
    api_pur = st.data_editor(pd.DataFrame([{"Job": "", "Material": "", "Req_Date": "", "Urgency": "High"}]), 
                             num_rows="dynamic", use_container_width=True, key=f"pur_{sk}")

    # 2. Sales & Enquiry
    st.subheader("📊 Sales & Enquiry Tracking")
    api_sales = st.data_editor(pd.DataFrame([{"Client": "", "Offers": 0, "Status": "Review"}]), 
                               num_rows="dynamic", use_container_width=True, key=f"sales_{sk}")

    # 3. Technical & Manufacturing
    st.subheader("🛠️ Technical & Manufacturing Progress")
    api_mfg = st.data_editor(pd.DataFrame([{"Job Code": "", "Planned": "", "Actual": "", "Delay_Reason": ""}]), 
                             num_rows="dynamic", use_container_width=True, key=f"mfg_{sk}")

    # 4. Deviations & NCR
    st.subheader("⚠️ Deviations & Quality (NCR)")
    api_ncr = st.data_editor(pd.DataFrame([{"Category": "Material", "Detail": "", "Impact": "NO"}]), 
                             num_rows="dynamic", use_container_width=True, key=f"ncr_{sk}")

    # 5. Management Decisions
    st.subheader("🧠 Management Decisions")
    with st.form(f"mgmt_form_{sk}"):
        f_dec = st.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = st.text_area("Decision Context")
        
        if st.form_submit_button("🚀 SYNC ALL TABLES"):
            # Sync each table to its own file
            sync_to_private_file(api_pur[api_pur["Job"] != ""], "api_purchase.csv")
            sync_to_private_file(api_sales[api_sales["Client"] != ""], "api_sales.csv")
            sync_to_private_file(api_mfg[api_mfg["Job Code"] != ""], "api_manufacturing.csv")
            sync_to_private_file(api_ncr[api_ncr["Detail"] != ""], "api_ncr.csv")
            
            # Management Decision log
            mgmt_df = pd.DataFrame([{"Decision_Req": f_dec, "Context": dec_context}])
            sync_to_private_file(mgmt_df, "api_management.csv")
            
            st.success("✅ All 5 Reports Synced Separately! Forms Cleared.")
            st.session_state.sync_count += 1
            st.rerun()

    # INDIVIDUAL SUMMARY TABLES
    st.divider()
    st.subheader("📋 Recent Submission Summary (API)")
    tabs = st.tabs(["Purchase", "Sales", "Mfg", "NCR", "Mgmt"])
    tabs[0].dataframe(fetch_logs("api_purchase.csv"), use_container_width=True)
    tabs[1].dataframe(fetch_logs("api_sales.csv"), use_container_width=True)
    tabs[2].dataframe(fetch_logs("api_manufacturing.csv"), use_container_width=True)
    tabs[3].dataframe(fetch_logs("api_ncr.csv"), use_container_width=True)
    tabs[4].dataframe(fetch_logs("api_management.csv"), use_container_width=True)

# --- 6. FOUNDER DASHBOARD & EXCEL DOWNLOAD ---
elif role == "Founder Dashboard":
    st.header("📊 Founder Master Overview")
    
    # EXCEL GENERATOR
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        fetch_logs("api_purchase.csv").to_excel(writer, sheet_name='Purchase', index=False)
        fetch_logs("api_sales.csv").to_excel(writer, sheet_name='Sales', index=False)
        fetch_logs("api_manufacturing.csv").to_excel(writer, sheet_name='Manufacturing', index=False)
        fetch_logs("api_ncr.csv").to_excel(writer, sheet_name='Quality_NCR', index=False)
        fetch_logs("api_management.csv").to_excel(writer, sheet_name='Management', index=False)
    
    st.download_button(
        label="📥 Download Master API Excel Report",
        data=buffer.getvalue(),
        file_name=f"BG_API_Report_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.ms-excel"
    )
    
    st.write("Review all 5 sheets in the downloaded file for full details.")
