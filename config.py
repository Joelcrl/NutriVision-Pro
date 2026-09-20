import streamlit as st
import json
import os
import hashlib
from child_nutrition import childNutrition_Requirements, get_nutrition_needs 

# Try to import tensorflow, but make it optional
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    tf = None
    TF_AVAILABLE = False

MODEL_PATH = "model/fruit_classifier.h5"
CLASS_NAMES_PATH = "model/class_names.json"
IMAGE_SIZE = (224, 224)
LOGO_PATH = "assets/logo.png"

@st.cache_resource
def load_resources():
    model = None
    class_names = []
    
    # Only try to load model if TensorFlow is available
    if not TF_AVAILABLE:
        st.sidebar.warning("⚠️ TensorFlow not available - fruit classification disabled")
        return None, []
    
    if os.path.exists(MODEL_PATH):
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
        except Exception as e:
            st.sidebar.warning(f"Warning: Could not load model: {e}. Classification will be skipped.")
    else:
        st.sidebar.warning(f"Warning: Model file not found at {MODEL_PATH}. Classification will be skipped.")

    if os.path.exists(CLASS_NAMES_PATH):
        try:
            with open(CLASS_NAMES_PATH, "r") as f:
                class_names = json.load(f)
        except Exception as e:
            st.sidebar.error(f"Error loading class names: {e}")
    else:
        st.sidebar.warning(f"Warning: Class names file not found at {CLASS_NAMES_PATH}.")

    return model, class_names

model, class_names = load_resources() 

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'login'
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {
        "demo@example.com": {"password_hash": "e99a18c428cb38d5f260853678922e03", "children": []}
    }
if 'current_user_email' not in st.session_state:
    st.session_state['current_user_email'] = None

def navigate_to(page):
    """Fungsi untuk navigasi antar halaman."""
    st.session_state['current_page'] = page

def hash_password(password):
    """Hash password menggunakan MD5."""
    return hashlib.md5(password.encode()).hexdigest()
