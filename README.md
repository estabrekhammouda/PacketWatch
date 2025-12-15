# PacketWatch – Network Intrusion Detection System (NIDS)

**Version:** 1.0.0  
**Author:** Estabrek Hamouda  

---

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

