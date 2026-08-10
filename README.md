# Obesity Risk Intelligence System

A full-stack machine learning application that predicts an individual's obesity-risk category using demographic, physical, dietary, lifestyle, and activity-related information.

The project follows a complete machine learning workflow covering:

- Data understanding
- Exploratory data analysis
- Feature preprocessing
- Baseline model development
- Hyperparameter tuning
- Final model evaluation
- Model explainability
- Advanced error analysis
- Flask REST API development
- Streamlit frontend development
- Automated testing
- Future database integration and deployment

The final machine learning model is exposed through a Flask REST API and consumed by a Streamlit frontend.

---

# Current Project Status

## Phases 1–9 Complete

The project currently includes:

```text
Machine Learning Pipeline        ✅
Final Trained Model              ✅
Model Explainability             ✅
Flask REST API                   ✅
Input Validation                 ✅
Prediction Endpoint              ✅
Streamlit Frontend               ✅
Prediction Visualization         ✅
Automated Tests                  ✅
SQLite Integration               ⏳ Next
Deployment                       ⬜ Planned
```

The next phase is:

# Phase 10 — SQLite and Full Integration

---

# Project Progress

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Data Understanding | ✅ Complete |
| Phase 2 | Exploratory Data Analysis | ✅ Complete |
| Phase 3 | Preprocessing Pipeline | ✅ Complete |
| Phase 4 | Baseline Model Development | ✅ Complete |
| Phase 5 | Hyperparameter Tuning | ✅ Complete |
| Phase 6 | Final Model Selection and Evaluation | ✅ Complete |
| Phase 7 | Explainability and Advanced Evaluation | ✅ Complete |
| Phase 8 | Flask REST API | ✅ Complete |
| Phase 9 | Streamlit Frontend | ✅ Complete |
| Phase 10 | SQLite and Full Integration | ⏳ Next |
| Phase 11 | Deployment and Final Documentation | ⬜ Planned |

---

# Project Objectives

The main objectives of the Obesity Risk Intelligence System are to:

- Analyse obesity-related lifestyle and demographic information.
- Build a reliable multiclass machine learning classifier.
- Develop reusable preprocessing logic.
- Prevent data leakage during model development.
- Compare multiple classification algorithms.
- Tune the strongest candidate models.
- Evaluate the final model using a reserved test set.
- Analyse class-level performance.
- Explain global model behaviour.
- Explain individual predictions.
- Analyse ordinal classification errors.
- Compare models with and without an explicit BMI feature.
- Perform descriptive subgroup performance analysis.
- Persist the final preprocessing and prediction pipeline.
- Expose the model through a REST API.
- Validate prediction requests before inference.
- Develop a user-facing assessment interface.
- Display predicted class, confidence, and probabilities.
- Add persistent prediction history using SQLite.
- Prepare the complete application for deployment.

---

# Dataset

The project uses the generated obesity dataset associated with:

```text
Kaggle Playground Series
Season 4 Episode 2
```

The local dataset is stored at:

```text
data/raw/obesity.csv
```

The raw dataset is excluded from Git version control.

---

# Dataset Dimensions

```text
Rows:    20,758
Columns: 18
```

The dataset contains:

```text
16 predictive features
1 identifier column
1 target column
```

The identifier column:

```text
id
```

is excluded from machine learning training.

---

# Target Variable

The target variable is:

```text
NObeyesdad
```

The model predicts one of seven obesity-related classes:

```text
Insufficient_Weight
Normal_Weight
Overweight_Level_I
Overweight_Level_II
Obesity_Type_I
Obesity_Type_II
Obesity_Type_III
```

This is therefore a:

```text
7-class multiclass classification problem
```

---

# Predictive Features

The final model uses 16 original input features.

## Numerical Features

```text
Age
Height
Weight
FCVC
NCP
CH2O
FAF
TUE
```

| Feature | Description |
|---|---|
| Age | Age of the individual |
| Height | Height in metres |
| Weight | Weight in kilograms |
| FCVC | Frequency of vegetable consumption |
| NCP | Number of main meals |
| CH2O | Daily water consumption |
| FAF | Physical activity frequency |
| TUE | Time spent using technological devices |

---

# Ordinal Features

```text
CAEC
CALC
```

## CAEC

Food consumption between meals:

```text
no
Sometimes
Frequently
Always
```

## CALC

Alcohol consumption:

```text
no
Sometimes
Frequently
```

These categories have meaningful ordering and are processed with ordinal encoding.

---

# Nominal Features

```text
Gender
family_history_with_overweight
FAVC
SMOKE
SCC
MTRANS
```

These variables do not have meaningful numerical ordering and are processed using one-hot encoding.

---

# Project Structure

```text
Obesity-Risk-Intelligence-System/
│
├── backend/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── error_handlers.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── model_info.py
│   │   └── prediction.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── input_validator.py
│       └── model_service.py
│
├── data/
│   └── raw/
│       ├── .gitkeep
│       └── obesity.csv
│
├── database/
│   └── .gitkeep
│
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── assessment_form.py
│   │   └── prediction_result.py
│   │
│   └── services/
│       ├── __init__.py
│       └── api_client.py
│
├── models/
│   ├── obesity_risk_pipeline.joblib
│   └── model_metadata.json
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_preprocessing.ipynb
│   ├── 04_baseline_models.ipynb
│   ├── 05_model_tuning.ipynb
│   └── 06_explainability.ipynb
│
├── reports/
│   ├── figures/
│   └── generated/
│
├── src/
│   └── preprocessing.py
│
├── tests/
│   ├── test_preprocessing.py
│   ├── test_health_api.py
│   ├── test_model_service.py
│   ├── test_model_info_api.py
│   ├── test_prediction_api.py
│   ├── test_api_errors.py
│   ├── test_frontend_api_client.py
│   └── test_prediction_result.py
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

# Phase 1 — Data Understanding

Phase 1 focused on understanding the dataset before building machine learning models.

The analysis included:

- Dataset dimensions
- Column names
- Data types
- Target classes
- Missing values
- Duplicate records
- Numerical variables
- Categorical variables
- Class distribution

Notebook:

```text
notebooks/01_data_understanding.ipynb
```

The dataset contains:

```text
20,758 records
18 columns
```

No major missing-value or duplicate-record problems were identified.

---

# Phase 2 — Exploratory Data Analysis

Exploratory Data Analysis was performed to understand relationships between obesity categories and available features.

The analysis included:

- Target distribution
- Numerical distributions
- Categorical distributions
- Age analysis
- Height analysis
- Weight analysis
- Vegetable consumption
- Meal patterns
- Water consumption
- Physical activity
- Technology usage
- Transportation
- Correlation analysis
- Class-level comparisons

Notebook:

```text
notebooks/02_eda.ipynb
```

---

# Phase 3 — Preprocessing Pipeline

Reusable preprocessing logic is implemented in:

```text
src/preprocessing.py
```

The preprocessing system uses:

```text
ColumnTransformer
```

to process numerical, ordinal, and nominal features independently.

---

## Numerical Pipeline

Numerical variables use:

```text
SimpleImputer(strategy="median")
StandardScaler()
```

This provides:

```text
Missing-value handling
        +
Feature scaling
```

---

## Ordinal Pipeline

Ordinal variables use:

```text
SimpleImputer(strategy="most_frequent")
OrdinalEncoder()
```

Unknown categories are represented using:

```text
unknown_value = -1
```

---

## Nominal Pipeline

Nominal features use:

```text
SimpleImputer(strategy="most_frequent")
OneHotEncoder(handle_unknown="ignore")
```

---

# Feature Transformation

The application accepts:

```text
16 original input features
```

After preprocessing:

```text
25 transformed features
```

are passed to the classifier.

---

# Phase 4 — Baseline Model Development

Several machine learning algorithms were evaluated.

Models included:

```text
Dummy Classifier
Logistic Regression
Decision Tree
Random Forest
Gradient Boosting
```

## Validation Results

| Model | Accuracy | Macro F1 |
|---|---:|---:|
| Gradient Boosting | 0.9033 | 0.8930 |
| Random Forest | 0.8956 | 0.8849 |
| Logistic Regression | 0.8581 | 0.8418 |
| Decision Tree | 0.8452 | 0.8308 |
| Dummy Classifier | 0.1949 | 0.0466 |

Gradient Boosting achieved the strongest baseline validation performance.

Notebook:

```text
notebooks/04_baseline_models.ipynb
```

---

# Generalization Analysis

Training and validation Macro F1 scores were compared.

```text
Logistic Regression
Train Macro F1      ≈ 0.8443
Validation Macro F1 ≈ 0.8418
Gap                ≈ 0.0025
```

```text
Gradient Boosting
Train Macro F1      ≈ 0.9126
Validation Macro F1 ≈ 0.8930
Gap                ≈ 0.0196
```

```text
Random Forest
Train Macro F1      ≈ 1.0000
Validation Macro F1 ≈ 0.8849
Gap                ≈ 0.1151
```

```text
Decision Tree
Train Macro F1      ≈ 1.0000
Validation Macro F1 ≈ 0.8308
Gap                ≈ 0.1692
```

Random Forest and Decision Tree demonstrated substantially larger train-validation gaps.

Gradient Boosting and Random Forest were selected for tuning.

---

# Phase 5 — Hyperparameter Tuning

The following candidate models were tuned:

```text
Gradient Boosting
Random Forest
```

Hyperparameter optimization used:

```text
RandomizedSearchCV
```

with:

```text
5-fold StratifiedKFold cross-validation
```

The primary selection metric was:

```text
Macro F1
```

---

# Model Tuning Results

| Candidate | Validation Macro F1 |
|---|---:|
| Tuned Gradient Boosting | **0.8978** |
| Tuned Random Forest | **0.8967** |
| Baseline Gradient Boosting | 0.8930 |
| Baseline Random Forest | 0.8849 |

The selected model was:

```text
Tuned Gradient Boosting
```

---

# Selected Gradient Boosting Configuration

```text
n_estimators       = 100
learning_rate      = 0.15
max_depth          = 3
min_samples_split  = 5
min_samples_leaf   = 2
subsample          = 0.8
max_features       = 0.8
random_state       = 42
```

---

# Phase 6 — Final Model Evaluation

The selected Gradient Boosting configuration was refitted using development data and evaluated on the reserved test set.

The final persisted object contains:

```text
Preprocessing Pipeline
        +
Gradient Boosting Classifier
```

Therefore, raw application features can be passed directly to the saved pipeline.

---

# Final Test Results

| Metric | Score |
|---|---:|
| Accuracy | **0.9075** |
| Balanced Accuracy | **0.8976** |
| Macro F1 | **0.8973** |
| Weighted F1 | **0.9072** |

The model correctly classified approximately:

```text
90.75%
```

of the final test examples.

---

# Class-Level F1 Scores

| Class | F1 Score |
|---|---:|
| Insufficient Weight | 0.9271 |
| Normal Weight | 0.8677 |
| Overweight Level I | 0.7871 |
| Overweight Level II | 0.8220 |
| Obesity Type I | 0.9020 |
| Obesity Type II | 0.9796 |
| Obesity Type III | 0.9959 |

The most difficult classes were:

```text
Overweight Level I
Overweight Level II
```

---

# Saved Machine Learning Pipeline

The trained model is stored at:

```text
models/obesity_risk_pipeline.joblib
```

Model metadata is stored at:

```text
models/model_metadata.json
```

The metadata contains:

- Project name
- Selected model
- Model family
- Model configuration
- Random state
- Predictive feature count
- Transformed feature count
- Target class count
- Feature names
- Target classes
- Development record count
- Test record count
- Validation Macro F1
- Final evaluation metrics
- Scikit-learn version

The persisted model was produced using:

```text
scikit-learn 1.8.0
```

---

# Phase 7 — Explainability and Advanced Evaluation

Phase 7 investigated how the final frozen model behaves.

Notebook:

```text
notebooks/06_explainability.ipynb
```

Analysis included:

```text
Global feature importance
Global SHAP analysis
Local SHAP explanations
Ordinal error analysis
BMI ablation
Gender subgroup analysis
```

---

# Global Tree Feature Importance

The five strongest raw features according to the Gradient Boosting model were:

```text
1. Weight
2. Gender
3. FCVC
4. Height
5. Age
```

---

# Global SHAP Importance

The leading features according to SHAP were:

```text
1. Weight
2. FCVC
3. Height
4. Gender
5. Age
```

Both techniques identified a similar group of influential variables.

---

# Local SHAP Explanations

Local SHAP analysis was performed on:

```text
3 correctly classified examples
3 incorrectly classified examples
```

For each example, the strongest signed feature contributions toward the predicted class were analysed.

Outputs are stored under:

```text
reports/figures/
```

and:

```text
reports/generated/local_shap_explanations.csv
```

---

# Ordinal Error Analysis

The target classes follow an approximate obesity-status ordering:

```text
Insufficient Weight
        ↓
Normal Weight
        ↓
Overweight Level I
        ↓
Overweight Level II
        ↓
Obesity Type I
        ↓
Obesity Type II
        ↓
Obesity Type III
```

## Results

```text
Mean Ordinal Distance:
0.1092
```

```text
Exact Prediction Rate:
90.75%
```

```text
Adjacent-Class Error Rate:
7.90%
```

```text
Severe Error Rate:
1.35%
```

A severe error is defined as:

```text
Ordinal distance >= 2
```

Most errors therefore occur between neighbouring classes.

---

# BMI Ablation Experiment

BMI was calculated using:

```text
BMI = Weight / Height²
```

Two validation configurations were compared.

| Configuration | Validation Macro F1 |
|---|---:|
| Original 16 Features | **0.8978** |
| Original 16 Features + BMI | **0.8946** |

Difference:

```text
BMI Macro F1 Delta:
-0.00316
```

Adding explicit BMI did not improve model performance.

Therefore, the original 16-feature model was retained.

---

# Gender Subgroup Evaluation

Descriptive model performance was evaluated across gender subgroups.

Observed Macro F1 gap:

```text
0.0186
```

However, class-support distributions differ substantially between gender groups.

Therefore, subgroup results are treated as:

```text
Descriptive diagnostics
```

rather than proof that the model is fair or unfair.

---

# Phase 7 Summary

Important results are stored in:

```text
reports/generated/phase7_summary.json
```

Summary:

```text
Selected Model:
Tuned Gradient Boosting

Final Test Macro F1:
0.8973

Top Tree Features:
Weight
Gender
FCVC
Height
Age

Top SHAP Features:
Weight
FCVC
Height
Gender
Age

Mean Ordinal Distance:
0.1092

Exact Prediction Rate:
90.75%

Adjacent Error Rate:
7.90%

Severe Error Rate:
1.35%

BMI Macro F1 Delta:
-0.00316

Gender Macro F1 Gap:
0.0186
```

---

# Phase 8 — Flask REST API

Phase 8 exposed the trained machine learning pipeline through a Flask REST API.

The backend uses an application-factory architecture.

Backend responsibilities are separated into:

```text
Routes
Services
Validation
Model loading
Error handling
```

---

# Flask Backend Architecture

```text
Client
   │
   ▼
Flask REST API
   │
   ├── GET /health
   ├── GET /model-info
   └── POST /predict
            │
            ▼
       Input Validation
            │
            ▼
        ModelService
            │
            ▼
Saved Scikit-learn Pipeline
            │
            ▼
      Gradient Boosting
            │
            ▼
        Prediction
```

---

# Application Factory

The Flask backend uses:

```python
create_app()
```

The application factory:

```text
Creates Flask Application
        ↓
Applies Configuration
        ↓
Loads ModelService
        ↓
Loads ML Pipeline
        ↓
Registers Blueprints
        ↓
Registers Error Handlers
        ↓
Returns Application
```

---

# Model Service

Model operations are implemented in:

```text
backend/services/model_service.py
```

Responsibilities include:

```text
Load model metadata
Check Scikit-learn version
Load saved pipeline
Return model information
Create model input DataFrame
Run predict()
Run predict_proba()
Return class probabilities
```

The model is loaded when the Flask application starts instead of being reloaded for every request.

---

# Input Validation

Prediction input validation is implemented in:

```text
backend/services/input_validator.py
```

Incoming requests must:

```text
Be JSON objects
Contain all 16 features
Contain no unexpected features
Use valid numerical values
Use finite numbers
Stay within configured input ranges
Use valid categorical values
```

---

# API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Verify backend availability |
| GET | `/model-info` | Retrieve model metadata |
| POST | `/predict` | Generate obesity-risk prediction |

---

# GET /health

Example response:

```json
{
    "service": "obesity-risk-api",
    "status": "ok"
}
```

---

# GET /model-info

Returns information including:

```text
Project
Selected model
Model family
Configuration
Feature counts
Feature names
Target classes
Scikit-learn version
Final test metrics
Model loading status
```

Example structure:

```json
{
    "project": "Obesity Risk Intelligence System",
    "selected_model": "Tuned Gradient Boosting",
    "model_family": "Gradient Boosting",
    "configuration": "Tuned",
    "predictive_feature_count": 16,
    "transformed_feature_count": 25,
    "target_class_count": 7,
    "scikit_learn_version": "1.8.0",
    "model_loaded": true
}
```

---

# POST /predict

The endpoint accepts the 16 predictive features.

Example:

```json
{
    "Age": 25,
    "Height": 1.70,
    "Weight": 70,
    "FCVC": 2,
    "NCP": 3,
    "CH2O": 2,
    "FAF": 1,
    "TUE": 1,
    "CAEC": "Sometimes",
    "CALC": "no",
    "Gender": "Male",
    "family_history_with_overweight": "yes",
    "FAVC": "yes",
    "SMOKE": "no",
    "SCC": "no",
    "MTRANS": "Public_Transportation"
}
```

---

# Prediction Response

The endpoint returns:

```json
{
    "predicted_class": "Normal_Weight",
    "confidence": 0.87,
    "probabilities": {
        "Insufficient_Weight": 0.02,
        "Normal_Weight": 0.87,
        "Overweight_Level_I": 0.08,
        "Overweight_Level_II": 0.02,
        "Obesity_Type_I": 0.01,
        "Obesity_Type_II": 0.00,
        "Obesity_Type_III": 0.00
    }
}
```

The values above are illustrative examples.

Actual values are calculated dynamically by the trained model.

---

# API Error Handling

The backend uses structured JSON error responses.

## Validation Error

```json
{
    "error": "validation_error",
    "message": "Age must be numeric."
}
```

Status:

```text
400
```

## Unknown Endpoint

```json
{
    "error": "not_found",
    "message": "The requested endpoint does not exist."
}
```

Status:

```text
404
```

## Unsupported HTTP Method

```json
{
    "error": "method_not_allowed",
    "message": "The HTTP method is not allowed for this endpoint."
}
```

Status:

```text
405
```

## Internal Server Error

```json
{
    "error": "internal_server_error",
    "message": "An unexpected server error occurred."
}
```

Status:

```text
500
```

---

# Phase 9 — Streamlit Frontend

Phase 9 provides the user-facing interface for the Obesity Risk Intelligence System.

The frontend is built using:

```text
Streamlit
```

The Streamlit application does not directly load the machine learning model.

Instead:

```text
Streamlit
    ↓
APIClient
    ↓
Flask REST API
    ↓
Machine Learning Pipeline
```

This keeps frontend and backend responsibilities separated.

---

# Frontend Architecture

```text
Browser
   │
   ▼
Streamlit Application
   │
   ├── Sidebar
   │     ├── API status
   │     ├── Model name
   │     ├── Accuracy
   │     └── Macro F1
   │
   ├── Assessment Form
   │     ├── Personal information
   │     ├── Physical information
   │     ├── Eating habits
   │     ├── Activity
   │     └── Lifestyle
   │
   └── Prediction Result
         ├── Predicted category
         ├── Confidence
         ├── Probability chart
         ├── Probability ranking
         └── Technical details
                │
                ▼
             APIClient
                │
          HTTP / JSON
                │
                ▼
          Flask REST API
```

---

# Frontend Components

The Streamlit interface is divided into reusable components.

## Assessment Form

Implemented in:

```text
frontend/components/assessment_form.py
```

It collects all 16 predictive features.

The form groups inputs into:

```text
Personal and Physical Information
Eating Habits
Lifestyle and Activity
```

This avoids presenting users with one long unstructured input form.

---

# Personal and Physical Inputs

```text
Age
Height
Weight
Gender
Family history of overweight
```

---

# Eating Habit Inputs

```text
FCVC
NCP
CAEC
FAVC
CH2O
CALC
```

---

# Lifestyle and Activity Inputs

```text
FAF
TUE
SMOKE
SCC
MTRANS
```

---

# Streamlit Form Submission

The complete form generates a dictionary containing:

```text
16 predictive features
```

The payload is then sent to:

```text
POST /predict
```

through the frontend API client.

---

# Frontend API Client

HTTP communication is handled by:

```text
frontend/services/api_client.py
```

The API client provides:

```text
get_health()
get_model_info()
predict()
```

The frontend therefore avoids scattering raw HTTP request code throughout the Streamlit application.

---

# API Error Handling in the Frontend

The frontend API client converts backend failures into:

```text
APIClientError
```

When the Flask API returns a useful error message, the Streamlit interface can display it to the user.

For example:

```text
Age must be numeric.
```

instead of displaying only:

```text
HTTP 400
```

---

# Prediction Result Component

Prediction visualization is implemented in:

```text
frontend/components/prediction_result.py
```

The component displays:

```text
Human-readable predicted category
Prediction confidence
Confidence progress indicator
Seven-class probability chart
Probability ranking
Second-highest predicted class
Technical prediction data
Educational-use warning
```

---

# Human-Readable Prediction Labels

Internal model labels such as:

```text
Normal_Weight
```

are presented as:

```text
Normal Weight
```

Similarly:

```text
Obesity_Type_III
```

becomes:

```text
Obesity Type III
```

The internal machine learning class names are not modified.

Only their visual presentation changes.

---

# Prediction Confidence

The frontend displays the model's probability for the predicted class.

Example:

```text
Prediction Confidence
87.25%
```

The confidence value represents:

```text
The model's predicted probability for its selected class
```

It does not represent medical certainty.

---

# Probability Visualization

The frontend displays probabilities for all seven classes.

Example structure:

```text
Normal Weight             █████████████████
Overweight Level I        ████
Overweight Level II       ██
Insufficient Weight       █
Obesity Type I            █
Obesity Type II
Obesity Type III
```

Probabilities are also shown as a ranked table.

---

# Streamlit Session State

The most recent prediction is stored in:

```text
st.session_state
```

This allows the prediction result to persist during Streamlit reruns within the current session.

The key used is:

```text
prediction_result
```

---

# Start New Assessment

After a prediction has been generated, the interface provides:

```text
Start New Assessment
```

This clears:

```text
Current prediction
Form widget state
```

and restores the form to its default values.

---

# Backend Connection Monitoring

When Streamlit starts, it requests:

```text
GET /health
```

If Flask is available:

```text
API Connected
```

is displayed.

If Flask cannot be reached, the frontend displays an error and prevents prediction functionality from continuing.

---

# Model Information Sidebar

The Streamlit sidebar displays:

```text
API connection status
Selected model
Test accuracy
Macro F1
Number of input features
Number of target classes
```

This information is retrieved from:

```text
GET /model-info
```

rather than being manually duplicated in the frontend.

---

# Complete Application Architecture

```text
                       USER
                         │
                         ▼
                Streamlit Frontend
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
       Sidebar      Assessment Form   Result UI
                         │
                  16 Raw Features
                         │
                         ▼
                      APIClient
                         │
                    HTTP / JSON
                         │
                         ▼
                   Flask REST API
                         │
                         ▼
                  Input Validation
                         │
                         ▼
                    ModelService
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
    model_metadata.json    obesity_risk_pipeline.joblib
                                     │
                                     ▼
                           Preprocessing Pipeline
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
              Numerical          Ordinal          Nominal
               Pipeline          Pipeline          Pipeline
                    │                │                │
                    └────────────────┼────────────────┘
                                     │
                                     ▼
                           25 Transformed Features
                                     │
                                     ▼
                          Gradient Boosting Model
                                     │
                                     ▼
                              Prediction Result
                                     │
                     ┌───────────────┼───────────────┐
                     │               │               │
                     ▼               ▼               ▼
                Predicted        Confidence      Probabilities
                  Class
                     │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                              Streamlit UI
```

---

# Automated Testing

The project includes automated tests for machine learning preprocessing, Flask backend functionality, API validation, API client communication, and frontend result-processing helpers.

Tests include:

```text
Preprocessing configuration
Feature transformation
Missing-value handling
Unknown categories
Health API
Model loading
Model metadata
Prediction API
Prediction probabilities
Missing feature validation
Unexpected feature validation
Numeric type validation
Numeric range validation
Categorical validation
Non-JSON requests
404 handling
405 handling
Frontend GET requests
Frontend prediction POST request
Frontend backend-error handling
Invalid JSON responses
Prediction label formatting
Probability DataFrame generation
Probability sorting
```

---

# Running Tests

Run the entire test suite:

```bash
python -m pytest -q
```

Run only backend API tests:

```bash
python -m pytest tests/test_prediction_api.py -q
```

Run frontend API-client tests:

```bash
python -m pytest tests/test_frontend_api_client.py -q
```

Run prediction-result helper tests:

```bash
python -m pytest tests/test_prediction_result.py -q
```

All tests should pass before project changes are committed.

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/SMCodeX7/Obesity-Risk-Intelligence-System.git
```

Move into the project:

```bash
cd Obesity-Risk-Intelligence-System
```

---

# 2. Create Virtual Environment

## Windows

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

# 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Important project dependencies include:

```text
pandas
numpy
matplotlib
seaborn
jupyterlab
scikit-learn==1.8.0
pytest
shap
joblib
Flask
streamlit
requests
```

---

# Dataset Setup

Place the dataset at:

```text
data/raw/obesity.csv
```

The raw dataset is excluded from Git version control.

---

# Running the Jupyter Notebooks

Launch:

```bash
jupyter lab
```

Execute notebooks in this order:

```text
1. 01_data_understanding.ipynb
2. 02_eda.ipynb
3. 03_preprocessing.ipynb
4. 04_baseline_models.ipynb
5. 05_model_tuning.ipynb
6. 06_explainability.ipynb
```

---

# Running the Complete Application

The application currently requires two running processes.

## Terminal 1 — Flask Backend

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start Flask:

```powershell
python -m flask --app backend run --debug
```

The API runs locally at:

```text
http://127.0.0.1:5000
```

Available endpoints:

```text
GET  /health
GET  /model-info
POST /predict
```

---

# Terminal 2 — Streamlit Frontend

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start Streamlit:

```powershell
python -m streamlit run frontend/app.py
```

Open the Streamlit URL shown in the terminal.

---

# Application Request Flow

When a user submits an assessment:

```text
User enters 16 features
        ↓
Streamlit Form
        ↓
Python Dictionary
        ↓
Frontend APIClient
        ↓
POST /predict
        ↓
Flask API
        ↓
Input Validation
        ↓
Pandas DataFrame
        ↓
Saved Scikit-learn Pipeline
        ↓
Preprocessing
        ↓
Gradient Boosting Classifier
        ↓
Predicted Class
        ↓
Confidence
        ↓
Seven Class Probabilities
        ↓
JSON Response
        ↓
Streamlit
        ↓
Prediction Result UI
```

---

# Generated Reports

Machine learning reports are stored in:

```text
reports/generated/
```

Important files include:

```text
baseline_model_comparison.csv
gradient_boosting_tuning_results.csv
random_forest_tuning_results.csv
model_tuning_comparison.csv
tuning_candidates.csv
leading_model_candidate.csv
final_model_selection.csv
final_test_metrics.csv
final_classification_report.csv
final_confusion_matrix.csv
global_tree_feature_importance.csv
global_shap_feature_importance.csv
global_feature_importance_comparison.csv
local_shap_explanations.csv
ordinal_error_summary.csv
ordinal_error_by_class.csv
bmi_ablation_results.csv
gender_subgroup_performance.csv
gender_class_distribution.csv
gender_subgroup_gap_summary.csv
phase7_summary.json
```

---

# Generated Figures

Visual outputs are stored under:

```text
reports/figures/
```

Important outputs include:

```text
global_tree_feature_importance.png
global_shap_feature_importance.png
gender_subgroup_macro_f1.png
local_shap_<sample>.png
```

---

# Technology Stack

## Machine Learning

```text
Python
Pandas
NumPy
Scikit-learn
SHAP
Joblib
```

## Data Analysis

```text
Pandas
NumPy
Matplotlib
Seaborn
JupyterLab
```

## Backend

```text
Python
Flask
```

## Frontend

```text
Python
Streamlit
Requests
```

## Testing

```text
Pytest
Flask Test Client
unittest.mock
```

## Database

```text
SQLite
```

Planned for Phase 10.

## Version Control

```text
Git
GitHub
```

---

# Key Technical Decisions

## Identifier Exclusion

The `id` field is excluded from model training.

---

## Reusable Preprocessing Pipeline

All preprocessing logic is stored inside reusable Scikit-learn transformers.

---

## Stratified Data Splitting

Class proportions are maintained when dividing data into training, validation, and test subsets.

---

## Validation-Based Model Selection

Hyperparameter and model selection decisions are based on development/validation performance.

---

## Macro F1 Selection Metric

Macro F1 was emphasized because all seven obesity classes should contribute equally to model evaluation.

---

## Saved End-to-End Pipeline

The complete preprocessing and classification pipeline is persisted together.

Application code therefore provides raw features directly to the saved pipeline.

---

## No Explicit BMI Feature

BMI was evaluated experimentally but did not improve validation Macro F1.

Therefore, the original 16-feature model remains the final model.

---

## Explainability

Both:

```text
Tree-based importance
SHAP
```

were used to analyse model behaviour.

---

## Separate Backend and Frontend

Streamlit does not directly load the trained model.

Instead:

```text
Streamlit
    ↓
Flask
    ↓
ML Pipeline
```

This provides clearer separation of responsibilities.

---

## Model Loaded Once

The Flask application loads the persisted machine learning pipeline during application initialization instead of repeatedly loading it for individual requests.

---

## Input Validation Before Inference

All incoming prediction requests are validated before reaching the machine learning model.

---

## Centralized Backend Error Handling

Backend validation and HTTP errors produce structured JSON responses.

---

## Dedicated Frontend API Client

HTTP communication is implemented inside:

```text
frontend/services/api_client.py
```

instead of being spread throughout the UI.

---

## Session-Based Prediction Persistence

The most recent result is stored using Streamlit session state.

---

# Current Limitations

## Dataset Representation

Model performance depends on the characteristics of the available dataset and may not generalize equally well to all real-world populations.

---

## Generated Dataset

The competition dataset contains generated characteristics.

It should not automatically be considered representative clinical population data.

---

## Medical Use

This project is intended for:

```text
Education
Machine learning experimentation
Software engineering practice
Research demonstration
```

It is not intended for medical diagnosis.

Predictions should not replace professional medical assessment.

---

## Explainability Limitation

SHAP explains relationships inside the trained model.

It does not establish medical causation.

For example:

```text
Weight has high SHAP importance
```

does not by itself mean:

```text
Weight medically causes a particular outcome
```

---

## Subgroup Analysis

Gender subgroup class distributions are uneven.

Subgroup metrics must therefore be interpreted cautiously.

---

## Current Prediction Persistence

Prediction results currently exist only during the active Streamlit session.

They are not yet permanently stored.

Persistent storage will be introduced in:

```text
Phase 10
```

---

# Reproducibility

Where applicable, the project uses:

```text
random_state = 42
```

The final persisted model records:

```text
scikit-learn = 1.8.0
```

Using the same version is recommended when loading the serialized pipeline.

---

# Development Roadmap

## Completed

```text
Phase 1
Data Understanding

Phase 2
Exploratory Data Analysis

Phase 3
Preprocessing Pipeline

Phase 4
Baseline Model Development

Phase 5
Hyperparameter Tuning

Phase 6
Final Model Selection and Evaluation

Phase 7
Explainability and Advanced Evaluation

Phase 8
Flask REST API

Phase 9
Streamlit Frontend
```

---

# Phase 10 — SQLite and Full Integration

The next phase will introduce persistent application data.

Planned functionality includes:

```text
SQLite database
        ↓
Prediction history
        ↓
Prediction timestamps
        ↓
Stored assessment inputs
        ↓
Stored predicted class
        ↓
Stored confidence
        ↓
Prediction history interface
```

The expected architecture will become:

```text
User
 ↓
Streamlit
 ↓
Flask REST API
 ↓
Machine Learning Pipeline
 ↓
Prediction
 ↓
SQLite Database
 ↓
Prediction History
```

---

# Phase 11 — Deployment and Final Documentation

The final phase will focus on:

```text
Final application testing
Code cleanup
Configuration review
Environment configuration
Deployment preparation
Architecture documentation
Final README review
Project screenshots
Final diagrams
Academic documentation
Final project demonstration preparation
```

---

# Project Progress Visualization

```text
Data Understanding       ██████████ 100%
EDA                      ██████████ 100%
Preprocessing            ██████████ 100%
Baseline Modelling       ██████████ 100%
Model Tuning             ██████████ 100%
Final Model Evaluation   ██████████ 100%
Explainability           ██████████ 100%
Flask REST API           ██████████ 100%
Streamlit Frontend       ██████████ 100%
SQLite Integration       ░░░░░░░░░░   0%
Deployment               ░░░░░░░░░░   0%
```

---

# Current System Architecture

```text
┌──────────────────────────────────────────┐
│                   USER                   │
└─────────────────────┬────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────┐
│          STREAMLIT FRONTEND              │
│                                          │
│  • Assessment Form                       │
│  • API Status                            │
│  • Model Information                     │
│  • Prediction Result                     │
│  • Confidence                            │
│  • Probability Visualization             │
└─────────────────────┬────────────────────┘
                      │
                   HTTP/JSON
                      │
                      ▼
┌──────────────────────────────────────────┐
│              FLASK REST API              │
│                                          │
│  GET  /health                            │
│  GET  /model-info                        │
│  POST /predict                           │
└─────────────────────┬────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────┐
│             INPUT VALIDATION             │
└─────────────────────┬────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────┐
│               MODEL SERVICE              │
└─────────────────────┬────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────┐
│       SAVED SCIKIT-LEARN PIPELINE        │
│                                          │
│  Numerical Preprocessing                 │
│  Ordinal Preprocessing                   │
│  Nominal Preprocessing                   │
│             ↓                            │
│      Gradient Boosting                   │
└─────────────────────┬────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────┐
│             PREDICTION RESULT            │
│                                          │
│  • Predicted Class                       │
│  • Confidence                            │
│  • 7 Class Probabilities                 │
└─────────────────────┬────────────────────┘
                      │
                      ▼
              Streamlit Result UI

                      │
                      ▼

              SQLite Integration
                 Phase 10 — Next
```

---

# License

This project is licensed under the:

```text
MIT License
```

See:

```text
LICENSE
```

for details.

---

# Current Milestone

## Phases 1–9 Complete

The project currently provides:

```text
Data Understanding                    ✅
Exploratory Data Analysis             ✅
Reusable Preprocessing                ✅
Baseline Model Comparison             ✅
Hyperparameter Tuning                 ✅
Final Model Selection                 ✅
Final Model Evaluation                ✅
Saved ML Pipeline                     ✅
Model Metadata                        ✅
Global Feature Importance             ✅
Global SHAP Analysis                  ✅
Local SHAP Explanations               ✅
Ordinal Error Analysis                ✅
BMI Ablation                          ✅
Gender Subgroup Analysis              ✅
Flask Application Factory             ✅
Health API                            ✅
Model Information API                 ✅
Prediction API                        ✅
Input Validation                      ✅
Prediction Confidence                 ✅
Seven-Class Probabilities             ✅
Centralized Backend Errors            ✅
Streamlit Frontend                    ✅
16-Feature Assessment Form            ✅
Frontend API Client                   ✅
Prediction Result Interface           ✅
Probability Visualization             ✅
Session-Based Result Persistence      ✅
Start New Assessment                  ✅
Frontend Error Handling               ✅
Automated Testing                     ✅
```

# Next Milestone

## Phase 10 — SQLite and Full Integration

The next objective is to make prediction data persistent and introduce prediction-history functionality.