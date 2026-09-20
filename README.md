# NutriVision Pro

An interactive web application for tracking children's daily nutrition and identifying fruits through AI-powered image classification.

**Live Demo:** [https://your-app-name.streamlit.app/](https://your-app-name.streamlit.app/)

## Features

- **Secure Authentication**: Login and registration system with profile data protection
- **Child Profile Management**: Track physical profile with automatic BMI calculation
- **Nutrition Tracking**: Monitor daily nutritional intake against recommended guidelines
- **Smart Fruit Scanner**: Real-time fruit identification and instant nutritional lookup using deep learning (MobileNetV2)

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend & Framework | Streamlit |
| Machine Learning | TensorFlow / Keras |
| Image Processing | Pillow / OpenCV |
| Data Processing | Pandas, NumPy |
| Language | Python 3.x |

## Project Structure

```
NutriVision-Pro/
├── model/
│   ├── class_names.json          # Classification model labels
│   └── fruit_classifier.h5       # Pre-trained MobileNetV2 model
├── assets/                        # UI/UX assets (logos, backgrounds)
├── auth.py                        # Authentication logic
├── child_profile.py               # Profile and BMI management
├── child_nutrition.py             # Nutrition tracking dashboard
├── scan.py                        # Image inference module
├── nutrition_data.py              # Nutrition data handler
├── config.py                      # Application configuration
├── home.py                        # Landing page
├── main.py                        # Entry point
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # Documentation
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/NutriVision-Pro.git
   cd NutriVision-Pro
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

The application will be available at `http://localhost:8501`

## Usage

1. Create an account or log in
2. Set up your child's profile (age, weight, height)
3. Track daily nutrition intake using the dashboard
4. Use the fruit scanner to identify fruits and view their nutritional content

## Dependencies

- streamlit
- tensorflow
- keras
- pillow
- opencv-python
- pandas
- numpy

See `requirements.txt` for complete version specifications.

## Author

Joel Chriscendo Rahardjo Liem
