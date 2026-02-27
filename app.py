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
        
        # Add metadata for every entry
        df['Entry_Date'] = datetime.now(IST).strftime("%Y-%m-%d")
        df['Timestamp'] = datetime.now(IST).strftime("%H:%M")

        try:
            # Update existing file
            file_contents = repo.get_contents(filename)
            existing_data = pd.read_csv(io.StringIO(file_contents.decoded_content.decode()))
            updated_df = pd.concat([df, existing_data], ignore_index=True)
            repo.update_file(file_contents.path, f"Update: {filename}", updated_df.to_csv(index=False), file_contents.sha)
        except:
            # Create file if missing
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

# --- 4. SIDEBAR ---
role = st.sidebar.radio("Role:", ["API (Kishore)", "Founder Dashboard"])
sk = st.session_state.sync_count 

# --- 5. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")

    # 1. Purchase Dependencies (WITH DATE SELECTOR)
    st.subheader("🔴 Critical Purchase Dependencies")
    init_pur_df = pd.DataFrame([{"Job": "", "Material": "", "Req_Date": date.today(), "Urgency": "High"}])
    
    api_pur = st.data_editor(
        init_pur_df, 
        num_rows="dynamic", 
        use_container_width=True, 
        key=f"pur_{sk}",
        column_config={
            "Req_Date": st.column_config.DateColumn("Required Date", format="YYYY-MM-DD")
        }
    )

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

    # 5. Management Decisions Form
    st.subheader("🧠 Management Decisions")
    with st.form(f"mgmt_form_{sk}"):
        f_dec = st.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = st.text_area("Decision Context")
        
        if st.form_submit_button("🚀 SYNC ALL TABLES"):
            # Sync each table to its own file on GitHub
            sync_to_private_file(api_pur[api_pur["Job"] != ""], "api_purchase.csv")
            sync_to_private_file(api_sales[api_sales["Client"] != ""], "api_sales.csv")
            sync_to_private_file(api_mfg[api_mfg["Job Code"] != ""], "api_manufacturing.csv")
            sync_to_private_file(api_ncr[api_ncr["Detail"] != ""], "api_ncr.csv")
            
            # Save Management Decision
            mgmt_df = pd.DataFrame([{"Decision_Req": f_dec, "Context": dec_context}])
            sync_to_private_file(mgmt_df, "api_management.csv")
            
            st.success("✅ All 5 Reports Synced Separately! Forms Cleared.")
            st.session_state.sync_count += 1
            st.rerun()

    # --- INDIVIDUAL SUMMARY TABLES (RE-INTEGRATED) ---
    st.divider()
    st.subheader("📋 Your Recent Submission Logs (API)")
    
    # FETCH DATA FOR TABS
    df_p = fetch_logs("api_purchase.csv")
    df_s = fetch_logs("api_sales.csv")
    df_m = fetch_logs("api_manufacturing.csv")
    df_n = fetch_logs("api_ncr.csv")
    df_mg = fetch_logs("api_management.csv")

    tabs = st.tabs(["Purchase", "Sales", "Mfg", "NCR", "Mgmt"])
    tabs[0].dataframe(df_p, use_container_width=True)
    tabs[1].dataframe(df_s, use_container_width=True)
    tabs[2].dataframe(df_m, use_container_width=True)
    tabs[3].dataframe(df_n, use_container_width=True)
    tabs[4].dataframe(df_mg, use_container_width=True)

    # --- ANCHOR EXCEL DOWNLOAD ---
    if not df_p.empty or not df_s.empty:
        anchor_buffer = io.BytesIO()
        with pd.ExcelWriter(anchor_buffer, engine='xlsxwriter') as writer:
            df_p.to_excel(writer, sheet_name='Purchase', index=False)
            df_s.to_excel(writer, sheet_name='Sales', index=False)
            df_m.to_excel(writer, sheet_name='Manufacturing', index=False)
            df_n.to_excel(writer, sheet_name='Quality_NCR', index=False)
            df_mg.to_excel(writer, sheet_name='Management', index=False)
        
        st.download_button(
            label="📥 Download My API Logs (Excel)",
            data=anchor_buffer.getvalue(),
            file_name=f"Kishore_API_Log_{date.today()}.xlsx",
            mime="application/vnd.ms-excel"
        )

# --- 6. FOUNDER DASHBOARD ---
elif role == "Founder Dashboard":
    st.header("📊 Founder Master Overview")
    
    # Fetch all data for Master Download
    df_p_f = fetch_logs("api_purchase.csv")
    df_s_f = fetch_logs("api_sales.csv")
    df_m_f = fetch_logs("api_manufacturing.csv")
    df_n_f = fetch_logs("api_ncr.csv")
    df_mg_f = fetch_logs("api_management.csv")

    # EXCEL GENERATOR
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_p_f.to_excel(writer, sheet_name='Purchase', index=False)
        df_s_f.to_excel(writer, sheet_name='Sales', index=False)
        df_m_f.to_excel(writer, sheet_name='Manufacturing', index=False)
        df_n_f.to_excel(writer, sheet_name='Quality_NCR', index=False)
        df_mg_f.to_excel(writer, sheet_name='Management', index=False)
    
    st.download_button(
        label="📥 Download Master API Excel Report",
        data=buffer.getvalue(),
        file_name=f"BG_API_Full_Report_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.ms-excel"
    )
    st.write("Review all 5 sheets in the downloaded file for full details.")
