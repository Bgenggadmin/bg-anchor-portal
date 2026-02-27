# ... (existing sidebar and header code)

if role == "API (Kishore)":
    st.header("API Site Entry - Kishore Anchor")
    with st.form("api_form"):
        # ... (other technical fields like Clarification Ageing)

        st.subheader("Operational & Purchase Integration")
        
        # 1. The Trigger
        has_dependency = st.radio("Any Critical Purchase Dependency?", ["NO", "YES"], horizontal=True)
        
        # 2. The Conditional Prompt (Must be inside the 'with st.form' block)
        if has_dependency == "YES":
            crit_dep = st.text_area("🔴 List: Project Name vs Requirement", 
                placeholder="e.g.\nMSN Maithri: 8mm 316 Plate\n30KL Oil System: 5HP Motor",
                height=150)
        
        st.subheader("Management & Decisions")
        # ... (Decision fields)

        if st.form_submit_button("Sync API Report"):
            st.success("API Data recorded.")
