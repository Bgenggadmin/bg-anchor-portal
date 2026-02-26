import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="B&G Anchor Portal", layout="wide")

# --- DATA LOADING ---
def load_data():
    try:
        df = pd.read_csv("master_log.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        return pd.DataFrame()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("B&G Digitalization")
role = st.sidebar.radio("Select Role", ["Purchase (Santhoshi)", "API (Kishore)", "ZLD (Ammu)", "Management Dashboard"])

# --- 5:30 PM NOTIFICATION LOGIC ---
now = datetime.now().time()
if now >= datetime.strptime("17:30", "%H:%M").time():
    st.sidebar.warning("⏰ It is past 5:30 PM. Please ensure your EOD report is submitted before closing.")

# --- APP LOGIC: ENTRY FORMS ---
if role in ["API (Kishore)", "ZLD (Ammu)"]:
    st.header(f"Daily Engineering Entry - {role}")
    with st.form("tech_form"):
        col1, col2 = st.columns(2)
        project = col1.selectbox("Project", ["30KL OIL SYSTEM", "MSN REACTORS", "DIVIS UNIT-II"])
        stage = col2.text_input("Current Stage (e.g. Fabrication/Water Trails)")
        dep = st.text_area("Critical Purchase Dependency", help="Specific items needed from Santhoshi")
        decision = st.selectbox("Founder Decision Required?", ["No", "Yes"])
        details = st.text_input("Decision Details")
        
        if st.form_submit_button("Submit EOD Report"):
            # Logic to append to master_log.csv goes here
            st.success("Data synced to Master Log.")

elif role == "Purchase (Santhoshi)":
    st.header("Purchase & Operations Entry")
    # Cross-functional View: See what others need
    st.subheader("⚠️ Pending Indents from API/ZLD")
    df = load_data()
    pending = df[df['Critical_Purchase_Dependency'].notna()]
    st.table(pending[['Date', 'Project', 'Critical_Purchase_Dependency']])
    
    with st.expander("Update Purchase Status"):
        res = st.text_input("Enter Response (e.g., PO Issued)")
        st.button("Update Technical Anchors")

# --- DASHBOARD & FILTERS ---
if role == "Management Dashboard":
    st.header("B&G Analytics (Day/Week/Month)")
    df = load_data()
    
    period = st.select_slider("View Range", options=["Daily", "Weekly", "Monthly"])
    
    if period == "Weekly":
        df['Display_Date'] = df['Date'].dt.to_period('W').astype(str)
    elif period == "Monthly":
        df['Display_Date'] = df['Date'].dt.to_period('M').astype(str)
    else:
        df['Display_Date'] = df['Date'].dt.date

    st.dataframe(df)
    
    # DOWNLOAD BUTTON (Replacing Excel)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Data as Excel/CSV", data=csv, file_name="BG_Report.csv")
