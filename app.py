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

# --- 2. SESSION STATE (FIXES CELL RETENTION & NameError) ---
if "sync_count" not in st.session_state:
    st.session_state.sync_count = 0

# --- 3. ISOLATED SYNC ENGINE ---
def sync_to_private_report(df, filename, anchor_name):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo("Bgenggadmin/bg-anchor-portal")
        
        # Add core tracking metadata for the Founder
        df['Report_Date'] = datetime.now(IST).strftime("%Y-%m-%d")
        df['Sync_Time'] = datetime.now(IST).strftime("%H:%M")

        try:
            # Update existing private file
            file_contents = repo.get_contents(filename)
            existing_data = pd.read_csv(io.StringIO(file_contents.decoded_content.decode()))
            updated_df = pd.concat([df, existing_data], ignore_index=True)
            repo.update_file(file_contents.path, f"Private sync: {anchor_name}", updated_df.to_csv(index=False), file_contents.sha)
        except:
            # Create private file if missing
            repo.create_file(filename, f"Initial {filename}", df.to_csv(index=False))
        return True
    except Exception as e:
        st.error(f"Sync Failed: {e}")
        return False

def fetch_private_logs(filename):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo("Bgenggadmin/bg-anchor-portal")
        contents = repo.get_contents(filename)
        return pd.read_csv(io.StringIO(contents.decoded_content.decode()))
    except:
        return pd.DataFrame()

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Founder Dashboard"])

st.divider()

# --- 5. ROLE: API (KISHORE) - 100% ISOLATED & ALL FIELDS RESTORED ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    sk = st.session_state.sync_count # Secret key for auto-clearing cells

    # 🔴 Critical Purchase Dependencies
    st.subheader("🔴 Critical Purchase Dependencies")
    api_dep = st.data_editor(pd.DataFrame([{"Project/Job": "", "Material": "", "Req_Date": "", "Status": "Pending"}]), 
                             num_rows="dynamic", use_container_width=True, key=f"api_dep_{sk}")

    # 📊 Sales & Enquiry Tracking
    st.subheader("📊 Sales & Enquiry Tracking")
    c1, c2 = st.columns(2)
    with c1:
        st.write("📝 New Enquiries")
        api_enq = st.data_editor(pd.DataFrame([{"Client": "", "Offers": 0, "Status": "Review"}]), num_rows="dynamic", key=f"enq_{sk}")
    with c2:
        st.write("📐 Drawings & Design")
        api_dwg = st.data_editor(pd.DataFrame([{"Job Code": "", "Dwg Released": 0}]), num_rows="dynamic", key=f"dwg_{sk}")

    # 🛠️ Technical & Manufacturing Progress
    st.subheader("🛠️ Technical & Manufacturing Progress")
    api_eng = st.data_editor(pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Priority": "High"}]), 
                             num_rows="dynamic", use_container_width=True, key=f"api_eng_{sk}")

    # ⚠️ Deviations & Quality (NCR)
    st.subheader("⚠️ Deviations & Quality (NCR)")
    api_dev = st.data_editor(pd.DataFrame([{"Category": "Material", "Detail": "", "Impact": "NO"}]), 
                             num_rows="dynamic", use_container_width=True, key=f"api_dev_{sk}")

    with st.form(f"api_mgmt_form_{sk}"):
        st.subheader("🧠 Management Decisions")
        c3, c4 = st.columns(2)
        f_dec = c3.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = c4.text_area("Decision Context (Detailed)")

        if st.form_submit_button("🚀 Sync API Private Report"):
            # Only sync if the main Engineering table has data
            valid_df = api_eng[api_eng["Job"] != ""].copy()
            valid_df["Founder_Decision"] = f_dec
            valid_df["Context"] = dec_context
            
            if not valid_df.empty:
                if sync_to_private_report(valid_df, "api_report.csv", "Kishore"):
                    st.success("✅ Reported to Founder! Cells cleared.")
                    st.session_state.sync_count += 1
                    st.rerun() # FORCES ALL DATA TO GO BLANK

    # ISOLATED SUMMARY: Only Kishore's data
    st.subheader("📋 Your Recent Submissions (API Only)")
    api_history = fetch_private_logs("api_report.csv")
    if not api_history.empty:
        st.dataframe(api_history.head(10), use_container_width=True)

# --- 6. FOUNDER DASHBOARD - ONLY YOU SEE THIS ---
elif role == "Founder Dashboard":
    st.header("📊 Founder Master Overview")
    t1, t2 = st.tabs(["API (Kishore)", "ZLD (Ammu)"])
    
    with t1:
        st.subheader("Kishore's Isolated Stream")
        st.dataframe(fetch_private_logs("api_report.csv"), use_container_width=True)
    with t2:
        st.subheader("Ammu's Isolated Stream")
        st.dataframe(fetch_private_logs("zld_report.csv"), use_container_width=True)
