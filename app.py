# --- 1. SESSION STATE FOR CLEARING CELLS ---
# Add this at the very top of your code, after imports
if "sync_count" not in st.session_state:
    st.session_state.sync_count = 0

# Function to clear cells
def reset_form():
    st.session_state.sync_count += 1
    st.rerun()

# --- 4. ROLE: API (KISHORE) ---
if role == "API (Kishore)":
    st.header("🏢 API Site Entry - Kishore Anchor")
    
    # We add the sync_count to the key to force it to clear after sync
    current_key = f"api_eng_{st.session_state.sync_count}"
    
    st.subheader("🛠️ Technical & Manufacturing Progress")
    # Using the dynamic key here is the secret to clearing the cells
    api_eng_data = st.data_editor(
        pd.DataFrame([{"Job": "", "Clarification": "", "Ageing": 0, "Priority": "High"}]), 
        num_rows="dynamic", 
        use_container_width=True, 
        key=current_key
    )

    if st.button("🚀 Sync API Master Report"):
        valid_data = api_eng_data[api_eng_data["Job"] != ""].copy()
        
        if not valid_data.empty:
            # 1. Trigger Sync
            if sync_data_to_github("bg-api-logs", "engineering_audit.csv", valid_data, "Kishore"):
                st.success("✅ Data Synced to GitHub Cloud!")
                st.balloons()
                # 2. Reset the Form (Clears all cells)
                reset_form()
        else:
            st.warning("⚠️ Cannot sync an empty table. Please enter Job details.")
