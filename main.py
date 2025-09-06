import streamlit as st
import requests
import base64
from verify import verify_staff_login # your custom verification
from stu_verify import verify_student_login # simple student verification
from staff_dashboard import show_staff_dashboard  # staff dash board
from student_dashboard import show_student_dashboard #student dash board



# Page configuration
st.set_page_config(page_title="Mookambigai Fees Portal", page_icon="🎓")

# Load logo and encode as base64
with open("logo.png", "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read()).decode()
    

# Render only the clean top banner
st.markdown(f"""
    <style>
        .top-banner {{
            display: flex;
            align-items: center;
            background-color:#003366;
            padding: 20px 40px;
            border-bottom: 2px solid #003366;
        }}
        .top-banner img {{
            height: 140px;
            margin-right: 20px;
        }}
        .top-banner-text h1 {{
            font-size:55px;
            font-weight:900;
            color:white;
            margin: 0;
            line-height: 0.5;
        }}
        .top-banner-text h2 {{
            font-size: 32px;
            font-weight: 600;
            color:white;
             margin: 0px 0 0;
             line-height: 0.0;
        }}
        .top-banner-text h4 {{
            font-size: 19px;
            color: #666;
            margin:0;
            font-weight: 400;
            line-height: 0.0;
        }}
    </style>

    <div class="top-banner">
        <img src="data:image/png;base64,{encoded_logo}" alt="Logo">
        <div class="top-banner-text">
            <h1>MOOKAMBIGAI</h1>
            <h2> COLLEGE OF ENGINEERING</h2>
            <h4>Approved by AICTE & Affiliated to Anna University</h4>
        </div>
    </div>
""", unsafe_allow_html=True)



if "page" not in st.session_state:
    st.session_state.page = "login"
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None

def login_page():
    st.title("Login Page")

    with st.form("login_form"):
        usertype = st.selectbox("Login as", options=["Staff", "Student"])
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if usertype == "Staff":
                if verify_staff_login(int(user_id), password):
                    st.success("✅ Staff login successful!")
                    st.session_state.page = "staff_dashboard"
                    st.session_state.user = user_id
                    st.session_state.role = "Staff"
                    st.rerun()
                    
                else:
                    st.error("❌ Invalid Staff credentials")
                    
            elif usertype == "Student":
                if verify_student_login(user_id,password):
                    st.success("✅ Student login successful!")
                    st.session_state.page = "student_dashboard"
                    st.session_state.user = user_id
                    st.session_state.role = "Student"
                    st.rerun() 
                else:
                    st.error("❌ Invalid student credentials")
                    
def staff_dashboard():
    show_staff_dashboard()  # 👈 Call the dashboard logic here




# -------- Student Dashboard --------
def student_dashboard():
    show_student_dashboard()  # Load full dashboard UI
    
# -------- Page Router --------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "staff_dashboard":
    staff_dashboard()
elif st.session_state.page == "student_dashboard":
    student_dashboard()                
