# Obesity Risk Intelligence System

A machine learning-based obesity risk classification system that predicts an individual's obesity-risk category using demographic, physical, dietary, lifestyle, and activity-related information.

The project follows a complete machine learning workflow from data understanding and exploratory analysis through model development, hyperparameter tuning, final evaluation, explainability, REST API development, and eventually a user-facing application.

## Current Status

**Phases 1–8 completed**

The machine learning model has been developed, evaluated, explained, saved, and exposed through a Flask REST API.

The next development stage is:

**Phase 9 — Streamlit Frontend**

---

# Project Objectives

The main objectives of this project are to:

- Analyse obesity-related demographic and lifestyle data.
- Build a reliable multiclass obesity-risk classifier.
- Develop reusable preprocessing logic.
- Compare multiple machine learning algorithms.
- Tune the strongest models using cross-validation.
- Evaluate the selected model on a reserved test set.
- Explain model behaviour using feature importance and SHAP.
- Analyse ordinal prediction errors.
- Compare model performance with and without an explicit BMI feature.
- Perform descriptive subgroup performance analysis.
- Save the complete trained machine learning pipeline.
- Expose the trained model through a Flask REST API.
- Validate incoming prediction requests.
- Return predicted class, confidence, and class probabilities.
- Provide structured API error responses.
- Later provide a user-friendly Streamlit interface and prediction history.

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
| Phase 9 | Streamlit Frontend | ⏳ Next |
| Phase 10 | SQLite and Full Integration | ⬜ Planned |
| Phase 11 | Deployment and Final Documentation | ⬜ Planned |

---

# Dataset

The project uses the generated obesity dataset associated with the Kaggle Playground Series Season 4 Episode 2 competition.

The local dataset is expected at:

```text
data/raw/obesity.csv
```

The raw dataset is intentionally excluded from Git version control.

## Dataset Size

```text
20,758 records
18 columns
```

The dataset contains:

```text
16 predictive features
1 identifier column
1 target column
```

The `id` column is excluded from model training.

---

# Target Variable

The prediction target is:

```text
NObeyesdad
```

The model predicts one of seven classes:

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

The final model uses 16 original predictive features.

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
| TUE | Time using technological devices |

---

## Ordinal Features

```text
CAEC
CALC
```

### CAEC

Food consumption between meals:

```text
no
Sometimes
Frequently
Always
```

### CALC

Alcohol consumption:

```text
no
Sometimes
Frequently
```

These values contain an inherent ordering and are encoded using an ordinal encoder.

---

## Nominal Features

```text
Gender
family_history_with_overweight
FAVC
SMOKE
SCC
MTRANS
```

These variables do not have a meaningful numerical ordering and are processed using one-hot encoding.

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
│       └── obesity.csv
│
├── database/
│   └── .gitkeep
│
├── frontend/
│   └── .gitkeep
│
├── models/
│   ├── model_metadata.json
│   └── obesity_risk_pipeline.joblib
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
│   └── test_api_errors.py
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

# Phase 1 — Data Understanding

The first phase focused on understanding the dataset before performing any modelling.

The analysis included:

- Dataset dimensions
- Column names
- Data types
- Target classes
- Missing values
- Duplicate records
- Numerical-variable inspection
- Categorical-variable inspection
- Target-class distribution

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

Exploratory Data Analysis was performed to better understand patterns within the dataset.

The analysis included:

- Obesity-class distribution
- Numerical feature distributions
- Categorical feature distributions
- Age patterns
- Height patterns
- Weight patterns
- Food-consumption behaviour
- Physical-activity behaviour
- Water consumption
- Transportation methods
- Correlation analysis
- Class-level feature comparisons

Notebook:

```text
notebooks/02_eda.ipynb
```

The EDA stage helped identify relationships between physical measurements, eating behaviour, activity levels, and obesity categories.

---

# Phase 3 — Preprocessing Pipeline

Reusable preprocessing logic is implemented in:

```text
src/preprocessing.py
```

The preprocessing system uses Scikit-learn's:

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

- Missing-value handling
- Consistent feature scaling

---

## Ordinal Pipeline

Ordinal variables use:

```text
SimpleImputer(strategy="most_frequent")
OrdinalEncoder()
```

Unknown categories are handled using:

```text
unknown_value = -1
```

This prevents unseen ordinal values from automatically crashing the preprocessing pipeline.

---

## Nominal Pipeline

Nominal variables use:

```text
SimpleImputer(strategy="most_frequent")
OneHotEncoder(handle_unknown="ignore")
```

This allows previously unseen nominal categories to be safely handled during transformation.

---

# Feature Transformation

The application accepts:

```text
16 raw predictive features
```

After preprocessing, the final pipeline produces:

```text
25 transformed features
```

These transformed features are passed to the Gradient Boosting classifier.

---

# Preprocessing Tests

Automated preprocessing tests are located in:

```text
tests/test_preprocessing.py
```

The tests verify:

- Correct feature grouping
- Independent preprocessor creation
- Successful feature transformation
- Missing-value handling
- Unknown-category handling

Tests can be run using:

```bash
python -m pytest
```

---

# Phase 4 — Baseline Models

Several machine learning classifiers were trained and compared.

The baseline models included:

```text
Dummy Classifier
Logistic Regression
Decision Tree
Random Forest
Gradient Boosting
```

## Validation Performance

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

Training and validation Macro F1 scores were also compared.

```text
Logistic Regression
Train Macro F1      ≈ 0.8443
Validation Macro F1 ≈ 0.8418

Gradient Boosting
Train Macro F1      ≈ 0.9126
Validation Macro F1 ≈ 0.8930

Random Forest
Train Macro F1      ≈ 1.0000
Validation Macro F1 ≈ 0.8849

Decision Tree
Train Macro F1      ≈ 1.0000
Validation Macro F1 ≈ 0.8308
```

Random Forest and Decision Tree showed larger train-validation gaps.

Gradient Boosting and Random Forest were selected for hyperparameter tuning.

---

# Phase 5 — Hyperparameter Tuning

The strongest baseline models were:

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
5-fold Stratified Cross Validation
```

The main refit metric was:

```text
Macro F1
```

Macro F1 was used because each obesity class should contribute equally to the overall evaluation.

---

## Tuned Model Performance

| Candidate | Validation Macro F1 |
|---|---:|
| Tuned Gradient Boosting | **0.8978** |
| Tuned Random Forest | **0.8967** |
| Baseline Gradient Boosting | 0.8930 |
| Baseline Random Forest | 0.8849 |

The final selected candidate was:

```text
Tuned Gradient Boosting
```

Notebook:

```text
notebooks/05_model_tuning.ipynb
```

---

# Selected Gradient Boosting Configuration

The selected model uses:

```text
n_estimators = 100
learning_rate = 0.15
max_depth = 3
min_samples_split = 5
min_samples_leaf = 2
subsample = 0.8
max_features = 0.8
random_state = 42
```

---

# Phase 6 — Final Model Evaluation

After model selection, the chosen configuration was refitted using the development data and evaluated on the reserved test set.

The final saved object contains:

```text
Preprocessing Pipeline
        +
Gradient Boosting Classifier
```

Therefore, application code can provide the original 16 features directly to the model pipeline.

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

of final test examples.

---

# Final Class Performance

The strongest-performing obesity categories included:

```text
Obesity_Type_III
Obesity_Type_II
Insufficient_Weight
```

The more difficult categories included:

```text
Overweight_Level_I
Overweight_Level_II
```

This is consistent with the fact that neighbouring weight-status classes can have overlapping characteristics.

---

# Saved Model

The trained pipeline is stored at:

```text
models/obesity_risk_pipeline.joblib
```

Metadata is stored at:

```text
models/model_metadata.json
```

The metadata includes:

- Project name
- Selected model
- Model family
- Configuration
- Random state
- Predictive feature list
- Number of raw features
- Number of transformed features
- Target classes
- Development record count
- Test record count
- Validation Macro F1
- Final test metrics
- Scikit-learn version

The saved pipeline was produced using:

```text
scikit-learn 1.8.0
```

The same version should therefore be used when loading the serialized model.

---

# Phase 7 — Explainability and Advanced Evaluation

Phase 7 investigated how the frozen final model makes predictions and how prediction errors behave.

Notebook:

```text
notebooks/06_explainability.ipynb
```

Phase 7 includes:

```text
Final model verification
Global tree-based feature importance
Global SHAP analysis
Local SHAP explanations
Ordinal error analysis
BMI ablation experiment
Gender subgroup performance analysis
```

---

# Global Tree Feature Importance

The five most important raw features according to the Gradient Boosting feature-importance calculation were:

```text
1. Weight
2. Gender
3. FCVC
4. Height
5. Age
```

---

# Global SHAP Feature Importance

SHAP identified the following leading raw features:

```text
1. Weight
2. FCVC
3. Height
4. Gender
5. Age
```

Both approaches therefore highlighted a similar group of highly influential features.

Important recurring variables included:

```text
Weight
Height
FCVC
Gender
Age
```

---

# Local SHAP Explanations

Local SHAP analysis was performed on:

```text
3 correctly classified test examples
3 incorrectly classified test examples
```

For each example, the strongest feature contributions to the predicted class were identified.

Generated local explanation files are stored under:

```text
reports/figures/
```

with names such as:

```text
local_shap_<sample_id>.png
```

The corresponding explanation data is stored in:

```text
reports/generated/local_shap_explanations.csv
```

---

# Ordinal Error Analysis

The obesity classes can be interpreted in an increasing weight-status order:

```text
Insufficient_Weight
        ↓
Normal_Weight
        ↓
Overweight_Level_I
        ↓
Overweight_Level_II
        ↓
Obesity_Type_I
        ↓
Obesity_Type_II
        ↓
Obesity_Type_III
```

Prediction errors were therefore analysed according to the distance between the true class and predicted class.

## Ordinal Error Results

```text
Mean ordinal distance:
0.1092

Exact prediction rate:
90.75%

Adjacent-class error rate:
7.90%

Severe error rate:
1.35%
```

A severe error is defined as:

```text
Ordinal distance >= 2 classes
```

Most prediction errors therefore occur between neighbouring classes rather than between widely separated obesity-risk categories.

---

# BMI Ablation Experiment

BMI was calculated using:

```text
BMI = Weight / Height²
```

Two configurations were compared using development/validation data:

```text
Original 16 features
```

and:

```text
Original 16 features + BMI
```

## Results

| Configuration | Validation Macro F1 |
|---|---:|
| Original 16 Features | **0.8978** |
| Original + BMI | **0.8946** |

Difference:

```text
BMI Macro F1 delta = -0.00316
```

Adding BMI did not improve validation performance.

Therefore, the original 16-feature model was retained.

---

# Gender Subgroup Analysis

The final model was also evaluated across gender subgroups.

The observed Macro F1 gap was approximately:

```text
0.0186
```

The dataset's obesity-class distributions differ substantially between gender groups.

Therefore, these subgroup results are interpreted as:

```text
Descriptive diagnostic analysis
```

rather than definitive evidence that the model is fair or unfair.

Further fairness evaluation would require more balanced and representative subgroup data.

---

# Phase 7 Summary

The Phase 7 summary is stored at:

```text
reports/generated/phase7_summary.json
```

Key results:

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

Phase 8 converts the trained machine learning model into a reusable REST API.

The backend is implemented using:

```text
Flask
```

and follows an application-factory architecture.

The API separates:

```text
Routes
Services
Input validation
Model loading
Error handling
```

instead of placing the entire application inside one Python file.

---

# Flask Backend Architecture

```text
Client
   │
   ▼
Flask Application
   │
   ├── GET /health
   │
   ├── GET /model-info
   │
   └── POST /predict
   │
   ▼
Input Validation
   │
   ▼
ModelService
   │
   ├── Load model metadata
   ├── Verify Scikit-learn version
   └── Load saved ML pipeline
   │
   ▼
Scikit-learn Pipeline
   │
   ├── Numerical preprocessing
   ├── Ordinal preprocessing
   ├── Nominal preprocessing
   └── Gradient Boosting
   │
   ▼
Prediction
   │
   ├── Predicted class
   ├── Confidence
   └── Class probabilities
```

---

# Flask Application Factory

The Flask backend uses:

```python
create_app()
```

rather than creating one global application containing all logic.

This allows application initialization to be organized centrally.

The application factory:

```text
Creates Flask application
        ↓
Applies configuration
        ↓
Creates ModelService
        ↓
Loads saved model
        ↓
Registers ModelService
        ↓
Registers API blueprints
        ↓
Registers error handlers
        ↓
Returns application
```

---

# Model Service

Model-related logic is implemented in:

```text
backend/services/model_service.py
```

`ModelService` is responsible for:

```text
Loading model_metadata.json
Checking the Scikit-learn version
Loading obesity_risk_pipeline.joblib
Returning model information
Creating prediction input DataFrames
Running predict()
Running predict_proba()
Returning prediction results
```

The trained model is loaded when the Flask application is created rather than being loaded again for every request.

---

# Input Validation

Prediction validation is implemented in:

```text
backend/services/input_validator.py
```

A prediction request must:

```text
Be a JSON object
Contain all 16 required features
Contain no unexpected features
Use valid numeric types
Use finite numerical values
Remain inside configured sanity ranges
Use supported categorical values
```

Invalid requests are rejected before the model receives the input.

---

# API Endpoints

The Flask API currently exposes three endpoints.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check whether the API is running |
| GET | `/model-info` | Return information about the trained model |
| POST | `/predict` | Generate an obesity-risk prediction |

---

# GET /health

Used to verify API availability.

Example request:

```text
GET /health
```

Example response:

```json
{
    "service": "obesity-risk-api",
    "status": "ok"
}
```

HTTP status:

```text
200 OK
```

---

# GET /model-info

Returns information about the loaded machine learning model.

Example request:

```text
GET /model-info
```

The response includes information such as:

```text
Project name
Selected model
Model family
Configuration
Predictive feature count
Transformed feature count
Target class count
Predictive feature names
Target class names
Scikit-learn version
Final test performance
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

The `/predict` endpoint accepts the 16 raw predictive features.

Example request body:

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

A successful prediction returns:

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

The values in this example are **illustrative only**.

Actual:

```text
predicted_class
confidence
probabilities
```

are calculated dynamically by the trained machine learning model.

The returned probability dictionary contains probabilities for all seven obesity classes.

The probabilities should sum approximately to:

```text
1.0
```

The confidence corresponds to the highest predicted class probability.

---

# API Validation Errors

Invalid requests return structured JSON.

Example:

```json
{
    "error": "validation_error",
    "message": "Age must be numeric."
}
```

HTTP status:

```text
400 Bad Request
```

Validation protects the prediction pipeline against malformed application input.

---

# 404 Error Response

Unknown endpoints return:

```json
{
    "error": "not_found",
    "message": "The requested endpoint does not exist."
}
```

HTTP status:

```text
404 Not Found
```

---

# 405 Error Response

Using an unsupported HTTP method returns:

```json
{
    "error": "method_not_allowed",
    "message": "The HTTP method is not allowed for this endpoint."
}
```

HTTP status:

```text
405 Method Not Allowed
```

For example:

```text
GET /predict
```

is rejected because `/predict` accepts:

```text
POST
```

only.

---

# 500 Error Response

Unexpected internal API failures return a structured response:

```json
{
    "error": "internal_server_error",
    "message": "An unexpected server error occurred."
}
```

HTTP status:

```text
500 Internal Server Error
```

Detailed internal exception information is intentionally not exposed directly through the API response.

---

# API Testing

Phase 8 includes automated tests for:

```text
Health endpoint
Model loading
Model metadata endpoint
Valid prediction
Prediction confidence
Seven class probabilities
Probability sum
Missing features
Unexpected features
Wrong numerical types
Numerical range validation
Invalid categorical values
Non-JSON requests
Unknown endpoints
Unsupported HTTP methods
```

Run all tests with:

```bash
python -m pytest -q
```

All tests should complete without failures before a Phase 8 change is considered complete.

---

# Running the Flask API

Activate the virtual environment first.

## Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Start Flask:

```powershell
python -m flask --app backend run --debug
```

The development server should start at:

```text
http://127.0.0.1:5000
```

Available endpoints:

```text
http://127.0.0.1:5000/health

http://127.0.0.1:5000/model-info

http://127.0.0.1:5000/predict
```

`/predict` must be called using an HTTP `POST` request.

---

# Example Prediction with PowerShell

Create the request body:

```powershell
$body = @{
    Age = 25
    Height = 1.70
    Weight = 70
    FCVC = 2
    NCP = 3
    CH2O = 2
    FAF = 1
    TUE = 1
    CAEC = "Sometimes"
    CALC = "no"
    Gender = "Male"
    family_history_with_overweight = "yes"
    FAVC = "yes"
    SMOKE = "no"
    SCC = "no"
    MTRANS = "Public_Transportation"
} | ConvertTo-Json
```

Send the request:

```powershell
$response = Invoke-RestMethod `
    -Uri http://127.0.0.1:5000/predict `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

Display the full result:

```powershell
$response | ConvertTo-Json -Depth 5
```

---

# Generated Reports

Machine learning reports are stored in:

```text
reports/generated/
```

Important reports include:

```text
baseline_model_comparison.csv
gradient_boosting_tuning_results.csv
random_forest_tuning_results.csv
model_tuning_comparison.csv
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

Visual outputs are stored in:

```text
reports/figures/
```

Important figures include:

```text
global_tree_feature_importance.png
global_shap_feature_importance.png
gender_subgroup_macro_f1.png
local_shap_<sample_id>.png
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/SMCodeX7/Obesity-Risk-Intelligence-System.git
```

Move into the repository:

```bash
cd Obesity-Risk-Intelligence-System
```

---

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Important runtime dependencies include:

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
```

---

# Dataset Setup

Place the obesity dataset at:

```text
data/raw/obesity.csv
```

The raw dataset is ignored by Git.

---

# Running the Notebooks

Launch JupyterLab:

```bash
jupyter lab
```

Study or execute the notebooks in this order:

```text
1. notebooks/01_data_understanding.ipynb
2. notebooks/02_eda.ipynb
3. notebooks/03_preprocessing.ipynb
4. notebooks/04_baseline_models.ipynb
5. notebooks/05_model_tuning.ipynb
6. notebooks/06_explainability.ipynb
```

---

# Running Automated Tests

Run the complete test suite:

```bash
python -m pytest -q
```

Run only API error tests:

```bash
python -m pytest tests/test_api_errors.py -q
```

Run prediction tests:

```bash
python -m pytest tests/test_prediction_api.py -q
```

---

# Complete System Architecture So Far

```text
                        User / API Client
                               │
                               ▼
                        Flask REST API
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
             /health       /model-info     /predict
                                               │
                                               ▼
                                      Input Validation
                                               │
                                               ▼
                                         ModelService
                                               │
                     ┌─────────────────────────┴────────────────────┐
                     │                                              │
                     ▼                                              ▼
          model_metadata.json                       obesity_risk_pipeline.joblib
                                                                    │
                                                                    ▼
                                                        Scikit-learn Pipeline
                                                                    │
                        ┌───────────────────────────────────────────┼───────────────────────────────────┐
                        │                                           │                                   │
                        ▼                                           ▼                                   ▼
                Numerical Pipeline                         Ordinal Pipeline                     Nominal Pipeline
                        │                                           │                                   │
                Median Imputation                         Most Frequent                          Most Frequent
                        │                                   Imputation                              Imputation
                        ▼                                           │                                   │
                Standard Scaling                                  ▼                                   ▼
                                                        Ordinal Encoding                      One-Hot Encoding
                        └───────────────────────────────────────────┼───────────────────────────────────┘
                                                                    │
                                                                    ▼
                                                         25 Transformed Features
                                                                    │
                                                                    ▼
                                                        Tuned Gradient Boosting
                                                                    │
                                                                    ▼
                                                       Obesity Risk Prediction
                                                                    │
                                     ┌──────────────────────────────┼──────────────────────────────┐
                                     │                              │                              │
                                     ▼                              ▼                              ▼
                              Predicted Class                   Confidence                   Probabilities
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

## Data Analysis and Visualization

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

## Testing

```text
Pytest
Flask Test Client
```

## Version Control

```text
Git
GitHub
```

## Planned Frontend

```text
Streamlit
```

## Planned Database

```text
SQLite
```

---

# Key Technical Decisions

The project applies several practices intended to improve reliability and maintainability.

### Identifier Removal

The dataset `id` field is not used as a predictive feature.

### Reusable Preprocessing

Feature preprocessing is implemented as reusable Scikit-learn pipeline components.

### Safe Category Handling

Unknown categorical values are handled by the preprocessing system.

### Stratified Data Splitting

Dataset splits preserve class proportions.

### Validation-Based Model Selection

Model selection and tuning are performed using development/validation data rather than repeatedly tuning against the final test result.

### Macro F1

Macro F1 is used as a major evaluation metric because the classification task contains seven classes.

### Cross-Validation

Hyperparameter tuning uses stratified cross-validation.

### Frozen Final Pipeline

The selected preprocessing and model components are persisted together.

### Explainability

Tree importance and SHAP are both used to investigate model behaviour.

### BMI Ablation

BMI is tested as an additional derived feature without replacing the frozen final model.

### Subgroup Analysis

Subgroup metrics are interpreted cautiously due to differences in subgroup class distributions.

### Model Service

Model loading is separated from HTTP route handling.

### Load Model Once

The serialized ML pipeline is loaded during Flask application initialization rather than on every prediction request.

### Request Validation

Incoming API data is checked before being sent to the model.

### Centralized Error Handling

Validation errors and HTTP errors return consistent JSON responses.

---

# Limitations

## Dataset Representation

Model performance depends on the characteristics of the available dataset and may not generalize equally well to every real-world population.

## Generated Dataset

The competition dataset contains generated characteristics and should not automatically be treated as representative clinical population data.

## Medical Use

This project is intended for:

```text
Machine learning
Software engineering
Educational demonstration
Research experimentation
```

It is **not a medical diagnostic system**.

Predictions should not replace professional medical assessment.

## Explainability

SHAP values explain model behaviour.

They do not establish medical causation.

For example:

```text
A feature having high SHAP importance
```

does not mean:

```text
The feature medically causes obesity.
```

## Subgroup Evaluation

Class distributions differ substantially between some gender subgroups.

Subgroup comparisons should therefore be interpreted carefully.

---

# Reproducibility

Where applicable, the project uses:

```text
random_state = 42
```

The persisted final model records:

```text
scikit-learn version = 1.8.0
```

Using the same Scikit-learn version is recommended when loading the model.

---

# Development Roadmap

## Completed

```text
Phase 1  — Data Understanding
Phase 2  — Exploratory Data Analysis
Phase 3  — Preprocessing
Phase 4  — Baseline Models
Phase 5  — Hyperparameter Tuning
Phase 6  — Final Model Evaluation
Phase 7  — Explainability and Advanced Evaluation
Phase 8  — Flask REST API
```

## Next

```text
Phase 9 — Streamlit Frontend
```

Phase 9 will create a graphical interface that allows a user to:

```text
Enter obesity-risk features
        ↓
Submit assessment
        ↓
Call Flask /predict
        ↓
Display predicted obesity category
        ↓
Display confidence
        ↓
Display class probabilities
```

## Planned

```text
Phase 10 — SQLite and Full Integration
Phase 11 — Deployment and Final Documentation
```

---

# Future Application Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 │ HTTP / JSON
 ▼
Flask REST API
 │
 ├── Input Validation
 │
 ├── Model Information
 │
 ├── Prediction Service
 │
 └── Error Handling
 │
 ▼
Saved Scikit-learn Pipeline
 │
 ├── Preprocessing
 │
 └── Tuned Gradient Boosting
 │
 ▼
Prediction Result
 │
 ├── Predicted Class
 ├── Confidence
 └── Probabilities
 │
 ▼
SQLite Prediction History
```

SQLite integration will be implemented in a later phase.

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
Streamlit Frontend       ░░░░░░░░░░   0%
Database Integration     ░░░░░░░░░░   0%
Deployment               ░░░░░░░░░░   0%
```

---

# License

This project is licensed under the MIT License.

See:

```text
LICENSE
```

for license information.

---

# Current Milestone

## Phases 1–8 Complete

The following components are now available:

```text
Dataset analysis
Exploratory data analysis
Reusable preprocessing
Baseline model comparison
Hyperparameter tuning
Final model selection
Final model evaluation
Saved ML pipeline
Model metadata
Global explainability
Local explainability
Ordinal error analysis
BMI feature ablation
Subgroup analysis
Flask application factory
Health endpoint
Model information endpoint
Validated prediction endpoint
Prediction confidence
Seven-class probabilities
Centralized API error handling
Automated backend tests
```

The next milestone is:

# Phase 9 — Streamlit Frontend

The Streamlit interface will provide the first user-facing layer of the Obesity Risk Intelligence System.