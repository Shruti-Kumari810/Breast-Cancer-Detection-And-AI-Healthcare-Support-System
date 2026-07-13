# 🩺 AI-Powered Breast Cancer Detection & Healthcare Support System

> An intelligent healthcare platform that leverages Machine Learning to assist in the early detection of breast cancer while providing patient record management and healthcare support.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikitlearn)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?logo=mysql)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📌 Project Overview

Breast cancer is one of the most common cancers affecting women worldwide. Early diagnosis significantly increases the chances of successful treatment.

This project is an AI-powered Breast Cancer Detection & Healthcare Support System that predicts whether a breast tumor is **Benign** or **Malignant** using Machine Learning algorithms trained on the **Wisconsin Breast Cancer Dataset**.

The system also provides a modern healthcare interface for patient management, medical report analysis, and healthcare assistance.

---

# 🚀 Features

- ✅ Breast Cancer Prediction using Machine Learning
- ✅ Multiple ML Models (Logistic Regression, SVM, Random Forest)
- ✅ FastAPI REST Backend
- ✅ Streamlit Interactive Frontend
- ✅ Patient Registration & Record Management
- ✅ MySQL Database Integration
- ✅ PDF Medical Report Upload
- ✅ Real-Time Prediction
- ✅ Prediction Confidence Score
- ✅ Doctor Information & Healthcare Support
- ✅ User-Friendly Dashboard

---

# 🧠 Machine Learning Models

The project implements and compares multiple classification algorithms:

- Logistic Regression
- Support Vector Machine (SVM)
- Random Forest Classifier

Evaluation Metrics:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- ROC-AUC Score

---

# 🛠️ Tech Stack

## Frontend

- Streamlit
- HTML
- CSS

## Backend

- FastAPI
- Uvicorn
- REST APIs

## Machine Learning

- Scikit-learn
- Pandas
- NumPy
- Joblib

## Database

- MySQL

## Visualization

- Matplotlib
- Seaborn

---

# 📂 Project Structure

```
Breast-Cancer-Detection-System/
│
├── frontend/
│   ├── Home.py
│   ├── Prediction.py
│   ├── Dashboard.py
│
├── backend/
│   ├── main.py
│   ├── api.py
│   ├── database.py
│
├── ml_models/
│   ├── logistic_regression.pkl
│   ├── svm.pkl
│   ├── random_forest.pkl
│
├── dataset/
│
├── reports/
│
├── database/
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

---

# 📊 Dataset

Dataset Used:

**Wisconsin Breast Cancer Diagnostic Dataset**

Features include:

- Radius
- Texture
- Perimeter
- Area
- Smoothness
- Compactness
- Concavity
- Symmetry
- Fractal Dimension

Target Classes:

- Benign (B)
- Malignant (M)

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Shruti-Kumari810/breast-cancer-detection-system.git
```

---

## Navigate to Project

```bash
cd breast-cancer-detection-system
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run FastAPI Backend

```bash
uvicorn main:app --reload
```

Backend URL

```
http://127.0.0.1:8000
```

---

## Run Streamlit Frontend

```bash
streamlit run Home.py
```

---

# 📈 Workflow

Patient Input

↓

Data Preprocessing

↓

Machine Learning Model

↓

Prediction

↓

Risk Analysis

↓

Result Display

↓

Store Patient Data in MySQL

---

# 📷 Screenshots

## Home Page

(Add Screenshot Here)

---

## Prediction Page

(Add Screenshot Here)

---

## Dashboard

(Add Screenshot Here)

---

## Result Page

(Add Screenshot Here)

---

# 📊 Future Enhancements

- AI Chatbot for Patient Support
- Deep Learning Models
- X-Ray & Mammogram Image Analysis
- Doctor Appointment Booking
- Email & SMS Notifications
- Cloud Deployment
- Mobile Application
- Multi-language Support

---

# 🎯 Learning Outcomes

Through this project, I learned:

- Machine Learning Model Development
- Feature Engineering
- Model Evaluation
- REST API Development
- FastAPI
- Streamlit
- MySQL Database Integration
- Healthcare Application Development
- Full Stack AI Project Deployment

---

# 👩‍💻 Author

**Shruti Kumari**

B.Tech CSE (AI & ML)

Asansol Engineering College

GitHub: https://github.com/Shruti-Kumari810

LinkedIn: https://www.linkedin.com/in/shruti-kumari-2b784b325/

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!

---

# 📜 License

This project is licensed under the MIT License.
