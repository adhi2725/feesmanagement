
import streamlit as st
import requests
import pandas as pd
from datetime import date

API_URL = "https://db-4ish.onrender.com"

def spr():
    spr_no = st.number_input("Enter SPR No", step=1)

    if st.button("Search"):
        API_URL1 = "https://db-4ish.onrender.com/det"
        
        try:
            response = requests.get(f"{API_URL1}?spr_no={spr_no}")
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
            
def datee():
    col1, col2 = st.columns(2)
    with col1:
        from_date = st.date_input("From", date(2023, 1, 1))
    with col2:
        to_date = st.date_input("To", date.today())

    if st.button("Fetch Records"):
        res = requests.get(f"{API_URL}/bet", params={"from_date": from_date, "to_date": to_date})
        try:
            data = res.json().get("PAYMENT DETAILS", [])
            
            columns = [
                "SPR_NO", "NAME", "DEPT", "PH_NO", "TUSION_FEES", "HOSTEL_FEES",
                "MESS_FEES", "BUS_FEES", "MAINTENANCE_FEES", "DETAIL", "BILL_NO",
                "BILL_DATE", "AMT_PAYED", "METHOD"
            ]

            # Convert to DataFrame
            df = pd.DataFrame(data, columns=columns).astype(str)

            # Display results
            st.dataframe(df, use_container_width=True)

            # Download as CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Payment Detail History",
                data=csv,
                file_name=f"details.csv",
                mime="text/csv"
            )

        except Exception:
            st.error(f"❌ API Error: {res.status_code} - {res.text}")



def show_staff_dashboard():  # 👈 MAIN ENTRY FUNCTION
    st.set_page_config(page_title="Staff Dashboard", layout="wide")
    st.title("🎓 Staff Dashboard - Student & Fees Management")
    st.sidebar.write("📊 Staff Dashboard")
    st.sidebar.write(f"Welcome Staff: {st.session_state.user}")
    menu = ["Insert Student","Insert fees" ,"Update Details", "Delete Student", "View Records"]
    choice = st.sidebar.radio("Select Action", menu)
    if st.sidebar.button("Logout from staff"):
        st.session_state.page = "login"
        st.session_state.user = None
        st.rerun()
    

    def display_table(data, title):
        df = pd.DataFrame(data)
        st.subheader(title)
        st.dataframe(df, use_container_width=True)

    if choice == "Insert Student":
        st.subheader("📝 Insert Student Record")
        with st.form("insert_form"):
            col1, col2 = st.columns(2)
            with col1:
                spr_no = st.number_input("SPR No", step=1)
                name = st.text_input("Name")
                dept = st.text_input("Department")
                ph_no = st.number_input("Phone Number", step=1)
            with col2:
                tf = st.number_input("Tuition Fees", step=1)
                hf = st.number_input("Hostel Fees", step=1)
                mf = st.number_input("Mess Fees", step=1)
                mtf = st.number_input("Maintenance Fees", step=1)
                bf = st.number_input("Bus Fees", step=1)
            submit = st.form_submit_button("Insert")

        if submit:
            params = dict(
                spr_no=spr_no, name=name, dept=dept, ph_no=ph_no,
                tusion_fees=tf, hostel_fees=hf, mess_fees=mf,
                maintances_fees=mtf, bus_fees=bf
            )
            res = requests.get(f"{API_URL}/insert/", params=params)
            try:
                st.success(res.json().get("Message", "Inserted successfully."))
            except ValueError:
                st.error(f"❌ API Error: {res.status_code} - {res.text}")
        st.markdown("---")
        st.subheader("📂 Bulk Upload from CSV/Excel")

        uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("Preview:", df.head())
            if st.button("Upload to Database"):
    # Reset pointer to the start of the file
                uploaded_file.seek(0)

    # Send file as multipart/form-data
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"{API_URL}/bulk_insert_file/", files=files)

                if response.status_code == 200:
                    st.success(response.json())
                else:
                    st.error(f"Error: {response.text}")

                
    elif choice == "Insert fees":
        st.subheader("📝 Insert fees Record")
        with st.form("insert.fees_form"):
            col1, col2 = st.columns(2)
            with col1:
                spr_no = st.number_input("SPR No", step=1)
                bill_no = st.number_input("Bill No")
                amt_payed = st.number_input("Amount Payed")
            with col2:
                details = st.text_input("Details of fees")
                bill_date = st.date_input("Date of the Bill")
                method = st.text_input("Method of the payment")
            submit = st.form_submit_button("Insert")

        if submit:
            params = dict(
                spr_no=spr_no, details=details, bill_no=bill_no, bill_date=bill_date,
                amt_payed=amt_payed, method=method,
            )
            res = requests.get(f"{API_URL}/fees/", params=params)
            try:
                st.success(res.json().get("Message", "Inserted successfully."))
            except ValueError:
                st.error(f"❌ API Error: {res.status_code} - {res.text}")

    elif choice == "Update Details":
        st.subheader("✏️ Update Student Field")
        spr_no = st.number_input("Enter SPR No to update", step=1)
        field = st.selectbox("Field to update", ["name", "dept", "ph_no", "tusion_fees", "hostel_fees", "mess_fees", "bus_fees", "maintances_fees"])
        new_value = st.text_input("New value")

        if st.button("Update"):
            route = {
                "name": "update2", "dept": "update3", "ph_no": "update4",
                "tusion_fees": "update5", "hostel_fees": "update6",
                "mess_fees": "update8", "bus_fees": "update7", "maintances_fees": "update9"
            }[field]
            try:
                val = int(new_value) if field not in ["name", "dept"] else new_value
                res = requests.patch(f"{API_URL}/{route}", params={"spr_no": spr_no, field: val})
                st.success(res.json().get("Message", "Updated successfully."))
            except:
                st.error("Invalid input or server error.")

    elif choice == "Delete Student":
        st.subheader("🗑️ Delete Student Record")
        spr_no = st.text_input("Enter SPR No to delete")
        if st.button("Delete"):
            res = requests.get(f"{API_URL}/delete", params={"spr_no": spr_no})
            try:
                st.success(res.json().get("message", "Deleted successfully."))
            except:
                st.error(f"❌ API Error: {res.status_code} - {res.text}")

    
    elif choice == "View Records":
        
        
        tab1, tab2, tab3, tab4, tab5  = st.tabs(["🎓 Students", "💳 Payments", "📊 Combined View","🔍 Search by SPR","📅 Search by Date" ])

        with tab1:
            res = requests.get(f"{API_URL}/view")
            if res.ok:
                try:
                    data = res.json().get("STUDENT DETAILS", [])
                    #display_table(data.get("STUDENT DETAILS", [])
                    columns = [
                    "SPR_NO", "NAME", "DEPT", "PHONE_NO", "TUSION_FEES", "HOSTEL_FEES",
                    "MESS_FEES", "BUS_FEES", "MAINTENANCE_FEES"]
                    df = pd.DataFrame(data, columns=columns).astype(str)
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Download Payment History",
                        data=csv,
                        file_name=f"studen details.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"Error parsing student data: {e}")
                    st.text(res.text)
            else:
                st.error(f"Failed to fetch student data: {res.status_code}")
                st.text(res.text)

        with tab2:
            res = requests.get(f"{API_URL}/view2")
            if res.ok:
                try:
                    data = res.json().get("PAYMENT DETAILS", [])
                    #display_table(data.get("PAYMENT DETAILS", []), "Payment Records")
                    columns = [ "SPR_NO", "DETAILS","BILL_NO","BILL_DATE","AMOUNT_PAYED","METHOD_OF PAY"]
                    df = pd.DataFrame(data, columns=columns).astype(str)
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Download Payment History",
                        data=csv,
                        file_name=f"studentsfeedetails.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Error parsing payment data: {e}")
                    st.text(res.text)
            else:
                st.error(f"Failed to fetch payment records: {res.status_code}")
                st.text(res.text)

        with tab3:
            res = requests.get(f"{API_URL}/all")
            if res.ok:
                try:
                    data = res.json().get("PAYMENT DETAILS", [])
                    # display_table(data.get("PAYMENT DETAILS", []), "Full Joined View")
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
                        label="⬇️ Download ENTIER History",
                        data=csv,
                        file_name=f"studentsfee_history.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"Error parsing joined view: {e}")
                    st.text(res.text)
            else:
                st.error(f"Failed to fetch full view: {res.status_code}")
                st.text(res.text)
                
        with tab4:
            spr()
            
        with tab5:
            datee()

