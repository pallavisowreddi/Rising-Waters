# Rising Waters: ML-Powered Flood Forecasting Web App

An end-to-end Machine Learning web application designed to predict regional flood risks. Using meteorological features such as annual rainfall, cloud visibility, and seasonal rainfall patterns, the application processes real-time weather metrics using an optimized **XGBoost Classifier** to deliver early warnings, confidence scores, and safety recommendations. 

The user interface is built on **Bootstrap 5** using a professional **White, Blue, and Dark Navy** design aesthetic. It includes custom form validations, loading spinner animations, and comprehensive advisory checklists. The application is packaged to be fully compatible with both **Vercel** serverless functions and **IBM Cloud**.

---

## 📂 Project Directory Structure

```
RisingWaters-Vercel/
├── vercel.json                    # Vercel routing & runtime configurations
├── requirements.txt               # Dependencies required by Flask & ML models
├── Procfile                       # IBM Cloud process configuration (WSGI Gunicorn launcher)
├── runtime.txt                    # Python environment specification
├── README.md                      # Complete setup, testing, and deployment guide
├── test_vercel_app.py             # Route integration test suite (using Flask test client)
├── api/                           # Serverless functions entry point
│   ├── index.py                   # Main Flask backend application
│   ├── floods.save                # Saved XGBoost Classification Model
│   ├── transform.save             # Saved StandardScaler instance
│   ├── templates/                 # Bootstrap 5 HTML layouts
│   │   ├── home.html              # Landing page dashboard
│   │   ├── index.html             # Parameter submission form
│   │   ├── chance.html            # High Flood Risk warning outcome page
│   │   ├── no_chance.html         # Low Flood Risk normal conditions page
│   │   └── error.html             # Custom 404/500 handlers page
│   └── static/                    # Custom frontend assets
│       ├── css/
│       │   └── main.css           # Custom dark navy theme overrides & animations
│       └── js/
│           └── main.js            # Input validation & submission overlay handlers
├── ModelTraining/                 # Model evaluation pipelines
│   ├── train.py                   # Automation training scripts
│   ├── flood dataset.xlsx         # Weather metrics dataset
│   └── Floods.ipynb               # Jupyter notebook for exploratory data analysis
└── screenshots/                   # Placeholders for application visuals
```

---

## 📊 Machine Learning Model Comparison

The classifiers were evaluated using a **75% train / 25% test split** (random state 10). The dataset columns were scaled using a `StandardScaler` fitted on the training split. 

| Classification Model | Accuracy | F1-Score | Recall | Precision |
|----------------------|----------|----------|--------|-----------|
| **XGBoost Classifier** | **96.55%** | **96.55%** | **96.55%** | **96.55%** |
| **Random Forest** | 96.55% | 96.55% | 96.55% | 96.55% |
| **Decision Tree** | 96.55% | 96.55% | 96.55% | 96.55% |
| **K-Nearest Neighbors (KNN)** | 89.65% | 89.47% | 89.65% | 90.48% |

*Although Decision Tree and Random Forest tied in accuracy, **XGBoost** was selected for final deployment because of its superior gradient boosting optimization, step-by-step leaf-wise tree splitting stability on tabular data, and excellent generalization.*

---

## 🚀 Getting Started Locally

### 1. Prerequisites
Ensure you have **Python 3.8+** installed. Download and install python from [python.org](https://www.python.org/downloads/) if needed.

### 2. Installation
Open your terminal (or VS Code terminal) and run the following command to install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Running the Flask App Locally
To start the Flask development server on your machine, run:
```bash
python api/index.py
```
Open your browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 4. Running the Integration Tests
To execute the automated test suite verifying endpoints, redirects, validation constraints, and prediction probability outputs:
```bash
python test_vercel_app.py
```

---

## ☁️ Deployment Guide

### Option A: Deploying on Vercel (Recommended)
Vercel supports serverless Python scripts natively using the configuration defined in `vercel.json`.

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```
2. **Deploy directly from VS Code**:
   Open a terminal at the project root (`RisingWaters-Vercel/`) and execute:
   ```bash
   vercel
   ```
   Follow the prompts to link the project and deploy. Once the build completes, Vercel will generate a production link (e.g. `https://rising-waters-example.vercel.app`).

3. **Deploy from GitHub Dashboard**:
   - Create a new repository on GitHub.
   - Push your code to the repository (see GitHub upload instructions below).
   - Go to [Vercel Dashboard](https://vercel.com/dashboard) -> click **Add New** -> **Project**.
   - Import your GitHub repository, choose **Other** framework preset, and click **Deploy**. Vercel will build and launch your Flask serverless function automatically!

---

### Option B: Deploying to IBM Cloud (Foundational Setup)
We have included a `Procfile` and `runtime.txt` configured for IBM Cloud Foundry or Cloud Engine running Python runtimes.

1. **Install IBM Cloud CLI** and target Cloud Foundry / Code Engine.
2. Create a manifest or use `cf push` from the root directory. IBM Cloud reads the `Procfile` to execute `gunicorn` and binds the application port.

---

## 🐙 Uploading to GitHub

To upload this new folder directly to your GitHub repository:

1. **Create a new repository on GitHub**:
   - Go to [github.com/new](https://github.com/new)
   - Set the Repository Name to `Rising-Waters`
   - Leave "Initialize repository with README, .gitignore" **UNCHECKED** (since we have them locally)
   - Click **Create repository**

2. **Run Git Commands in your VS Code Terminal**:
   Open the folder `RisingWaters-Vercel` in VS Code, open a terminal, and run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Vercel-ready Rising Waters app"
   git branch -M main
   git remote add origin https://github.com/pallavisowreddi/Rising-Waters.git
   git push -u origin main -f
   ```

*Note: If the origin URL is already configured, you can skip the `git remote add origin` step or update it with `git remote set-url origin <URL>`.*
