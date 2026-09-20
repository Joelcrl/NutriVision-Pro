# auth.py

import streamlit as st
import os 
import base64
from config import navigate_to, hash_password, LOGO_PATH 

# Path ke wallpaper
WALLPAPER_PATH = "assets/wallpaper_auth.jpg" 

def get_base64_image(image_path):
    """Membaca gambar dan mengkonversinya ke Base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Error: File tidak ditemukan di path: {image_path}. Memuat latar belakang default.")
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

def custom_css():
    """Menginjeksikan CSS untuk kustomisasi tampilan dan menyembunyikan sidebar."""
    
    bg_image_base64 = get_base64_image(WALLPAPER_PATH)
    logo_base64 = get_base64_image(LOGO_PATH) 

    bg_style = f"""
    <style>
    /* BACKGROUND GAMBAR DARI BASE64 */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{bg_image_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* MENYEMBUNYIKAN SIDEBAR DAN TOMBOL HAMBURGER */
    [data-testid="stSidebar"], [data-testid="stDecoration"] {{
        display: none !important;
        width: 0 !important;
    }}
    [data-testid="stAppViewBlockContainer"] {{
        padding-left: 20px;
        padding-right: 20px;
        max-width: 100% !important;
    }}
    
    /* MODIFIKASI: Wrapper Form Transparan di Tengah */
    /* Kita modifikasi .centered-container untuk menampung elemen-elemen secara terpusat,
       tetapi kita HAPUS background-color putihnya. 
       Kami tambahkan background putih HANYA PADA FORM untuk keterbacaan input. */
    .centered-content-wrapper {{
        /* Kontainer Utama untuk Centering */
        margin-top: 5px; 
        width: 100%;
        max-width: 450px; 
    }}
    
    /* Style Logo di Halaman Auth */
    .auth-logo {{
        display: block; 
        margin-left: auto;
        margin-right: auto;
        width: 400px; 
        height: auto;
        margin-bottom: 15px; 
    }}

    /* KUSTOMISASI JUDUL UTAMA (H1 & H3) */
    .auth-title, .auth-subtitle, .centered-content-wrapper h2 {{
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.7); /* Memberi bayangan agar terlihat di background yang ramai */
        color: white !important; /* Ubah warna teks utama menjadi putih agar kontras dengan background */
    }}
    .auth-title {{
        text-align: center; 
        font-size: 3em; 
        font-weight: 800; 
        margin-bottom: 5px;
    }}
    .auth-subtitle {{
        text-align: center; 
        font-size: 1.5em; 
        font-weight: 600; 
        margin-bottom: 20px;
        color: black !important;
    }}

    /* KUSTOMISASI SUBJUDUL ("Masuk ke Akun Anda") */
    .centered-content-wrapper h2 {{
        font-weight: 700;
        font-size: 1.6em; 
        margin-top: 20px; 
        margin-bottom: 15px; 
        border-bottom: 2px solid #ccc; 
        padding-bottom: 5px;
    }}
    
    /* BARU: Memberi latar belakang putih HANYA pada Formulir Input Streamlit */
    .stForm {{
        background-color: rgba(255, 255, 255, 0.9); /* Kotak Putih Transparan pada Form Saja */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}


    /* KUSTOMISASI INPUT BAR (Hitam) */
    [data-testid="stTextInput"] > div > div > input,
    [data-testid="stTextInput"] > div > input {{
        background-color: black !important;
        color: white !important; 
        border-color: #333333 !important; 
        font-weight: 600;
    }}
    [data-testid="stWidgetLabel"] > div {{
        color: black !important; 
        font-weight: 700;
        font-size: 1.1em;
    }}

    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)
    return logo_base64 


# --- FUNGSI UTAMA ---

def logout():
    """Fungsi untuk logout dan reset state."""
    st.session_state['logged_in'] = False
    st.session_state['current_user_email'] = None
    navigate_to('login')
    st.success("Anda berhasil logout.")
    st.rerun()

def login_page():
    """Halaman Streamlit untuk Login (Full Background, Tanpa Kotak Putih)."""
    
    logo_base64 = custom_css() # Panggil CSS dan ambil base64 logo
    logo_html = f"""<img src="data:image/png;base64,{logo_base64}" class="auth-logo">"""
    
    # Menggunakan wrapper untuk centering, tetapi tanpa background putih
    st.markdown('<div class="centered-content-wrapper">', unsafe_allow_html=True)
    
    # Konten Teks di luar form (Transparan)
    st.markdown(f"""
        <div class="header-box">
            {logo_html} 
            <h2 class='auth-subtitle'>Selamat datang kembali, Bunda!</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<h2>Masuk ke Akun Anda</h2>", unsafe_allow_html=True)
        
    # Formulir Login (Memiliki background putih melalui CSS .stForm)
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="contoh@domain.com")
        password = st.text_input("Password", type="password", placeholder="Masukkan kata sandi Anda")
        
        login_button = st.form_submit_button("Masuk", type="primary", use_container_width=True)
        
        # --- Logika Otentikasi tetap sama ---
        if login_button:
            if email in st.session_state['user_data']:
                stored_hash = st.session_state['user_data'][email]['password_hash']
                input_hash = hash_password(password)
                
                if input_hash == stored_hash:
                    st.session_state['logged_in'] = True
                    st.session_state['current_user_email'] = email
                    navigate_to('home')
                    st.rerun()
                else:
                    st.error("Password salah. Silakan coba lagi.")
            else:
                st.error("Email belum terdaftar.")

    st.markdown("<hr style='border-top: 2px solid white;'>", unsafe_allow_html=True) 
    
    st.markdown("<p style='text-align: center; color: black;'>Belum punya akun?</p>", unsafe_allow_html=True)
    if st.button("Daftar Sekarang", use_container_width=True, key='go_to_register'):
        navigate_to('register')
        st.rerun()
        
    st.markdown("</div>", unsafe_allow_html=True) # Tutup div kustom


def register_page():
    """Halaman Streamlit untuk Register (Full Background, Tanpa Kotak Putih)."""
    
    logo_base64 = custom_css() 
    logo_html = f"""<img src="data:image/png;base64,{logo_base64}" class="auth-logo">"""

    # Menggunakan wrapper untuk centering, tetapi tanpa background putih
    st.markdown('<div class="centered-content-wrapper">', unsafe_allow_html=True)

    # Konten Teks di luar form (Transparan)
    st.markdown(f"""
        {logo_html}
        <h1 class='auth-title'>Register Akun Baru</h1>
        <h3 class='auth-subtitle'>Bergabunglah dengan NutriVisionPro!</h3>
        <hr style='border-top: 2px solid white;'>
        <h2>Daftarkan Akun Anda</h2>
    """, unsafe_allow_html=True)

    st.info("Ayo daftarkan akun Bunda untuk memulai pemantauan gizi anak.")

    # Formulir Register (Memiliki background putih melalui CSS .stForm)
    with st.form("register_form"):
        email = st.text_input("Email (akan menjadi username Anda)", placeholder="Masukkan email aktif Anda")
        password = st.text_input("Password", type="password", placeholder="Minimal 6 karakter")
        confirm_password = st.text_input("Konfirmasi Password", type="password", placeholder="Ulangi kata sandi")
        
        register_button = st.form_submit_button("Daftar Akun", type="primary", use_container_width=True)

        # --- Logika Registrasi tetap sama ---
        if register_button:
            if email in st.session_state['user_data']:
                st.error("Email ini sudah terdaftar. Silakan login atau gunakan email lain.")
            elif not email or not password or not confirm_password:
                st.error("Semua kolom harus diisi.")
            elif password != confirm_password:
                st.error("Konfirmasi password tidak cocok.")
            else:
                st.session_state['user_data'][email] = {
                    "password_hash": hash_password(password),
                    "children": []
                }
                st.success("Registrasi berhasil! Silakan Login.")
                navigate_to('login')
                st.rerun()

    st.markdown("<hr style='border-top: 2px solid white;'>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: white;'>Sudah punya akun?</p>", unsafe_allow_html=True)
    if st.button("Masuk di Sini", use_container_width=True, key='go_to_login'):
        navigate_to('login')
        st.rerun()
        
    st.markdown("</div>", unsafe_allow_html=True)