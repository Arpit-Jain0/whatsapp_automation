import streamlit as st
import tempfile
import main_code
import time


if "page" not in st.session_state:
    st.session_state.page = "Login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None  


def show_login():
    st.markdown("<h1 style='text-align: center;'>🔒 Login Page</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1]) 
    
    with col2:  
        st.subheader("Enter your credentials")
        username = st.text_input("Enter Username", key="phone_number")
        password = st.text_input("Password", type="password", key="password")
        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "password123":
                st.success("✅ Login successful!")
                st.session_state.logged_in = True
                st.session_state.username=username
                st.session_state.page = "WhatsApp"
                time.sleep(2)
                st.rerun() 
            else:
                st.error("❌ Invalid username or password.")
            

def show_whatsapp_automation(username):
    st.markdown(f"### Welcome, **{username}**! 🎉")

    st.title("WhatsApp Message Sender")
    with st.sidebar:
       st.write("Owner name")

    col1, col2 = st.columns(2)
    with col1:
        numbers_file = st.file_uploader("📂 Upload numbers.txt", type=["txt"])
    with col2:
        image_file = st.file_uploader("🖼️ Upload an image", type=["jpg", "jpeg", "png"])
    
    message = st.text_area("Enter the message to send",height=200)
    image_path=None
    if image_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=image_file.name) as tmp_file:
            tmp_file.write(image_file.read())
            image_path = tmp_file.name
    
    if st.button("Send Messages"):
        if numbers_file and message:
            main_code.send_whatsapp_messages(numbers_file, image_path, message)
            
        else:
            st.error("Please upload a numbers file and enter a message.")



if st.session_state.page == "Login":
    st.set_page_config(page_title="Login Page", layout="centered")
    show_login()
elif st.session_state.page == "WhatsApp" and st.session_state.logged_in:
    st.set_page_config(page_title="WhatsApp Automation", layout="centered")
    show_whatsapp_automation(st.session_state.username)
else:
    st.session_state.page = "Login"
    st.experimental_rerun()
