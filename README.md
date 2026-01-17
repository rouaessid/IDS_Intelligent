# 🛡️ Intelligent Intrusion Detection System (IDS)

A hierarchical multi-level machine learning system for network intrusion detection with a professional Next.js real-time monitoring dashboard and FastAPI backend.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.0-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-2.1.3-red)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Performance](#performance)
- [Project Structure](#project-structure)

## 🎯 Overview

This project implements a **3-level hierarchical classification system** for network intrusion detection using the CIC-IDS2017 dataset. The system combines multiple machine learning models (Random Forest, XGBoost, and Linear SVM) to achieve high accuracy while preventing data leakage and overfitting.

### Key Highlights
- **99%+ accuracy** across major classification levels
- **Hierarchical Approach**: Binary -> Family -> Expert Specialization
- **Real-time Simulation**: Sampling from real network traffic
- **Modern UI**: Next.js dashboard with interactive charts and alerts
- **Pre-trained Models**: All weight and scalers are provided as `.joblib` files

> [!WARNING]
> The simulation data file `X_unscaled.joblib` (approx. 170MB) is excluded from this repository due to GitHub's file size limits. You should generate it using the provided notebooks before running the simulation locally.

## ✨ Features

### 🔍 Multi-Level Detection
1. **Level 1 (Binary)**: Distinguishes between benign and malicious traffic (Random Forest)
2. **Level 2 (Family)**: Classifies attacks into families (DoS, BruteForce, etc.)
3. **Level 3 (Expert)**: Specialized models for granular identification (e.g., **Linear SVM** for DoS)

### 📊 Interactive Dashboard (Next.js)
- **Live Monitoring**: Real-time simulation of network flow analysis via FastAPI sampling
- **Manual Analysis**: Deep inspection of specific flows via attack index investigation
- **Visual Analytics**: Traffic trends and threat distribution by family

### 🛠️ Technical Implementation
- **Data Preprocessing**: Handling inf/nan, reduction from 78 to 62 features
- **Identity Protection**: Removal of ports and window size features to prevent overfitting
- **Persistence**: Models and scalers saved in the `data/` directory



## 🚀 Installation

### Prerequisites
- Python 3.11+
- Node.js & npm
- Virtual environment (venv)

### Backend Setup (FastAPI)
1. **Activate venv**
```bash
venv\Scripts\activate
```
2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Run API**
```bash
python api/main.py
```

### Frontend Setup (Next.js)
1. **Install dependencies**
```bash
npm install
```
2. **Run Dev Server**
```bash
npm run dev
```

## 💻 Usage

1. Open **http://localhost:3000** for the dashboard.
2. Ensure the backend is running on **http://localhost:5000**.
3. Use the **"Start Simulation"** button to see real-time detection in action.
4. Go to **"Analysis"** to investigate specific dataset indices.

## 📈 Performance (Test Set)

| Level | Accuracy |
|-------|----------|
| **Level 1 (Binary)** | 99.2% |
| **Level 2 (Family)** | 100% |
| **Level 3 Experts**  | 97% - 99% |

## 📁 Project Structure & Models

The project includes pre-trained models stored as `.joblib` files in the `data/trained_models/` directory.

```
IDS_Intelligent/
├── data/
│   ├── processed/          # Processed datasets (X_unscaled.joblib)
│   └── trained_models/     # Model weights and scalers (.joblib)
│       └── level3/         # Expert models
├── api/                    # FastAPI Backend
├── app/                    # Next.js App Router (Frontend)
├── src/                    # Shared logic (detector.py)
├── notebooks/              # Data Science Pipeline
└── README.md
```

> [!NOTE]
> The `.joblib` files are essential for the `IDSDetector` to function without re-training.
