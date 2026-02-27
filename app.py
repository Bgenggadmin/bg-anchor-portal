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

# --- 2. SESSION STATE (FIXES CELL CLEARING) ---
if "sync_count" not in st.session_state:
    st.session_state.sync_count = 0

# --- 3. ENGINES: INDEPENDENT SYNC & FETCH ---
def sync_to_private_file(df, filename, anchor_name):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        # Update this to your exact repository name
        repo = g.get_repo("Bgenggadmin/bg-anchor-portal")
        
        # Add tracking metadata
        df['Report_Date'] = datetime.now(IST).strftime("%Y-%m-%d")
        df['Sync_Time'] = datetime.now(IST).strftime("%H:%M")
        df['Anchor'] = anchor_name

        try:
            # Update existing file
            file_contents = repo.get_contents(filename)
            existing_data = pd.read_csv(io.StringIO(file_contents.decoded_content.decode()))
            updated_df = pd.concat([df, existing_data], ignore_index=True)
            repo.update_file(file_contents.path, f"Sync: {anchor_name}", updated_df.to_csv(index=False), file_contents.sha)
        except:
            # Create file if it doesn't exist
            repo.create_file(filename, f"Initial Create: {filename}", df.to_csv(index=False))
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

# --- 4. SIDEBAR ---
st.sidebar.title("🏢 B&G Engineering")
role = st.sidebar.radio("Select Anchor Role:", 
    ["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)", "Management Dashboard"])

st.divider()

# --- 5. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    sk = st.session_state.sync_count # Reset key

    with st.form(f"api_form_{sk}"):
        st.subheader("🛠️ Technical & Manufacturing Progress")
        api_eng = st.data_editor(pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Priority": "High"}]), 
                                 num_rows="dynamic", use_container_width=True, key=f"api_editor_{sk}")
        
        st.subheader("🧠 Management Decisions")
        c1, c2 = st.columns(2)
        f_dec = c1.selectbox("Founder Decision Required?", ["NO", "YES"])
        dec_context = c2.text_area("Decision Context (Detailed)")

        if st.form_submit_button("🚀 Sync API Report"):
            valid_df = api_eng[api_eng["Job"] != ""].copy()
            valid_df["Founder_Decision"] = f_dec
            valid_df["Context"] = dec_context
            
            if not valid_df.empty:
                if sync_to_private_file(valid_df, "api_report.csv", "Kishore"):
                    st.success("✅ Reported to Founder! Cells cleared.")
                    st.session_state.sync_count += 1
                    st.rerun()

    # INDEPENDENT SUMMARY TABLE
    st.subheader("📋 Your Recent Submissions (API)")
    api_history = fetch_private_logs("api_report.csv")
    if not api_history.empty:
        st.dataframe(api_history.head(10), use_container_width=True)

# --- 6. ROLE: ZLD (AMMU) ---
elif role == "ZLD (Ammu)":
    st.header("💧 ZLD Site Entry - Ammu Anchor")
    sk = st.session_state.sync_count

    with st.form(f"zld_form_{sk}"):
        st.subheader("🏗️ Project Execution & Risks")
        zld_proj = st.data_editor(pd.DataFrame([{"Project Name": "", "Stage": "Fabrication", "Risk": "NO"}]), 
                                  num_rows="dynamic", use_container_width=True, key=f"zld_editor_{sk}")
        
        zld_context = st.text_area("Site Updates")

        if st.form_submit_button("🚀 Sync ZLD Report"):
            valid_zld = zld_proj[zld_proj["Project Name"] != ""].copy()
            valid_zld["Updates"] = zld_context
            
            if not valid_zld.empty:
                if sync_to_private_file(valid_zld, "zld_report.csv", "Ammu"):
                    st.success("✅ ZLD Data Synced!")
                    st.session_state.sync_count += 1
                    st.rerun()

    st.subheader("📋 Your Recent Submissions (ZLD)")
    zld_history = fetch_private_logs("zld_report.csv")
    if not zld_history.empty:
        st.dataframe(zld_history.head(10), use_container_width=True)

# --- 7. ROLE: PURCHASE (SANTHOSHI) ---
elif role == "Purchase (Santhoshi)":
    st.header("📦 Purchase & Operations - Santhoshi")
    sk = st.session_state.sync_count
    
    with st.form(f"pur_form_{sk}"):
        p1, p2 = st.columns(2)
        planned = p1.number_input("Planned Manpower", value=62)
        actual = p2.number_input("Actual Manpower", value=52)
        
        st.subheader("⚙️ Asset Status")
        ops = st.data_editor(pd.DataFrame([{"Asset": "Plasma", "Status": "Working"}]), 
                             num_rows="dynamic", key=f"pur_editor_{sk}")

        if st.form_submit_button("🚀 Sync Purchase Log"):
            pur_df = ops.copy()
            pur_df["Planned"] = planned
            pur_df["Actual"] = actual
            if sync_to_private_file(pur_df, "purchase_report.csv", "Santhoshi"):
                st.success("✅ Purchase Log Updated!")
                st.session_state.sync_count += 1
                st.rerun()

    st.subheader("📋 Your Recent Submissions (Purchase)")
    pur_history = fetch_private_logs("purchase_report.csv")
    if not pur_history.empty:
        st.dataframe(pur_history.head(10), use_container_width=True)

# --- 8. MANAGEMENT DASHBOARD (FOUNDER ONLY) ---
else:
    st.header("📊 Founder Master Overview")
    t1, t2, t3 = st.tabs(["API (Kishore)", "ZLD (Ammu)", "Purchase (Santhoshi)"])
    
    with t1:
        st.dataframe(fetch_private_logs("api_report.csv"), use_container_width=True)
    with t2:
        st.dataframe(fetch_private_logs("zld_report.csv"), use_container_width=True)
    with t3:
        st.dataframe(fetch_private_logs("purchase_report.csv"), use_container_width=True)
