# PacketWatch – Network Intrusion Detection System (NIDS)

## 📖 Project Overview

**PacketWatch** is a machine learning-powered **Network Intrusion Detection System (NIDS)** designed to detect malicious network activity in real-time. It leverages various features of network sessions to classify traffic as either **normal** or **attack**. The system includes a trained **Random Forest model**, data preprocessing pipelines, and a simple web-based deployment using **FastAPI**.

---

## 🎯 Features

- **Machine Learning Models:** Logistic Regression, Random Forest, SVM (RBF kernel) with cross-validation.
- **Data Processing:**
  - Missing value handling (median for numeric, mode for categorical)
  - Outlier detection using Isolation Forest
  - Feature engineering: total login activity, failed login ratio
  - Scaling, polynomial features, one-hot encoding, and feature binning
- **Exploratory Data Analysis (EDA):**
  - Feature distributions and correlations
  - Boxplots and countplots for categorical features
  - Session duration vs. attack detection
- **Deployment:**
  - FastAPI server with endpoints for health check and prediction
  - Input validation using Pydantic models
  - Serves static HTML/CSS/JS front-end
- **Output:** Predicts if a network session is malicious (1) or normal (0)

---

## 📂 Project Structure

PacketWatch/
│
├─ intrusion_model.pkl # Trained Random Forest model
├─ Projet_ML_version5.ipynb # Jupyter notebook with EDA and modeling
├─ app.py # FastAPI backend
├─ static/
│ ├─ index.html # Front-end page
│ ├─ style.css
│ └─ script.js
├─ README.md
└─ requirements.txt

## ⚙️ Installation

Clone the repository:
in bash
git clone https://github.com/yourusername/PacketWatch.git
cd PacketWatch

Install dependencies:

bash
pip install -r requirements.txt

Running the API
Start the FastAPI server:

bash
Copy code
python app.py

Open your browser and access:

Main UI: http://localhost:8000/

API Docs (Swagger): http://localhost:8000/docs

Health Check: http://localhost:8000/health

Prediction Endpoint
POST /predict

Request Example:

json
Copy code
{
  "session_id": "sess_12345",
  "network_packet_size": 512,
  "protocol_type": "TCP",
  "login_attempts": 3,
  "session_duration": 120.5,
  "encryption_used": "AES",
  "ip_reputation_score": 75.5,
  "failed_logins": 2,
  "browser_type": "Chrome",
  "unusual_time_access": 0
}
Response Example:

json
Copy code
{
  "session_id": "sess_12345",
  "attack_detected": 1
}
📊 Model Evaluation
Random Forest achieved the best performance during cross-validation.

Evaluation metrics include Accuracy, F1-score, and Confusion Matrix.

Data preprocessing ensures robustness to missing values, outliers, and categorical features.

🛠 Technologies Used
Python 3.11

Pandas, Numpy, Seaborn, Matplotlib

Scikit-learn (ML pipelines, preprocessing, Random Forest, SVM, Logistic Regression)

FastAPI (API deployment)

Joblib (model serialization)

HTML, CSS, JS (frontend)

📌 Notes
Ensure all required Python packages are installed from requirements.txt.

Model predictions are based on historical data; retraining with new data is recommended for improved accuracy.

FastAPI allows easy integration with web or mobile applications for real-time detection.
