# Obesity Risk Intelligence System

A complete machine learning application for predicting obesity-risk categories from demographic, eating-habit, lifestyle, and physical characteristics.

The system combines a trained Scikit-learn machine learning pipeline with a Flask REST API, Streamlit frontend, SQLite prediction history, and downloadable PDF assessment reports.

> **Important:** This project is developed for educational and research purposes. Predictions produced by this system are not medical diagnoses and should not replace professional healthcare advice or clinical assessment.

---

## Project Status

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
| Phase 10 | SQLite and Full Application Integration | ✅ Complete |
| Phase 11 | Final UI Redesign, Deployment and Documentation | ⏳ Next |

---

# 1. Project Overview

The **Obesity Risk Intelligence System** is an end-to-end machine learning application designed to classify users into one of seven obesity-risk categories.

The project covers the complete machine learning lifecycle:

- Dataset understanding
- Exploratory data analysis
- Data preprocessing
- Feature engineering
- Model development
- Model comparison
- Hyperparameter tuning
- Final model evaluation
- Explainability
- BMI ablation analysis
- Ordinal prediction-error analysis
- Subgroup analysis
- REST API development
- Streamlit frontend development
- SQLite persistence
- Prediction-history management
- PDF assessment-report generation
- Automated testing
- Full application integration

The final predictive model is a tuned **Gradient Boosting Classifier** wrapped inside a Scikit-learn Pipeline.

---

# 2. System Architecture

The current system architecture is:

```text
User
 │
 ▼
Streamlit Frontend
 │
 ▼
Frontend API Client
 │
 ▼
Flask REST API
 │
 ├── Input Validation
 │
 ▼
Scikit-learn Pipeline
 │
 ├── Preprocessing
 │   ├── Numerical processing
 │   ├── Ordinal encoding
 │   └── One-hot encoding
 │
 └── Tuned Gradient Boosting Classifier
 │
 ▼
Prediction Result
 │
 ├── Predicted Class
 ├── Confidence
 └── 7 Class Probabilities
 │
 ▼
SQLite Database
 │
 ├── Prediction History
 └── Saved Assessment
        │
        ▼
   PDF Report Service
        │
        ▼
 Downloadable PDF
```

---

# 3. Main Features

## Machine Learning

- Seven-class obesity-risk classification
- Scikit-learn Pipeline
- Automated preprocessing
- Numerical feature scaling
- Ordinal feature encoding
- Nominal one-hot encoding
- Stratified train/validation/test splitting
- Multiple baseline model comparison
- Hyperparameter tuning
- Final independent test-set evaluation
- Class-level evaluation
- Explainability analysis
- BMI feature ablation
- Ordinal error analysis
- Gender subgroup evaluation

## Backend

- Flask REST API
- Centralized validation
- Centralized error handling
- Model loading service
- Model metadata endpoint
- Health endpoint
- Prediction endpoint
- SQLite integration
- Prediction persistence
- Prediction-history API
- Individual prediction retrieval
- PDF report endpoint

## Frontend

- Streamlit application
- Sidebar navigation
- Guided obesity-risk assessment form
- Model information display
- Prediction result display
- Confidence visualization
- Seven-class probability visualization
- Probability ranking
- Prediction history
- Previous assessment retrieval
- PDF report download
- Educational disclaimer

## Persistence

Every successful prediction is automatically stored in SQLite.

Stored information includes:

- 16 predictive input features
- Predicted class
- Confidence
- Seven prediction probabilities
- Model name
- Scikit-learn version
- Creation timestamp

---

# 4. Dataset

The project uses the obesity-risk dataset associated with the Kaggle Playground Series Season 4 Episode 2.

Local dataset location:

```text
data/raw/obesity.csv
```

The raw dataset itself is intentionally excluded from Git tracking.

Dataset characteristics:

| Property | Value |
|---|---:|
| Total Records | 20,758 |
| Original Columns | 18 |
| Predictive Features | 16 |
| Target Classes | 7 |
| Missing Values | 0 |
| Duplicate Records | 0 |

The original `id` column is excluded from model training.

---

# 5. Target Variable

The prediction target is:

```text
NObeyesdad
```

The seven target classes are:

```text
Insufficient_Weight
Normal_Weight
Overweight_Level_I
Overweight_Level_II
Obesity_Type_I
Obesity_Type_II
Obesity_Type_III
```

Readable versions used by the interface are:

| Internal Class | Display Name |
|---|---|
| `Insufficient_Weight` | Insufficient Weight |
| `Normal_Weight` | Normal Weight |
| `Overweight_Level_I` | Overweight Level I |
| `Overweight_Level_II` | Overweight Level II |
| `Obesity_Type_I` | Obesity Type I |
| `Obesity_Type_II` | Obesity Type II |
| `Obesity_Type_III` | Obesity Type III |

---

# 6. Predictive Features

The final model uses **16 predictive features**.

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

## Ordinal Features

```text
CAEC
CALC
```

Ordinal category orders:

### CAEC

```text
no
Sometimes
Frequently
Always
```

### CALC

```text
no
Sometimes
Frequently
```

## Nominal Features

```text
Gender
family_history_with_overweight
FAVC
SMOKE
SCC
MTRANS
```

---

# 7. Feature Meanings

| Feature | Description |
|---|---|
| Age | Age of the individual |
| Height | Height in meters |
| Weight | Weight in kilograms |
| Gender | Gender category |
| family_history_with_overweight | Family history of overweight |
| FAVC | Frequent consumption of high-calorie food |
| FCVC | Frequency of vegetable consumption |
| NCP | Number of main meals |
| CAEC | Food consumption between meals |
| SMOKE | Smoking status |
| CH2O | Daily water consumption |
| SCC | Calorie consumption monitoring |
| FAF | Physical activity frequency |
| TUE | Time using technology devices |
| CALC | Alcohol consumption |
| MTRANS | Main transportation method |

---

# 8. Data Splitting Strategy

The dataset is divided using **stratified sampling**.

```text
Training Set      70%
Validation Set    15%
Test Set          15%
```

Final record counts:

| Dataset | Records |
|---|---:|
| Training | 14,530 |
| Validation | 3,114 |
| Test | 3,114 |
| Total | 20,758 |

Random state:

```text
42
```

The test set remains isolated during model development and tuning.

---

# 9. Preprocessing Pipeline

Preprocessing is implemented in:

```text
src/preprocessing.py
```

The preprocessing pipeline contains three branches.

## Numerical Pipeline

```text
Missing-value handling
        ↓
Median Imputation
        ↓
Standard Scaling
```

## Ordinal Pipeline

```text
Missing-value handling
        ↓
Most Frequent Imputation
        ↓
Ordinal Encoding
```

Unknown ordinal values are encoded using:

```text
-1
```

## Nominal Pipeline

```text
Missing-value handling
        ↓
Most Frequent Imputation
        ↓
One-Hot Encoding
```

Unknown nominal categories are ignored safely.

After transformation, the 16 original predictive features become:

```text
25 transformed features
```

---

# 10. Baseline Models

Several classification models were evaluated.

| Model | Validation Accuracy | Validation Macro F1 |
|---|---:|---:|
| Gradient Boosting | 0.90334 | 0.89303 |
| Random Forest | 0.89563 | 0.88486 |
| Logistic Regression | 0.85806 | 0.84181 |
| Decision Tree | 0.84522 | 0.83080 |
| Dummy Classifier | 0.19493 | 0.04661 |

Gradient Boosting and Random Forest were selected for tuning.

---

# 11. Overfitting Analysis

Training and validation Macro F1 scores were compared.

| Model | Train Macro F1 | Validation Macro F1 | Gap |
|---|---:|---:|---:|
| Logistic Regression | 0.8443 | 0.8418 | 0.0025 |
| Gradient Boosting | 0.9126 | 0.8930 | 0.0196 |
| Random Forest | 1.0000 | 0.8849 | 0.1151 |
| Decision Tree | 1.0000 | 0.8308 | 0.1692 |

Gradient Boosting demonstrated a better balance between predictive performance and generalization.

---

# 12. Hyperparameter Tuning

Gradient Boosting and Random Forest were tuned.

Final validation ranking:

| Candidate | Validation Macro F1 |
|---|---:|
| Tuned Gradient Boosting | **0.897776** |
| Tuned Random Forest | 0.896691 |
| Baseline Gradient Boosting | 0.893031 |
| Baseline Random Forest | 0.884858 |

The selected model was:

```text
Tuned Gradient Boosting
```

---

# 13. Final Gradient Boosting Configuration

```python
GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.15,
    max_depth=3,
    min_samples_split=5,
    min_samples_leaf=2,
    subsample=0.8,
    max_features=0.8,
    random_state=42
)
```

---

# 14. Final Test Performance

The final selected model was evaluated once on the independent test set.

| Metric | Score |
|---|---:|
| Accuracy | **0.907514** |
| Balanced Accuracy | **0.897642** |
| Macro F1 | **0.897328** |
| Weighted F1 | **0.907214** |

Approximate test accuracy:

```text
90.75%
```

---

# 15. Class-Level Performance

Final test F1 scores:

| Target Class | F1 Score |
|---|---:|
| Insufficient Weight | 0.9271 |
| Normal Weight | 0.8677 |
| Overweight Level I | 0.7871 |
| Overweight Level II | 0.8220 |
| Obesity Type I | 0.9020 |
| Obesity Type II | 0.9796 |
| Obesity Type III | 0.9959 |

The model performs particularly strongly for:

```text
Obesity Type II
Obesity Type III
Insufficient Weight
```

The more difficult categories include:

```text
Overweight Level I
Overweight Level II
```

---

# 16. Explainability Analysis

Model explainability was performed using SHAP and model-based feature importance.

The strongest global raw features identified included:

```text
Weight
FCVC
Height
Gender
Age
```

Tree-based feature importance also highlighted:

```text
Weight
Gender
FCVC
Height
Age
```

These analyses provide descriptive information about model behavior and should not be interpreted as causal relationships.

---

# 17. BMI Ablation Study

BMI was evaluated as an additional engineered feature.

Two model configurations were compared:

```text
Original 16 Features
vs.
Original 16 Features + BMI
```

Results:

| Configuration | Validation Macro F1 |
|---|---:|
| Original 16 Features | **0.897776** |
| Original + BMI | 0.894614 |

Difference:

```text
-0.003162
```

Because BMI did not improve validation performance, the final model retained the original **16 features**.

This also avoids introducing a derived feature that is already strongly represented through height and weight.

---

# 18. Ordinal Error Analysis

Because obesity-risk categories have a natural severity order, prediction errors were also analyzed by category distance.

Results:

| Metric | Value |
|---|---:|
| Exact Classification | 0.907514 |
| Adjacent-Class Error | 0.078998 |
| Severe Error (distance ≥ 2) | 0.013488 |
| Mean Ordinal Distance | 0.109184 |

Most incorrect classifications occurred between neighboring categories.

---

# 19. Subgroup Evaluation

A descriptive gender subgroup analysis was performed.

| Gender | Support | Accuracy | Macro F1 |
|---|---:|---:|---:|
| Female | 1,573 | 0.910998 | 0.744944 |
| Male | 1,541 | 0.903958 | 0.763548 |

Macro F1 difference:

```text
0.018604
```

These results are descriptive only.

Because subgroup class support varies considerably, this analysis does **not** establish that the system is fair or unfair.

---

# 20. Saved Model

The final trained machine learning pipeline is stored at:

```text
models/obesity_risk_pipeline.joblib
```

Model metadata is stored at:

```text
models/model_metadata.json
```

The saved artifact contains both:

```text
Preprocessing Pipeline
        +
Gradient Boosting Classifier
```

This allows new raw observations to be passed directly into the saved pipeline without manually repeating preprocessing steps.

---

# 21. Model Metadata

Key metadata:

| Property | Value |
|---|---|
| Project | Obesity Risk Intelligence System |
| Selected Candidate | Tuned Gradient Boosting |
| Model Family | Gradient Boosting |
| Configuration | Tuned |
| Random State | 42 |
| Predictive Features | 16 |
| Transformed Features | 25 |
| Target Classes | 7 |
| Development Records | 17,644 |
| Test Records | 3,114 |
| Scikit-learn Version | 1.8.0 |

---

# 22. Flask REST API

The backend is implemented using Flask.

Current endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | API health status |
| GET | `/model-info` | Model metadata and performance |
| POST | `/predict` | Generate and save prediction |
| GET | `/predictions` | Retrieve prediction history |
| GET | `/predictions/<id>` | Retrieve a saved assessment |
| GET | `/predictions/<id>/report` | Generate assessment PDF |

---

# 23. Health Endpoint

Request:

```http
GET /health
```

Example response:

```json
{
    "status": "ok",
    "service": "obesity-risk-api"
}
```

---

# 24. Model Information Endpoint

Request:

```http
GET /model-info
```

The endpoint provides information including:

- Selected model
- Model family
- Configuration
- Number of predictive features
- Number of classes
- Target classes
- Scikit-learn version
- Final test metrics
- Model loading status

---

# 25. Prediction Endpoint

Request:

```http
POST /predict
```

Example payload:

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

Example response structure:

```json
{
    "prediction_id": 1,
    "predicted_class": "Normal_Weight",
    "confidence": 0.91,
    "probabilities": {
        "Insufficient_Weight": 0.01,
        "Normal_Weight": 0.91,
        "Overweight_Level_I": 0.05,
        "Overweight_Level_II": 0.02,
        "Obesity_Type_I": 0.005,
        "Obesity_Type_II": 0.003,
        "Obesity_Type_III": 0.002
    }
}
```

Actual values depend on the submitted assessment.

---

# 26. Input Validation

The backend validates all prediction requests before sending them to the machine learning model.

A request must contain exactly the required 16 predictive features.

Numerical application sanity ranges:

| Feature | Minimum | Maximum |
|---|---:|---:|
| Age | 1.0 | 120.0 |
| Height | 0.5 | 2.5 |
| Weight | 10.0 | 350.0 |
| FCVC | 1.0 | 3.0 |
| NCP | 1.0 | 4.0 |
| CH2O | 1.0 | 3.0 |
| FAF | 0.0 | 3.0 |
| TUE | 0.0 | 2.0 |

These are application sanity boundaries rather than medical thresholds.

The validator also checks:

- Missing features
- Unexpected features
- Numerical types
- Numerical ranges
- Valid categorical values

---

# 27. SQLite Prediction History

Prediction history is stored in:

```text
database/obesity_risk.db
```

This file is generated locally and intentionally ignored by Git.

The schema is defined in:

```text
database/schema.sql
```

The main table is:

```text
prediction_history
```

It contains 23 columns:

```text
id

age
height
weight
fcvc
ncp
ch2o
faf
tue

caec
calc
gender
family_history_with_overweight
favc
smoke
scc
mtrans

predicted_class
confidence
probabilities_json

model_name
scikit_learn_version

created_at
```

---

# 28. Prediction History API

Retrieve recent predictions:

```http
GET /predictions
```

Example structure:

```json
{
    "count": 2,
    "predictions": [
        {
            "id": 2,
            "predicted_class": "Normal_Weight",
            "confidence": 0.91,
            "model_name": "Tuned Gradient Boosting",
            "scikit_learn_version": "1.8.0",
            "created_at": "2026-08-10 18:30:00"
        }
    ]
}
```

Retrieve one complete assessment:

```http
GET /predictions/2
```

The response includes:

```text
Assessment ID
16 input values
Predicted class
Confidence
Seven probabilities
Model name
Scikit-learn version
Timestamp
```

---

# 29. PDF Assessment Reports

Every saved assessment can be converted into a downloadable PDF report.

Endpoint:

```http
GET /predictions/<id>/report
```

The report is generated dynamically using ReportLab.

Reports are generated **in memory** rather than permanently stored in the repository.

Each report contains:

- Project title
- Assessment ID
- Assessment timestamp
- Predicted obesity-risk category
- Prediction confidence
- Personal and physical information
- Eating-habit information
- Lifestyle and activity information
- Seven-class probability distribution
- Probability ranking
- Model information
- Scikit-learn version
- Educational/non-diagnostic disclaimer
- Page footer and page number

PDFs can be downloaded from:

```text
New Assessment Result
```

and:

```text
Prediction History
```

---

# 30. Streamlit Frontend

The frontend is implemented using Streamlit.

Current navigation:

```text
New Assessment
Prediction History
```

## New Assessment

Users can:

- Enter the 16 required values
- Submit an assessment
- Receive a predicted category
- View confidence
- View all seven probabilities
- View probability ranking
- Download a PDF report
- Start a new assessment

## Prediction History

Users can:

- View saved assessment count
- View recent assessments
- Select an assessment
- Reopen previous inputs
- View the original prediction
- View confidence and probabilities
- Download the assessment PDF again

---

# 31. Persistence

Streamlit session state is used only for temporary interface state.

Persistent prediction information is stored in SQLite.

Therefore:

```text
Restart Streamlit
        ↓
History remains
```

and:

```text
Restart Flask
        ↓
History remains
```

as long as the SQLite database is retained.

---

# 32. Error Handling

The backend implements centralized handling for:

```text
Validation errors
404 errors
405 errors
Internal server errors
```

Example validation response:

```json
{
    "error": "validation_error",
    "message": "..."
}
```

Missing prediction example:

```json
{
    "error": "prediction_not_found",
    "message": "Prediction record not found."
}
```

---

# 33. Project Structure

```text
Obesity-Risk-Intelligence-System/
│
├── backend/
│   ├── __init__.py
│   ├── database.py
│   ├── exceptions.py
│   ├── error_handlers.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── prediction_repository.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── history.py
│   │   ├── model_info.py
│   │   └── prediction.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── input_validator.py
│       ├── model_service.py
│       └── pdf_report_service.py
│
├── data/
│   └── raw/
│       └── .gitkeep
│
├── database/
│   ├── .gitkeep
│   └── schema.sql
│
│   # obesity_risk.db is generated locally
│   # and ignored by Git
│
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── assessment_form.py
│   │   ├── prediction_history.py
│   │   ├── prediction_result.py
│   │   └── report_download.py
│   │
│   └── services/
│       ├── __init__.py
│       └── api_client.py
│
├── models/
│   ├── model_metadata.json
│   └── obesity_risk_pipeline.joblib
│
├── notebooks/
│   └── ...
│
├── reports/
│   ├── figures/
│   └── generated/
│
├── src/
│   ├── __init__.py
│   └── preprocessing.py
│
├── tests/
│   ├── test_database.py
│   ├── test_frontend_api_client.py
│   ├── test_full_integration.py
│   ├── test_pdf_report_service.py
│   ├── test_prediction_api.py
│   ├── test_prediction_history_api.py
│   ├── test_prediction_history_ui.py
│   ├── test_prediction_report_api.py
│   ├── test_prediction_result.py
│   └── ...
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

Some experiment and analysis files may vary depending on the current repository state.

---

# 34. Installation

## 1. Clone the Repository

```powershell
git clone https://github.com/SMCodeX7/Obesity-Risk-Intelligence-System.git
```

Move into the project:

```powershell
cd Obesity-Risk-Intelligence-System
```

---

## 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
```

Then:

```powershell
python -m pip install -r requirements.txt
```

---

# 35. Main Dependencies

The project uses:

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
Flask==3.1.3
streamlit
requests
reportlab
```

---

# 36. Dataset Setup

Place the dataset at:

```text
data/raw/obesity.csv
```

The raw dataset is not stored in the GitHub repository.

---

# 37. Initialize SQLite

Before using prediction history for the first time, initialize the database.

Run:

```powershell
python -m flask --app backend init-db
```

Expected output:

```text
Database initialized: ...\database\obesity_risk.db
```

The command is safe to run again because the schema uses:

```sql
CREATE TABLE IF NOT EXISTS
```

---

# 38. Running the Application

The system requires two terminals.

## Terminal 1 — Flask Backend

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run Flask:

```powershell
python -m flask --app backend run --debug
```

Default backend URL:

```text
http://127.0.0.1:5000
```

---

## Terminal 2 — Streamlit Frontend

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run Streamlit:

```powershell
python -m streamlit run frontend/app.py
```

Streamlit will display the local application URL in the terminal.

Usually:

```text
http://localhost:8501
```

---

# 39. Testing the API Manually

## Health Check

```powershell
Invoke-RestMethod `
    -Uri http://127.0.0.1:5000/health `
    -Method Get
```

## Prediction History

```powershell
Invoke-RestMethod `
    -Uri http://127.0.0.1:5000/predictions `
    -Method Get |
    ConvertTo-Json -Depth 5
```

## Single Prediction

Example:

```powershell
Invoke-RestMethod `
    -Uri http://127.0.0.1:5000/predictions/1 `
    -Method Get |
    ConvertTo-Json -Depth 6
```

---

# 40. Automated Testing

Run all tests with:

```powershell
python -m pytest -q
```

The project contains tests for:

- Database initialization
- Database schema
- Input validation
- Prediction API
- Model loading
- Prediction persistence
- Prediction history
- History detail retrieval
- Frontend API client
- Frontend result helpers
- History UI helpers
- PDF generation
- PDF API endpoint
- Missing report handling
- Full prediction workflow
- Multiple prediction persistence

The complete test suite should finish with:

```text
0 failed
```

---

# 41. Full Integration Test

The full integration test verifies:

```text
Health API
    ↓
Model API
    ↓
Empty SQLite Database
    ↓
Prediction
    ↓
Database Save
    ↓
History Retrieval
    ↓
Assessment Detail
    ↓
PDF Generation
```

Run:

```powershell
python -m pytest tests/test_full_integration.py -q
```

---

# 42. Database Git Policy

The runtime SQLite database must not be committed.

Ignored patterns include:

```gitignore
database/*.db
database/*.db-shm
database/*.db-wal
database/*.sqlite
database/*.sqlite3
```

Tracked database files include:

```text
database/.gitkeep
database/schema.sql
```

Verify the runtime database is ignored:

```powershell
git check-ignore database/obesity_risk.db
```

Expected:

```text
database/obesity_risk.db
```

---

# 43. PDF Git Policy

PDFs downloaded manually during testing should not be added to the repository.

For example:

```text
assessment-3.pdf
```

is only a temporary locally downloaded report.

The application normally generates report bytes dynamically and sends them to the browser.

It does not require permanent PDF files inside the source repository.

---

# 44. Development Workflow

Typical development workflow:

```text
Modify Code
    ↓
Run Targeted Tests
    ↓
Run Full Test Suite
    ↓
Manual Application Test
    ↓
git status
    ↓
git add
    ↓
git commit
    ↓
git push
```

---

# 45. Current User Workflow

The implemented application flow is:

```text
1. Open Streamlit

2. Select New Assessment

3. Enter 16 required values

4. Submit assessment

5. Flask validates input

6. Saved ML pipeline generates prediction

7. Prediction is stored in SQLite

8. Frontend displays:
   - predicted class
   - confidence
   - seven probabilities

9. User may download PDF

10. User may open Prediction History

11. User may reopen any stored assessment

12. User may download its report again
```

---

# 46. Model Reproducibility

The project records important reproducibility information including:

```text
Random State: 42
Scikit-learn Version: 1.8.0
Selected Model: Tuned Gradient Boosting
Predictive Feature Count: 16
Target Class Count: 7
```

The model service checks the saved model metadata when loading the pipeline.

---

# 47. Important Design Decisions

## Raw Dataset Is Not Committed

The raw dataset is excluded from version control.

## Test Set Is Protected

The independent test set is not used for hyperparameter selection.

## Model and Preprocessing Are Saved Together

Using a Scikit-learn Pipeline reduces the risk of preprocessing inconsistencies between training and inference.

## BMI Was Not Added

BMI was tested experimentally but slightly reduced validation Macro F1.

## Predictions Are Persisted

Predictions are stored in SQLite rather than relying only on Streamlit session state.

## PDFs Are Generated On Demand

PDF reports are generated from stored prediction records instead of being permanently stored as database blobs.

## API and Frontend Are Separated

Streamlit communicates with Flask through an API client instead of directly loading the machine learning model.

---

# 48. Limitations

The project has several important limitations.

## Dataset Limitations

The model performance is dependent on the characteristics and quality of the training dataset.

## Not Clinical Software

The application has not been developed, validated, or certified as a medical diagnostic system.

## Prediction Confidence

Model probability should not be interpreted as clinical certainty.

## Subgroup Analysis

Current subgroup analysis is descriptive and does not establish fairness.

## Limited External Validation

Performance reported in this repository is based on the project's held-out test dataset.

External populations may behave differently.

## SQLite

SQLite is suitable for the current academic application but may not be appropriate for a high-concurrency production healthcare system.

## Authentication

The current academic version does not include a complete user authentication and authorization system.

---

# 49. Ethical Considerations

Obesity-related prediction involves sensitive health-associated information.

The project therefore avoids presenting outputs as medical diagnoses.

The interface and generated reports include non-diagnostic warnings.

The system should not be used to:

- Diagnose a medical condition
- Replace clinicians
- Make treatment decisions
- Discriminate against individuals
- Make employment or insurance decisions
- Make other high-impact decisions

---

# 50. Phase 10 Completion

Phase 10 introduced complete persistence and reporting integration.

Completed components include:

```text
SQLite database                       ✅
Database schema                       ✅
Database initialization command       ✅
Prediction persistence                ✅
Unique prediction IDs                 ✅
Prediction history API                ✅
Prediction detail API                 ✅
Streamlit history interface           ✅
Persistent history                    ✅
PDF generation service                ✅
PDF REST endpoint                     ✅
Current prediction PDF download       ✅
History PDF download                  ✅
Database tests                        ✅
History API tests                     ✅
PDF tests                             ✅
Frontend client tests                 ✅
Full integration tests                ✅
```

Phase 10 architecture:

```text
Streamlit
    ↓
Flask REST API
    ↓
Validation
    ↓
Machine Learning Pipeline
    ↓
Prediction
    ↓
SQLite
   /    \
  /      \
History   PDF Report
```

---

# 51. Phase 11 — Final Phase

The next and final development phase is:

```text
Phase 11
Final Product, Deployment and Documentation
```

Planned work includes:

## Final Frontend Redesign

The current frontend is functionally complete.

Phase 11 will focus on transforming it from a standard Streamlit-style interface into a more polished application experience.

Planned improvements include:

- Modern landing/dashboard layout
- Improved typography
- Better spacing and hierarchy
- Assessment cards
- Improved navigation
- Modern result presentation
- Better prediction cards
- Improved probability visualization
- Improved history presentation
- Better responsive behavior
- More professional visual identity

The assessment workflow may also be organized into more guided sections rather than displaying all information as one large form.

## Final Application Testing

- Full functional regression testing
- Browser testing
- Error-state testing
- PDF verification
- History verification
- UI testing
- Final cleanup

## Deployment

Planned deployment work includes:

- Backend deployment
- Streamlit deployment
- Environment configuration
- Production API URL configuration
- Deployment testing

## Final Documentation

Final documentation will include:

- Updated README
- Application screenshots
- Architecture documentation
- Setup instructions
- Deployment instructions
- Model methodology summary
- Evaluation results
- Limitations
- Final project demonstration material

---

# 52. Future Improvements

Potential future enhancements beyond the academic project include:

- User authentication
- User-specific prediction histories
- PostgreSQL migration
- Role-based access control
- Admin dashboard
- Analytics dashboard
- Batch CSV prediction
- Cloud object storage for generated reports
- Audit logging
- Docker support
- CI/CD
- Automated deployment
- Model monitoring
- Data-drift monitoring
- Model version tracking
- Additional subgroup evaluations
- External model validation
- More advanced explainability
- Personalized educational insights

---

# 53. Technologies Used

## Machine Learning

```text
Python
Scikit-learn
Pandas
NumPy
SHAP
Joblib
```

## Data Visualization

```text
Matplotlib
Seaborn
```

## Backend

```text
Flask
SQLite
```

## Frontend

```text
Streamlit
Requests
```

## Reporting

```text
ReportLab
```

## Testing

```text
Pytest
```

## Development

```text
VS Code
Jupyter
Git
GitHub
```

---

# 54. Repository

GitHub repository:

```text
https://github.com/SMCodeX7/Obesity-Risk-Intelligence-System
```

Default branch:

```text
main
```

---

# 55. License

This project is distributed under the **MIT License**.

See:

```text
LICENSE
```

for the full license text.

---

# 56. Disclaimer

The **Obesity Risk Intelligence System** is an educational machine learning project.

Its predictions:

- Are not medical diagnoses
- Are not clinical recommendations
- Do not guarantee an individual's health status
- Should not replace consultation with qualified healthcare professionals

The system is intended to demonstrate machine learning development, model evaluation, explainability, API integration, persistence, frontend development, automated testing, and reporting within an academic software project.

---

## Current Completion Summary

```text
Data Understanding                  ✅
EDA                                 ✅
Preprocessing                       ✅
Baseline Modeling                   ✅
Hyperparameter Tuning               ✅
Final Model Evaluation              ✅
Explainability                      ✅
BMI Ablation                        ✅
Ordinal Error Analysis              ✅
Subgroup Analysis                   ✅
Saved ML Pipeline                   ✅
Flask REST API                      ✅
Input Validation                    ✅
Streamlit Frontend                  ✅
SQLite Persistence                  ✅
Prediction History                  ✅
PDF Assessment Reports              ✅
Automated Tests                     ✅
Full Application Integration        ✅

Final UI Redesign                   ⏳
Deployment                          ⏳
Final Documentation                 ⏳
```

**Phase 10 is complete. Phase 11 is the final development phase.**