# 🍏 NutriVision Pro

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-red)](https://link-aplikasi-kamu.streamlit.app/)

An interactive web application built with **Streamlit**, designed to help parents track their child's daily nutrition and classify fruit images using a Deep Learning model (MobileNetV2).

## ✨ Key Features

- 🔐 **User Authentication:** Secure login and registration system to protect user profile data.
- 👶 **Child Profile & BMI Calculator:** Keep track of the child's physical profile with automatic Body Mass Index (BMI) calculations to monitor growth and health status.
- 📊 **Daily Nutrition Tracker:** A monitoring dashboard to ensure the child's daily nutritional needs are consistently met.
- 📸 **Smart Fruit Scanner:** Real-time fruit image detection and classification using artificial intelligence, instantly displaying the nutritional information of the scanned fruit.

## 📂 Repository Structure

```text
NutriVision-Pro/
├── model/
│   ├── class_names.json        # Class labels for the classification model
│   └── fruit_classifier.h5     # Pre-trained Deep Learning model (MobileNetV2)
├── ux AOL AI/assets/           # UI/UX assets directory (Logos, Backgrounds, etc.)
├── auth.py                     # Login and registration logic
├── child_nutrition.py          # Nutrition tracking and dashboard module
├── child_profile.py            # Profile management and BMI calculation module
├── config.py                   # Main application configuration file
├── home.py                     # Main landing page
├── main.py                     # Main execution file (Streamlit entry point)
├── nutrition_data.py           # Static database or nutrition data handler
├── scan.py                     # Image scanning and inference module
├── requirements.txt            # List of required Python dependencies
├── .gitignore                  # Files and directories to be ignored by Git
└── README.md                   # Project documentation

🚀 Local Installation Guide
If you want to run this application locally on your machine, follow these steps:

1. Clone the Repository

git clone [https://github.com/your-username/NutriVision-Pro.git](https://github.com/your-username/NutriVision-Pro.git)
cd NutriVision-Pro

2. Create a Virtual Environment

python -m venv venv

# For Windows users:
venv\Scripts\activate

# For Mac/Linux users:
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Run the Application

streamlit run main.py

🛠️ Technologies Used
Frontend & Framework: Streamlit

Machine Learning: TensorFlow / Keras

Image Processing: Pillow / OpenCV

Data Manipulation: Pandas & NumPy

Programming Language: Python 3.x