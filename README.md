# 🛡️ Intelligent Intrusion Detection System (IDS)

A hierarchical multi-level machine learning system for network intrusion detection with a professional real-time monitoring dashboard.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.0-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-2.1.3-red)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52-green)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Performance](#performance)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🎯 Overview

This project implements a **3-level hierarchical classification system** for network intrusion detection using the CIC-IDS2017 dataset. The system combines multiple machine learning models to achieve high accuracy while preventing data leakage and overfitting.

### Key Highlights
- **99%+ accuracy** across all classification levels
- **Real-time detection** with <15ms average latency
- **Professional dashboard** with dark cybersecurity theme
- **Behavioral learning** (no reliance on IP/Port identity features)
- **Production-ready** architecture with proper data handling

## ✨ Features

### 🔍 Multi-Level Detection
1. **Level 1 (Binary)**: Distinguishes between benign and malicious traffic
2. **Level 2 (Family)**: Classifies attacks into 7 families (DoS, DDoS, BruteForce, etc.)
3. **Level 3 (Expert)**: Specialized models for granular attack identification

### 📊 Interactive Dashboard
- **Live Monitoring**: Real-time simulation of network flow analysis
- **Manual Analysis**: Deep inspection of specific flows with attack index suggestions
- **System Info**: Architecture documentation and performance metrics
- **Dark Theme**: Professional cybersecurity-themed interface

### 🛠️ Technical Features
- Split-then-scale methodology to prevent data leakage
- Independent scalers for each classification level
- Feature importance diagnostics
- Automated identity feature removal at Level 3

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Network Traffic                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │   Level 1      │  Random Forest
            │   Binary       │  (Benign vs Attack)
            └────────┬───────┘
                     │
                ┌────┴────┐
                │ Attack? │
                └────┬────┘
                     │ Yes
                     ▼
            ┌────────────────┐
            │   Level 2      │  Random Forest
            │   Family       │  (DoS, BruteForce, etc.)
            └────────┬───────┘
                     │
            ┌────────┴────────┐
            │                 │
            ▼                 ▼
    ┌──────────────┐  ┌──────────────┐
    │  DoS Expert  │  │ BruteForce   │  Random Forest
    │  (Logistic)  │  │ Expert (RF)  │  / Logistic Regression
    └──────────────┘  └──────────────┘
```

## 🚀 Installation

### Prerequisites
- Python 3.11+
- Git
- 8GB+ RAM recommended

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/rouaessid/IDS_Intelligent.git
cd IDS_Intelligent
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download the dataset**
- Download CIC-IDS2017 from [Canadian Institute for Cybersecurity](https://www.unb.ca/cic/datasets/ids-2017.html)
- Place CSV files in `data/raw/`

5. **Run preprocessing notebooks**
```bash
jupyter notebook notebooks/02_preprocessing.ipynb
```

## 💻 Usage

### Launch the Dashboard
```bash
streamlit run src/app.py --server.port 8505
```

Then open your browser to: **http://localhost:8505**

### Dashboard Modes

#### 1. Live Monitoring
- Click **"Start Simulation"** to analyze 50 random flows
- View real-time alerts and threat classifications
- Monitor system metrics (flows analyzed, threats detected)

#### 2. Manual Analysis
- Enter a flow index (e.g., 540822 for FTP-Patator attack)
- Click **"Analyze Flow"** to see detailed classification
- Use **"Random Attack"** button for quick testing

#### 3. System Info
- View architecture documentation
- Check model performance metrics
- Review technology stack

### Training Models

Run notebooks in order:
```bash
1. notebooks/01_exploration.ipynb
2. notebooks/02_preprocessing.ipynb
3. notebooks/03_model_Level_01.ipynb
4. notebooks/04_model_Level_02.ipynb
5. notebooks/05_model_Level_03_CustomSpecialization.ipynb
```

## 📊 Dataset

**CIC-IDS2017** - A comprehensive network traffic dataset containing:
- **2.8M+ flows** (540K benign, 557K attacks)
- **7 attack families**: DoS, DDoS, BruteForce, WebAttack, PortScan, Bot, RareAttack
- **14 specific attack types**: FTP-Patator, SSH-Patator, DoS Hulk, etc.
- **80+ features**: Flow duration, packet statistics, IAT metrics, etc.

## 📈 Performance

| Level | Model | Accuracy | Precision | Recall | F1-Score |
|-------|-------|----------|-----------|--------|----------|
| **Level 1** | Random Forest | 99.0% | 99.1% | 98.9% | 99.0% |
| **Level 2** | XGBoost | 99.1% | 99.2% | 99.0% | 99.1% |
| **Level 3 (DoS)** | Logistic Regression | 99.3% | 99.4% | 99.2% | 99.3% |
| **Level 3 (BruteForce)** | Random Forest | 98.7% | 98.8% | 98.6% | 98.7% |

### Key Metrics
- **Detection Rate**: 99.3% for attacks
- **False Positive Rate**: <1%
- **Average Latency**: 12ms per flow
- **Throughput**: ~83 flows/second

## 📁 Project Structure

```
IDS_Intelligent/
├── data/
│   ├── raw/                    # Original CIC-IDS2017 CSV files
│   ├── cleaned/                # Preprocessed dataset
│   ├── processed/              # Unscaled features + labels
│   └── trained_models/         # Saved models & scalers
│       ├── level3/             # Expert models
│       ├── model_lvl1_binary.joblib
│       ├── model_lvl2_multiclass.joblib
│       └── scaler_*.joblib
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_model_Level_01.ipynb
│   ├── 04_model_Level_02.ipynb
│   └── 05_model_Level_03_CustomSpecialization.ipynb
├── src/
│   ├── app.py                  # Streamlit dashboard
│   └── detector.py             # Multi-level detection engine
├── requirements.txt
└── README.md
```

## 🔧 Technical Details

### Data Leakage Prevention
- **Split-first, then scale**: Data is split into train/test BEFORE scaling
- **Independent scalers**: Each level has its own StandardScaler
- **No global scaling**: Prevents test data from influencing training

### Overfitting Prevention
- **Identity feature removal**: Dropped `Destination Port`, `Init_Win_bytes_forward/backward`
- **Behavioral learning**: Models learn from flow patterns (IAT, packet length, duration)
- **Feature importance tracking**: Diagnostic plots to verify proper learning

### Label Encoding
- **Two-step decoding**: Primary encoder (string→ID) + Secondary encoder (ID→0-N)
- **Proper family mapping**: Ensures correct attack family names in dashboard



⭐ If you find this project useful, please consider giving it a star!
