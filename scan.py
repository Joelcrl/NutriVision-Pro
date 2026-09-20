import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from tensorflow.keras.preprocessing import image
from config import model, class_names, IMAGE_SIZE, navigate_to 

try:
    from nutrition_data import fruit as NUTRITION_DATA 
except ImportError:
    st.error("Gagal mengimpor data nutrisi buah dari nutrition_data.py.")
    NUTRITION_DATA = {} 

def scan_page():
    """Definisi halaman Scan Buah Streamlit."""
    
    st.title("📸 Scan Buah & Catat Makanan")
    st.subheader("Upload gambar buah untuk klasifikasi otomatis.")

    if st.button("← Kembali ke Home"):
        if 'manual_input' in st.session_state:
             del st.session_state['manual_input']
        navigate_to('home')
        st.rerun()

    st.markdown("---")

    current_email = st.session_state['current_user_email']
    user_children = st.session_state['user_data'][current_email]['children']
    
    if not user_children:
        st.warning("Silakan daftarkan anak terlebih dahulu di menu 'Kelola Profil Anak'.")
        return

    child_names = [child['name'] for child in user_children]
    selected_child_name = st.selectbox("Pilih Anak yang Akan Makan", child_names)
    selected_child_index = child_names.index(selected_child_name)

    CURRENT_KEY = f'nutrisi_hari_ini_{selected_child_index}' 

    st.markdown("---")

    uploaded_file = st.file_uploader("Pilih gambar buah...", type=['jpg', 'png', 'jpeg', 'webp', 'avif'])
    
    predicted_class = None

    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Gambar Buah yang Di-upload", use_container_width=True)
        
        if 'manual_input' not in st.session_state:
             st.session_state['manual_input'] = False 

        if model and class_names and not st.session_state['manual_input']:
            
            with st.spinner('Menganalisis gambar...'):
                img_resized = img.resize(IMAGE_SIZE) 
                img_array = image.img_to_array(img_resized) / 255.0 
                img_array = np.expand_dims(img_array, axis=0)

                preds = model.predict(img_array)
                pred_index = np.argmax(preds[0])
                confidence = np.max(preds[0]) * 100

                predicted_class = class_names[pred_index] 
            
            st.success("Analisis Selesai!")
            st.markdown(f"### Prediksi: **{predicted_class}**")
            st.markdown(f"**Keyakinan:** `{confidence:.2f}%`")
            
            if predicted_class.lower() not in NUTRITION_DATA:
                st.warning(f"Nutrisi untuk buah **{predicted_class}** tidak ditemukan di database. Beralih ke input manual.")
                st.session_state['manual_input'] = True
                predicted_class = "Unknown Fruit"

        else:
            if predicted_class is None:
                 predicted_class = "Unknown Fruit"

        if predicted_class:
            
            is_manual = st.session_state['manual_input'] or predicted_class == "Unknown Fruit"

            if not is_manual and st.button("❌ Tidak, ini buah lain", key='manual_switch'):
                st.session_state['manual_input'] = True
                st.rerun() 

            final_fruit_name = predicted_class.lower()
            
            if is_manual:
                available_fruits = sorted(list(NUTRITION_DATA.keys()))
                default_index = available_fruits.index(final_fruit_name) if final_fruit_name in available_fruits else 0

                final_fruit_name = st.selectbox(
                    "Pilih Buah Sebenarnya", 
                    options=available_fruits,
                    index=default_index,
                    format_func=lambda x: x.capitalize(),
                    key='fruit_selector'
                ).lower()
                
            
            if final_fruit_name and final_fruit_name in NUTRITION_DATA:
                st.markdown(f"---")
                st.subheader(f"📊 Nutrisi untuk **{final_fruit_name.capitalize()}**")
                
                grams = st.number_input(
                    f"Berapa gram **{final_fruit_name.capitalize()}** yang akan dimakan?", 
                    min_value=1.0, 
                    max_value=500.0, 
                    value=100.0, 
                    step=10.0,
                    key='gram_input'
                )
                
                base_nutri = NUTRITION_DATA[final_fruit_name]
                scale = grams / 100.0
                
                calculated_nutri = {}
                display_rows = []
                
                for key, value in base_nutri.items():
                    calculated_value = value * scale 
                    display_value = calculated_value 
                    unit = " µg" 
                    
                    if key == "water":
                        if calculated_value >= 1_000_000:
                            display_value = calculated_value / 1_000_000
                            unit = " Liter"
                        elif calculated_value >= 1_000:
                            display_value = calculated_value / 1_000
                            unit = " mL"
                        else:
                            unit = " µL"
                            
                    elif key in ["fiber"]:
                        display_value = calculated_value / 1_000 
                        unit = " g"
                    
                    elif key == "calories":
                        unit = " kkal"
                        display_value = calculated_value 
                        
                    elif calculated_value >= 1000:
                        display_value = calculated_value / 1000
                        unit = " mg" 

                    
                    calculated_nutri[key] = value * scale 
                    
                    display_key = key.replace('vitaminb', 'Vitamin B').replace('vitamina', 'Vitamin A').replace('vitamine', 'Vitamin E').replace('vitamink', 'Vitamin K').title()
                    display_key = display_key.replace('Water', 'Air').replace('Fiber', 'Serat').replace('Calories', 'Kalori')
                    
                    formatted_value = f"{display_value:.2f}".rstrip('0').rstrip('.')
                    display_rows.append({
                        "Nutrisi": display_key,
                        "Jumlah": formatted_value,
                        "Satuan": unit
                    })
                
                st.dataframe(pd.DataFrame(display_rows), use_container_width=True)

                if st.button(f"✅ Konfirmasi & Tambahkan {final_fruit_name.capitalize()} ke Meal {selected_child_name}", type="primary", key='add_meal_button'):
                    
                    if CURRENT_KEY in st.session_state:
                         for key, value in calculated_nutri.items():
                             if key in st.session_state[CURRENT_KEY]:
                                st.session_state[CURRENT_KEY][key] += value
                                
                    meal_entry = {
                        "date": 'Today',
                        "food": final_fruit_name.capitalize(),
                        "grams": grams,
                        "nutrients": calculated_nutri 
                    }
                    
                    st.session_state['user_data'][current_email]['children'][selected_child_index]['meal_history'].append(meal_entry)
                    st.success(f"**{final_fruit_name.capitalize()}** ({grams:.0f}g) berhasil ditambahkan ke riwayat makan **{selected_child_name}**.")
                    
                    if 'manual_input' in st.session_state:
                         del st.session_state['manual_input']
                    
                    navigate_to('home')
                    st.rerun()