
import streamlit as st
import os 

from config import navigate_to, model, class_names, LOGO_PATH 
from auth import login_page, register_page, logout 
from home import home_page
from child_profile import child_profile_page
from scan import scan_page
import base64

MAIN_PAGE_WALLPAPER_PATH = "assets/wallpaper_main.jpg"

def get_base64_image(image_path):
    """Membaca gambar dan mengkonversinya ke Base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        print(f"Error: File wallpaper tidak ditemukan di path: {image_path}.")
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="


def set_main_page_background():
    """css buat halaman pertama"""
    
    bg_image_base64 = get_base64_image(MAIN_PAGE_WALLPAPER_PATH)

    bg_style = f"""
    <style>
    /*BACKGROUND UTAMA */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{bg_image_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)


def custom_sidebar_css():
    """css untuk sidebar"""
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background-color: black;
            color: white; 
        }}
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] label {{
            color: white !important;
        }}
        [data-testid="stSidebar"] .stButton > button {{
            background-color: white !important; 
            border: 1px solid black; 
        }}
        
        [data-testid="stSidebar"] .stButton > button *,
        [data-testid="stSidebar"] .stButton > button {{
            color: black !important; 
            /* Catatan: Selektor * akan menargetkan span dan div yang berisi teks/emoji */
        }}

        [data-testid="stSidebar"] .stButton > button:hover {{
            background-color: #f0f0f0 !important; 
        }}
        
        [data-testid="stSidebar"] .stButton > button:hover *,
        [data-testid="stSidebar"] .stButton > button:hover {{
            color: black !important;
        }}

        [data-testid="stSidebar"] hr {{
            border-top: 1px solid #444444; 
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="NutriVisionPro", layout="wide")
custom_sidebar_css()
set_main_page_background()

if st.session_state['logged_in']:
    
    if os.path.exists(LOGO_PATH):
        st.sidebar.image(LOGO_PATH, use_column_width='always') 
    else:
        st.sidebar.warning(f"Logo file not found at: {LOGO_PATH}") 
    
    st.sidebar.markdown("---") 

    st.sidebar.header(f"Halo, Bunda!")
    st.sidebar.markdown(f"User: `{st.session_state['current_user_email']}`")
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("Home Dashboard", use_container_width=True):
        navigate_to('home')
        st.rerun()
    if st.sidebar.button("Kelola Profil Anak", use_container_width=True):
        navigate_to('child_profile')
        st.rerun()
    if st.sidebar.button("Scan & Catat Buah", use_container_width=True):
        navigate_to('scan')
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.button("🔒 Logout", on_click=logout, use_container_width=True)

if st.session_state['logged_in']:
    if st.session_state['current_page'] == 'home':
        home_page()
    elif st.session_state['current_page'] == 'child_profile':
        child_profile_page()
    elif st.session_state['current_page'] == 'scan':
        scan_page()
    else:
        navigate_to('home')
        st.rerun()
else:
    if st.session_state['current_page'] == 'register':
        register_page()
    else: 
        login_page()