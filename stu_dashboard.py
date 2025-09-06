import streamlit as st
import pandas as pd
import requests

API_URL = "https://db-4ish.onrender.com/det"

def show_student_dashboard():
    st.title("🎓 Student Dashboard")
    if st.sidebar.button("Logout"):
        st.session_state.page = "login"
        st.session_state.user = None
        st.rerun()

    # Validate session
    if "user" not in st.session_state or not st.session_state.user:
        st.warning("⚠️ Student ID not found in session. Please log in again.")
        st.stop()

    spr_no = st.session_state.user
    st.markdown(f"Welcome, Student **{spr_no}**")
    st.markdown("📄 **Fee Payment History**")

    try:
        # Fetch payment history from API
        response = requests.get(f"{API_URL}?spr_no={spr_no}")
        if response.status_code != 200:
            st.error("❌ Failed to fetch data from the server.")
            return

        data = response.json().get("PAYMENT DETAILS", [])

        if not data:
            st.info("No payment records found.")
            return

        # Define columns matching the API response
        columns = [
            "SPR_NO", "NAME", "DEPT", "PH_NO", "TUSION_FEES", "HOSTEL_FEES",
            "MESS_FEES", "BUS_FEES", "MAINTENANCE_FEES", "DETAIL", "BILL_NO",
            "BILL_DATE", "AMT_PAYED", "METHOD"
        ]

        # Convert to DataFrame with string casting to avoid Arrow errors
        df = pd.DataFrame(data, columns=columns).astype(str)

        # Display payment history table
        st.dataframe(df, use_container_width=True)

        # Provide download option as CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Payment History",
            data=csv,
            file_name=f"student_{spr_no}_fee_history.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
