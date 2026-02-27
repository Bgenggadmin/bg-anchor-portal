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
        
        # Metadata
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

# --- 5. ROLE: API (KISHORE) - ALL 5 TABLES RESTORED ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")

    # 1. Critical Purchase Dependencies
    st.subheader("🔴 1. Critical Purchase Dependencies")
    api_pur = st.data_editor(
        pd.DataFrame([{"Job": "", "Material": "", "Req_Date": date.today(), "PO_Ref": "Pending", "Urgency": "High"}]), 
        num_rows="dynamic", use_container_width=True, key=f"pur_{sk}",
        column_config={"Req_Date": st.column_config.DateColumn("Required Date", format="YYYY-MM-DD")}
    )

    # 2. Sales & Enquiry Tracking
    st.subheader("📊 2. Sales & Enquiry Tracking")
    c1, c2 = st.columns(2)
    with c1:
        st.write("📝 New Enquiries")
        api_enq = st.data_editor(pd.DataFrame([{"Client": "", "Offers_Issued": 0, "Status": "Review"}]), 
                                 num_rows="dynamic", key=f"enq_{sk}")
    with c2:
        st.write("📐 Drawings & Design")
        api_dwg = st.data_editor(pd.DataFrame([{"Job_Code": "", "Dwg_Released": 0, "Design_Status": "Pending"}]), 
                                 num_rows="dynamic", key=f"dwg_{sk}")

    # 3. Technical & Manufacturing Progress
    st.subheader("🛠️ 3. Technical & Manufacturing Progress")
    api_mfg = st.data_editor(
        pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Planned": "", "Actual": "", "Delay_Reason": ""}]), 
        num_rows="dynamic", use_container_width=True, key=f"mfg_{sk}"
    )

    # 4. Deviations & Quality (NCR)
    st.subheader("⚠️ 4. Deviations & Quality (NCR)")
    api_ncr = st.data_editor(
        pd.DataFrame([{"Category": "Material", "Detail": "", "Impact": "NO", "NCR_Status": "Open"}]), 
        num_rows="dynamic", use_container_width=True, key=f"ncr_{sk}"
    )

    # 5. Management Decisions
    st.subheader("🧠 5. Management Decisions")
    with st.form(f"mgmt_form_{sk}"):
        f_dec = st.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = st.text_area("Decision Context (Detailed)")
        
        if st.form_submit_button("🚀 SYNC ALL 5 TABLES"):
            # Syncing all tables separately to their own CSVs
            sync_to_private_file(api_pur[api_pur["Job"] != ""], "api_purchase.csv")
            sync_to_private_file(api_enq[api_enq["Client"] != ""], "api_enquiries.csv")
            sync_to_private_file(api_dwg[api_dwg["Job_Code"] != ""], "api_drawings.csv")
            sync_to_private_file(api_mfg[api_mfg["Job"] != ""], "api_manufacturing.csv")
            sync_to_private_file(api_ncr[api_ncr["Detail"] != ""], "api_ncr.csv")
            
            # Save decision separately
            sync_to_private_file(pd.DataFrame([{"Decision": f_dec, "Details": dec_context}]), "api_decisions.csv")
            
            st.success("✅ All fields synced and cleared!")
            st.session_state.sync_count += 1
            st.rerun()

    # --- INDIVIDUAL SUMMARIES FOR KISHORE ---
    st.divider()
    st.subheader("📋 Your Recent Activity")
    st.dataframe(fetch_logs("api_manufacturing.csv").head(5), use_container_width=True)

# --- 6. FOUNDER DASHBOARD ---
elif role == "Founder Dashboard":
    st.header("📊 Founder Master Overview")
    
    # MASTER EXCEL DOWNLOAD
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        fetch_logs("api_purchase.csv").to_excel(writer, sheet_name='Purchase', index=False)
        fetch_logs("api_enquiries.csv").to_excel(writer, sheet_name='Enquiries', index=False)
        fetch_logs("api_drawings.csv").to_excel(writer, sheet_name='Drawings', index=False)
        fetch_logs("api_manufacturing.csv").to_excel(writer, sheet_name='Manufacturing', index=False)
        fetch_logs("api_ncr.csv").to_excel(writer, sheet_name='NCR_Quality', index=False)
        fetch_logs("api_decisions.csv").to_excel(writer, sheet_name='Decisions', index=False)
    
    st.download_button(
        label="📥 Download Full API Report (Excel)",
        data=output.getvalue(),
        file_name=f"BG_Full_Report_{date.today()}.xlsx",
        mime="application/vnd.ms-excel"
    )
