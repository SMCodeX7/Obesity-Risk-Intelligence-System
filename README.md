# Obesity Risk Intelligence System

An end-to-end machine learning application that predicts obesity-risk categories using demographic, physical, nutritional, and lifestyle information.

The system combines a trained Scikit-learn machine learning pipeline with a Flask REST API, Streamlit user interface, SQLite prediction history, and downloadable PDF assessment reports.

> This project is developed for educational and research purposes. Predictions are not medical diagnoses and should not replace professional healthcare advice.

## Overview

The Obesity Risk Intelligence System classifies an assessment into one of seven categories:

- Insufficient Weight
- Normal Weight
- Overweight Level I
- Overweight Level II
- Obesity Type I
- Obesity Type II
- Obesity Type III

The final model uses 16 input features and a tuned Gradient Boosting Classifier.

## Key Features

- Guided 3-step obesity-risk assessment
- Seven-class machine learning prediction
- Prediction confidence and probability distribution
- Severity-based result visualization
- Flask REST API
- Streamlit frontend
- SQLite prediction history
- Saved assessment review
- Downloadable PDF reports
- Sri Lanka time display using UTC+05:30
- Safe prediction-history clearing
- Automated test suite
- Model explainability and evaluation analysis

## Model Performance

The selected model is a tuned **Gradient Boosting Classifier**.

| Metric | Score |
|---|---:|
| Accuracy | 90.75% |
| Balanced Accuracy | 89.76% |
| Macro F1 | 89.73% |
| Weighted F1 | 90.72% |

The final model was evaluated on an independent test set.

## System Architecture

```text
User
  |
  v
Streamlit Frontend
  |
  v
Frontend API Client
  |
  v
Flask REST API
  |
  +--> Input Validation
  |
  v
Scikit-learn Pipeline
  |
  +--> Preprocessing
  +--> Gradient Boosting Model
  |
  v
Prediction Result
  |
  +--> SQLite Prediction History
  |
  +--> PDF Report
```

## Technology Stack

**Machine Learning**
- Python
- Scikit-learn
- Pandas
- NumPy
- SHAP
- Joblib

**Backend**
- Flask
- Waitress
- SQLite
- ReportLab

**Frontend**
- Streamlit

**Testing**
- Pytest

## Project Structure

```text
Obesity-Risk-Intelligence-System/
│
├── backend/        Flask API, database and report services
├── frontend/       Streamlit application
├── models/         Trained model and model metadata
├── src/            ML preprocessing and supporting logic
├── database/       SQLite schema and local database
├── data/           Dataset directories
├── notebooks/      ML development and analysis notebooks
├── reports/        Evaluation outputs and analysis
├── tests/          Automated tests
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/SMCodeX7/Obesity-Risk-Intelligence-System.git
cd Obesity-Risk-Intelligence-System
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the backend:

```bash
python -m backend.run_production
```

The API runs locally at:

```text
http://127.0.0.1:5000
```

Open another terminal, activate the virtual environment, and start Streamlit:

```bash
python -m streamlit run frontend/app.py
```

Open the Streamlit URL shown in the terminal.

## Prediction History Clearing

Prediction-history deletion is protected by an environment variable.

To enable it locally in PowerShell:

```powershell
$env:OBESITY_ENABLE_HISTORY_RESET="true"
```

When disabled, the backend rejects history-clear requests.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/model-info` | Retrieve model information |
| POST | `/predict` | Generate and save a prediction |
| GET | `/predictions` | Retrieve prediction history |
| GET | `/predictions/<id>` | Retrieve a saved assessment |
| GET | `/predictions/<id>/report` | Download a PDF report |
| DELETE | `/predictions` | Clear prediction history when enabled |

## Running Tests

Run the complete automated test suite with:

```bash
python -m pytest -q
```

## Dataset

The project uses the obesity-risk dataset associated with the Kaggle Playground Series Season 4 Episode 2.

The raw dataset is not included in Git tracking.

The model uses 16 predictive features covering:

- Demographic information
- Height and weight
- Eating habits
- Water consumption
- Physical activity
- Technology use
- Transportation
- Lifestyle characteristics

## Model Development

The machine learning workflow includes:

- Data exploration
- Preprocessing pipelines
- Stratified dataset splitting
- Baseline model comparison
- Hyperparameter tuning
- Independent test evaluation
- SHAP explainability
- BMI ablation analysis
- Ordinal error analysis
- Subgroup evaluation

The final trained pipeline is stored in:

```text
models/obesity_risk_pipeline.joblib
```

## Disclaimer

This system is intended only for educational and research use.

Its predictions represent machine learning estimates based on the supplied input data and should not be interpreted as medical diagnoses, treatment recommendations, or professional healthcare advice.

## License

This project is licensed under the MIT License.