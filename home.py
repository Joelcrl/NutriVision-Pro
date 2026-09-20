import streamlit as st
import pandas as pd
from child_nutrition import get_nutrition_needs 
from config import navigate_to 

def home_page():
    email = st.session_state['current_user_email']
    user = st.session_state['user_data'][email]
    
    st.title(f"Selamat Datang, Bunda!")

    st.header("Ringkasan Kebutuhan Nutrisi Anak")
    
    if not user['children']:
        st.info("Belum ada data anak yang terdaftar. Silakan tambahkan profil anak.")
        st.button("➕ Kelola Profil Anak", on_click=lambda: navigate_to('child_profile'))
        return # Keluar dari fungsi jika tidak ada anak

    st.info(f"Anda memiliki **{len(user['children'])}** data anak.")
    st.subheader("Kebutuhan Nutrisi Harian yang Direkomendasikan")

    for child_index, child_data in enumerate(user['children']):
        
        TARGET_KEY = f'target_nutrisi_{child_index}'
        CURRENT_KEY = f'nutrisi_hari_ini_{child_index}'
        
        child_name = child_data.get('name', f"Anak #{child_index + 1}")
        age = child_data.get('age') 
        gender = child_data.get('gender')
        weight = child_data.get('weight')
        height = child_data.get('height')

        if age is not None and gender:
            try:
                age = int(age)
                
                nutrition_needs = get_nutrition_needs(age, gender) 
                
                st.markdown(f"### 👶 {child_name} (Usia **{age}** tahun, **{gender}**)")
                
                if weight and height:
                    st.markdown(f"**Berat:** {weight} kg | **Tinggi:** {height} cm")

                if nutrition_needs:
                    
                    if TARGET_KEY not in st.session_state:
                        st.session_state[TARGET_KEY] = nutrition_needs
                        st.session_state[CURRENT_KEY] = {key: 0 for key in nutrition_needs.keys()}
                    
                    current_target = st.session_state[TARGET_KEY]
                    current_progress = st.session_state[CURRENT_KEY]
                    
                    st.header("📋 Target Kebutuhan Harian")
                    display_needs = []
                    
                    for key, value in current_target.items():
                        unit = " µg" 
                        display_value = value
                        
                        if key == "water":
                            if value >= 1_000_000:
                                display_value = value / 1_000_000
                                unit = " Liter"
                            else:
                                display_value = value / 1_000 
                                unit = " mL"
                        elif key == "fiber":
                            display_value = value / 1_000
                            unit = " g"
                        elif key == "calories": 
                            unit = " kkal"
                            display_value = value
                        elif value >= 1000 and value < 1_000_000: 
                            display_value = value / 1000
                            unit = " mg"
                        
                        display_key = key.replace('vitaminb', 'Vitamin B').replace('vitamina', 'Vitamin A').replace('vitamine', 'Vitamin E').replace('vitamink', 'Vitamin K').title()
                        display_key = display_key.replace('Water', 'Air').replace('Fiber', 'Serat').replace('Calories', 'Kalori')
                        
                        formatted_value = f"{display_value:.2f}".rstrip('0').rstrip('.')
                        
                        display_needs.append({
                            "Nutrisi": display_key, 
                            "Kebutuhan Harian": f"{formatted_value}{unit}"
                        })

                    st.table(pd.DataFrame(display_needs))
                    st.markdown("---") 

                    st.header("📈 Pencapaian Hari Ini")
                    
                    for key in current_target.keys():
                        target = current_target.get(key, 1) 
                        current = current_progress.get(key, 0)
                        
                        if target > 0:
                            persentase = min(1.0, current / target) 
                        else:
                            persentase = 0.0

                        display_key = key.replace('vitaminb', 'Vitamin B').replace('vitamina', 'Vitamin A').replace('vitamine', 'Vitamin E').replace('vitamink', 'Vitamin K').title()
                        display_key = display_key.replace('Water', 'Air').replace('Fiber', 'Serat').replace('Calories', 'Kalori')

                        progress_text = f"{display_key} ({int(persentase * 100)}%)"

                        st.progress(persentase, text=progress_text)
                        
                else:
                    st.warning(f"Kebutuhan nutrisi untuk anak usia {age} tahun belum tersedia di database.")

            except ValueError:
                st.error(f"Nilai usia anak {child_name} tidak valid.")
            except Exception as e:
                 st.error(f"Terjadi kesalahan: {e}")
        else:
            st.warning(f"Data usia atau jenis kelamin untuk {child_name} tidak lengkap.")

    st.markdown("---")
    st.subheader("Aksi Cepat")
    col1, col2 = st.columns(2)
    with col1:
        st.button("📸 Scan Buah Baru", type="primary", use_container_width=True, on_click=lambda: navigate_to('scan'))
    with col2:
        st.button("➕ Kelola Profil Anak", use_container_width=True, on_click=lambda: navigate_to('child_profile'))