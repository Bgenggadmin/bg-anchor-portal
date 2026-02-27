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
        
        # Standardize date formats for the CSV
        if 'Req_Date' in df.columns:
            df['Req_Date'] = pd.to_datetime(df['Req_Date']).dt.strftime('%Y-%m-%d')
            
        df['Entry_Date'] = datetime.now(IST).strftime("%Y-%m-%d")
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

# --- 5. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")

    # 1. Purchase Dependencies (WITH DATE PICKER)
    st.subheader("🔴 Critical Purchase Dependencies")
    
    # Define the structure with a default date
    init_pur_df = pd.DataFrame([{"Job": "", "Material": "", "Req_Date": date.today(), "Urgency": "High"}])
    
    api_pur = st.data_editor(
        init_pur_df, 
        num_rows="dynamic", 
        use_container_width=True, 
        key=f"pur_{sk}",
        column_config={
            "Req_Date": st.column_config.DateColumn(
                "Required Date",
                min_value=date(2025, 1, 1),
                max_value=date(2027, 12, 31),
                format="YYYY-MM-DD",
                step=1,
            ),
            "Urgency": st.column_config.SelectboxColumn(
                "Urgency",
                options=["High", "Medium", "Low"],
                required=True,
            )
        }
    )

    # 2. Other Tables (Simplified for this snippet, keep your existing ones)
    st.subheader("🛠️ Technical Progress & Decisions")
    with st.form(f"mgmt_form_{sk}"):
        api_mfg = st.data_editor(pd.DataFrame([{"Job Code": "", "Status": "Ongoing"}]), 
                                 num_rows="dynamic", key=f"mfg_{sk}")
        f_dec = st.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = st.text_area("Decision Context")
        
        if st.form_submit_button("🚀 SYNC ALL REPORTS"):
            # Sync Purchase with Date Formatting
            sync_to_private_file(api_pur[api_pur["Job"] != ""], "api_purchase.csv")
            sync_to_private_file(api_mfg[api_mfg["Job Code"] != ""], "api_manufacturing.csv")
            
            st.success("✅ Reports Synced! Calendar dates saved.")
            st.session_state.sync_count += 1
            st.rerun()

    # 3. INDEPENDENT SUMMARY
    st.divider()
    st.subheader("📋 Recent Submission Summary (API)")
    st.dataframe(fetch_logs("api_purchase.csv"), use_container_width=True)

# --- 6. FOUNDER DASHBOARD ---
elif role == "Founder Dashboard":
    st.header("📊 Founder Master Overview")
    # ... (Excel Download code from previous turn)
