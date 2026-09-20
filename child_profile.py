import streamlit as st
import pandas as pd
from child_nutrition import get_nutrition_needs # Import fungsi kebutuhan nutrisi
from config import navigate_to # Import fungsi navigasi

def child_profile_page():
    """Definisi halaman Kelola Profil Anak Streamlit."""
    st.title("👶 Kelola Profil Anak")
    st.subheader("Daftarkan atau perbarui data anak Anda.")
    
    if st.button("← Kembali ke Home"):
        navigate_to('home')
        st.rerun()
        
    st.markdown("---")
    st.subheader("Tambahkan Anak Baru")

    # --- Bagian Form Tambah Anak ---
    with st.form("add_child_form", clear_on_submit=True):
        child_name = st.text_input("Nama Anak")
        child_age = st.number_input("Umur (Tahun)", min_value=1, max_value=18, step=1) 
        child_gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        child_height = st.number_input("Tinggi Badan (cm)", min_value=50, max_value=200, step=1)
        child_weight = st.number_input("Berat Badan (kg)", min_value=5.0, max_value=100.0, step=0.1)
        
        add_button = st.form_submit_button("Simpan Data Anak", type="primary")
        
        if add_button:
            if child_name:
                nutri_needs_data = get_nutrition_needs(child_age, child_gender)
                
                # Logika: Tentukan Status Berat/Tinggi (Sama seperti di apps.py)
                status = "Data tidak lengkap"
                bmi = None
                if child_height > 0:
                    bmi = child_weight / ((child_height / 100) ** 2)
                    if bmi < 18.5:
                        status = "Berat Badan Kurang (Underweight)"
                    elif bmi >= 18.5 and bmi < 25:
                        status = "Berat Badan Ideal"
                    elif bmi >= 25 and bmi <30:
                        status = "Kelebihan berat badan"
                    elif bmi >= 30:
                        status = "Obesitas"
                    else:
                        status = "Tidak Terdefinisi"
                else:
                    status = "Tinggi badan belum diisi"
                    
                
                new_child = {
                    "name": child_name,
                    "age": child_age,
                    "gender": child_gender,
                    "height": child_height,
                    "weight": child_weight,
                    "bmi": f"{bmi:.2f}" if bmi else "N/A",
                    "nutri_needs": nutri_needs_data if nutri_needs_data else "Data tidak ditemukan", 
                    "bmi_status": status,
                    "meal_history": [] 
                }
                
                current_email = st.session_state['current_user_email']
                st.session_state['user_data'][current_email]['children'].append(new_child)
                
                st.success(f"Profil **{child_name}** berhasil ditambahkan!")
                st.markdown(f"**Status Berat/Tinggi:** `{status}`")
                
            else:
                st.error("Nama anak harus diisi.")

    st.markdown("---")
    # --- Bagian Tampilkan Daftar Anak (Opsional: untuk edit/delete) ---
    current_email = st.session_state['current_user_email']
    user_children = st.session_state['user_data'][current_email]['children']
    
    if user_children:
        st.subheader("Daftar Anak Terdaftar")
        df_children = pd.DataFrame([
            {"Nama": c['name'], "Usia (Tahun)": c['age'], "Jenis Kelamin": c['gender'], "Status BMI": c['bmi_status']}
            for c in user_children
        ])
        st.dataframe(df_children, use_container_width=True)
    else:
        st.info("Belum ada anak terdaftar. Gunakan formulir di atas untuk menambahkan.")