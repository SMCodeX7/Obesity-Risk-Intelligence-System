# Obesity Risk Intelligence System

A machine learning-based obesity risk classification system designed to predict an individual's obesity category from demographic, lifestyle, eating-behaviour, and physical-activity information.

The project follows a structured machine learning workflow covering data understanding, exploratory data analysis, preprocessing, baseline modelling, hyperparameter tuning, final model evaluation, explainability, feature ablation, ordinal error analysis, and subgroup performance analysis.

The machine learning research and evaluation stages through **Phase 7 are complete**.

---

## Project Overview

Obesity is influenced by several interacting factors including physical characteristics, eating habits, activity level, family history, and lifestyle behaviours.

This project develops a multiclass machine learning model capable of classifying individuals into one of seven obesity-risk categories.

The system is designed with two goals:

1. Build a reliable multiclass obesity-risk classifier.
2. Make the model interpretable using feature importance and SHAP explanations.

The final application will later expose the trained model through a Flask REST API and a Streamlit user interface.

---

## Current Project Status

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Data Understanding | ✅ Complete |
| Phase 2 | Exploratory Data Analysis | ✅ Complete |
| Phase 3 | Preprocessing Pipeline | ✅ Complete |
| Phase 4 | Baseline Model Development | ✅ Complete |
| Phase 5 | Hyperparameter Tuning | ✅ Complete |
| Phase 6 | Final Model Selection and Evaluation | ✅ Complete |
| Phase 7 | Explainability and Advanced Evaluation | ✅ Complete |
| Phase 8 | Flask REST API | ⏳ Next |
| Phase 9 | Streamlit Frontend | ⬜ Planned |
| Phase 10 | SQLite and Full Integration | ⬜ Planned |
| Phase 11 | Deployment and Final Documentation | ⬜ Planned |

---

# Dataset

The project uses the generated obesity-risk dataset from the Kaggle Playground Series Season 4 Episode 2 competition.

The local dataset is expected at:

```text
data/raw/obesity.csv
```

Raw data is intentionally not committed to the repository.

### Dataset size

```text
20,758 records
18 columns
```

The dataset contains:

- 16 predictive features
- 1 identifier column
- 1 target column

The identifier column is excluded from modelling.

---

## Target Variable

The target variable is:

```text
NObeyesdad
```

It contains seven classes:

1. `Insufficient_Weight`
2. `Normal_Weight`
3. `Overweight_Level_I`
4. `Overweight_Level_II`
5. `Obesity_Type_I`
6. `Obesity_Type_II`
7. `Obesity_Type_III`

This makes the problem a **7-class multiclass classification problem**.

---

# Predictive Features

The model uses 16 original input features.

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

### Meaning

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

## Ordinal Categorical Features

```text
CAEC
CALC
```

### CAEC — Food consumption between meals

Ordered as:

```text
no
Sometimes
Frequently
Always
```

### CALC — Alcohol consumption

Ordered as:

```text
no
Sometimes
Frequently
```

---

## Nominal Categorical Features

```text
Gender
family_history_with_overweight
FAVC
SMOKE
SCC
MTRANS
```

These features do not have a meaningful numerical order and are therefore encoded using one-hot encoding.

---

# Project Structure

```text
Obesity-Risk-Intelligence-System/
│
├── backend/
│   └── .gitkeep
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
│   └── test_preprocessing.py
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

The `backend`, `frontend`, and `database` directories are reserved for the application-development phases.

---

# Phase 1 — Data Understanding

Phase 1 focused on understanding the structure and quality of the dataset.

The analysis included:

- Dataset dimensions
- Column types
- Target classes
- Missing-value analysis
- Duplicate detection
- Numerical-variable inspection
- Categorical-variable inspection
- Class distribution analysis

The dataset contains no missing records requiring major correction and is suitable for supervised multiclass classification.

Notebook:

```text
notebooks/01_data_understanding.ipynb
```

---

# Phase 2 — Exploratory Data Analysis

Exploratory Data Analysis investigated the relationships between input variables and obesity classes.

The analysis included:

- Target-class distribution
- Numerical feature distributions
- Categorical feature distributions
- Weight and height patterns
- Age patterns
- Eating behaviour
- Physical activity
- Transportation behaviour
- Correlation analysis
- Class-level comparisons

Notebook:

```text
notebooks/02_eda.ipynb
```

---

# Phase 3 — Preprocessing

A reusable preprocessing pipeline was developed in:

```text
src/preprocessing.py
```

The preprocessing pipeline uses Scikit-learn's:

```text
ColumnTransformer
```

to process numerical, ordinal, and nominal features separately.

---

## Numerical Pipeline

Numerical features use:

```text
SimpleImputer(strategy="median")
StandardScaler()
```

This provides protection against missing numerical values and standardizes the numerical variables.

---

## Ordinal Pipeline

Ordinal features use:

```text
SimpleImputer(strategy="most_frequent")
OrdinalEncoder()
```

Unknown categories are encoded using:

```text
unknown_value = -1
```

This allows the preprocessing pipeline to safely handle previously unseen ordinal values.

---

## Nominal Pipeline

Nominal variables use:

```text
SimpleImputer(strategy="most_frequent")
OneHotEncoder(handle_unknown="ignore")
```

This prevents prediction failures when an unseen nominal category is provided.

---

## Feature Transformation

The original model receives:

```text
16 raw predictive features
```

After preprocessing:

```text
25 transformed features
```

are passed to the classifier.

---

# Preprocessing Tests

Automated tests are available in:

```text
tests/test_preprocessing.py
```

Tests verify:

- Feature-group configuration
- Creation of independent preprocessing objects
- Successful transformation
- Missing-value handling
- Unknown-category handling

Run the tests using:

```bash
pytest
```

or:

```bash
python -m pytest
```

---

# Phase 4 — Baseline Models

Several classification algorithms were evaluated as baseline models.

Models included:

- Dummy Classifier
- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

### Validation performance

| Model | Accuracy | Macro F1 |
|---|---:|---:|
| Gradient Boosting | 0.9033 | 0.8930 |
| Random Forest | 0.8956 | 0.8849 |
| Logistic Regression | 0.8581 | 0.8418 |
| Decision Tree | 0.8452 | 0.8308 |
| Dummy Classifier | 0.1949 | 0.0466 |

Gradient Boosting achieved the strongest validation performance.

Random Forest also performed well but showed a larger training-validation performance gap.

Notebook:

```text
notebooks/04_baseline_models.ipynb
```

---

# Phase 5 — Hyperparameter Tuning

The two strongest baseline candidates were selected for tuning:

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

The main optimization metric was:

```text
Macro F1
```

Macro F1 was selected because all seven obesity classes should contribute equally to model evaluation.

---

## Tuned Model Comparison

| Model | Validation Accuracy | Validation Macro F1 |
|---|---:|---:|
| Tuned Gradient Boosting | 0.9075 | 0.8978 |
| Tuned Random Forest | 0.9059 | 0.8967 |
| Baseline Gradient Boosting | 0.9033 | 0.8930 |
| Baseline Random Forest | 0.8956 | 0.8849 |

The final selected candidate was:

```text
Tuned Gradient Boosting
```

Notebook:

```text
notebooks/05_model_tuning.ipynb
```

---

# Final Gradient Boosting Configuration

The selected Gradient Boosting classifier uses:

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

After model selection, the final pipeline was refitted using the development dataset and evaluated on the reserved test set.

The persisted pipeline contains both:

```text
Preprocessing
+
Gradient Boosting classifier
```

This means application code can send the original 16 input features directly to the pipeline.

---

## Final Test Performance

| Metric | Score |
|---|---:|
| Accuracy | **0.9075** |
| Balanced Accuracy | **0.8976** |
| Macro F1 | **0.8973** |
| Weighted F1 | **0.9072** |

The model therefore correctly classifies approximately:

```text
90.75%
```

of the final test records.

---

## Final Model Artifact

The trained pipeline is stored at:

```text
models/obesity_risk_pipeline.joblib
```

Model metadata is stored at:

```text
models/model_metadata.json
```

The metadata records:

- Selected model
- Feature configuration
- Target classes
- Development sample count
- Test sample count
- Validation performance
- Final test performance
- Scikit-learn version

The persisted model was created using:

```text
scikit-learn 1.8.0
```

The runtime environment should therefore use the same version.

---

# Phase 7 — Explainability and Advanced Evaluation

Phase 7 investigates how the frozen final model makes its predictions and how its errors behave.

Notebook:

```text
notebooks/06_explainability.ipynb
```

Phase 7 includes:

- Final-model verification
- Global tree feature importance
- Global SHAP analysis
- Local SHAP explanations
- Ordinal error analysis
- BMI feature ablation
- Gender subgroup performance analysis

---

# Global Feature Importance

Gradient Boosting's built-in feature importance was compared with SHAP-based feature importance.

## Top Tree-Based Features

```text
1. Weight
2. Gender
3. FCVC
4. Height
5. Age
```

## Top SHAP Features

```text
1. Weight
2. FCVC
3. Height
4. Gender
5. Age
```

Both approaches identify a similar group of highly influential variables.

In particular:

```text
Weight
Height
FCVC
Gender
Age
```

play major roles in model predictions.

---

# SHAP Explainability

SHAP was used to analyse the contribution of individual features to model predictions.

Two forms of explainability were performed.

## Global SHAP

Global SHAP analysis determines which features have the greatest influence across a sample of test predictions.

Generated output:

```text
reports/figures/global_shap_feature_importance.png
```

---

## Local SHAP

Local SHAP explanations were generated for:

```text
3 correctly classified examples
3 incorrectly classified examples
```

For each prediction, the five strongest feature contributions were recorded.

Generated local explanation figures are stored in:

```text
reports/figures/local_shap_*.png
```

The corresponding table is stored in:

```text
reports/generated/local_shap_explanations.csv
```

---

# Ordinal Error Analysis

The target classes represent an approximate increasing obesity-severity order:

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

Incorrect predictions were therefore analysed based on the distance between the true and predicted class.

### Results

```text
Mean ordinal distance: 0.1092
Exact prediction rate: 90.75%
Adjacent-class error rate: 7.90%
Severe error rate: 1.35%
```

A severe error is defined as a prediction at least two class levels away from the true class.

This shows that most errors occur between neighbouring obesity categories rather than distant categories.

---

# BMI Feature Ablation

BMI was calculated as:

```text
BMI = Weight / Height²
```

A controlled experiment compared:

```text
Original 16 Features
```

against:

```text
Original 16 Features + BMI
```

The experiment used the training and validation sets only.

### Results

| Configuration | Validation Macro F1 |
|---|---:|
| Original 16 features | **0.8978** |
| Original + BMI | **0.8946** |

Macro F1 change:

```text
-0.00316
```

Explicitly adding BMI therefore did not improve validation performance.

The original 16-feature model was retained.

---

# Subgroup Performance Analysis

The frozen final model was also evaluated across gender subgroups.

The observed Macro F1 difference between gender groups was approximately:

```text
0.0186
```

These results should be interpreted carefully.

The distribution of obesity classes differs considerably between gender subgroups in the dataset. Therefore, subgroup metrics are treated as descriptive diagnostic information rather than definitive evidence that the model is either fair or unfair.

Further fairness analysis would require more balanced and representative subgroup data.

---

# Phase 7 Summary

The Phase 7 summary is stored at:

```text
reports/generated/phase7_summary.json
```

Current summary:

```text
Selected model:
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

BMI Macro F1 Change:
-0.00316

Gender Macro F1 Gap:
0.0186
```

---

# Generated Reports

Model-development and evaluation reports are stored in:

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

Explainability figures are stored in:

```text
reports/figures/
```

Examples include:

```text
global_tree_feature_importance.png
global_shap_feature_importance.png

local_shap_<sample_id>.png

gender_subgroup_macro_f1.png
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/SMCodeX7/Obesity-Risk-Intelligence-System.git
```

Move into the project:

```bash
cd Obesity-Risk-Intelligence-System
```

---

## 2. Create a virtual environment

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

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
```

Then:

```bash
python -m pip install -r requirements.txt
```

The persisted model requires:

```text
scikit-learn==1.8.0
```

---

## 4. Add the Dataset

Create:

```text
data/raw/
```

and place the dataset at:

```text
data/raw/obesity.csv
```

---

# Run the Notebooks

Start Jupyter:

```bash
jupyter lab
```

The notebooks should be studied in the following order:

```text
1. notebooks/01_data_understanding.ipynb
2. notebooks/02_eda.ipynb
3. notebooks/03_preprocessing.ipynb
4. notebooks/04_baseline_models.ipynb
5. notebooks/05_model_tuning.ipynb
6. notebooks/06_explainability.ipynb
```

---

# Run Tests

From the project root:

```bash
python -m pytest
```

---

# Machine Learning Architecture

The current machine learning workflow is:

```text
Raw User Features
        │
        ▼
Scikit-learn Pipeline
        │
        ├── Numerical Processing
        │      ├── Median Imputation
        │      └── Standard Scaling
        │
        ├── Ordinal Processing
        │      ├── Most-Frequent Imputation
        │      └── Ordinal Encoding
        │
        ├── Nominal Processing
        │      ├── Most-Frequent Imputation
        │      └── One-Hot Encoding
        │
        ▼
25 Transformed Features
        │
        ▼
Tuned Gradient Boosting Classifier
        │
        ▼
Obesity Risk Class
```

---

# Planned Application Architecture

The next stages will convert the trained model into a complete application.

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
 ├── Saved ML Pipeline
 │       ├── Preprocessing
 │       └── Gradient Boosting
 │
 ├── Prediction
 ├── Confidence
 ├── Class Probabilities
 └── Explanation
 │
 ▼
SQLite Prediction History
```

---

# Next Phase

The next development stage is:

## Phase 8 — Flask REST API

Planned API functionality includes:

```text
GET /health
GET /model-info
POST /predict
```

The API will:

- Load the trained model once when the server starts
- Validate incoming user data
- Convert JSON into the expected feature structure
- Run the saved Scikit-learn pipeline
- Return the predicted obesity-risk class
- Return prediction confidence
- Return class probabilities
- Handle invalid requests safely
- Include automated API tests

---

# Key Technical Decisions

Several practices were used to improve the reliability of the project:

- The identifier column is excluded from training.
- Preprocessing is performed inside a reusable Scikit-learn pipeline.
- Unknown categorical values are handled safely.
- Stratified dataset splitting preserves target-class proportions.
- Model selection is based on development/validation data.
- Macro F1 is used as an important multiclass evaluation metric.
- Hyperparameter tuning uses stratified cross-validation.
- The final preprocessing pipeline and classifier are persisted together.
- SHAP is used alongside tree-based feature importance.
- BMI ablation is evaluated using training/validation data rather than changing the frozen final model.
- Subgroup metrics are interpreted cautiously because class distributions differ across groups.

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

## Data Visualization

```text
Matplotlib
Seaborn
```

## Development and Testing

```text
JupyterLab
Pytest
Git
GitHub
```

## Planned Application Stack

```text
Flask
Streamlit
SQLite
```

---

# Limitations

The current project has several limitations.

### Dataset Representation

The model's performance depends on the characteristics of the available dataset and may not generalize equally well to every real-world population.

### Generated Dataset

The dataset includes generated/synthetic characteristics and therefore should not automatically be treated as representative clinical population data.

### Medical Use

This system is a machine learning and educational project.

It is **not a medical diagnostic system** and should not replace professional medical evaluation.

### Subgroup Analysis

Some obesity classes are highly unevenly distributed across gender groups. Subgroup metrics therefore require careful interpretation.

### Explainability

SHAP explains how the model produced predictions but does not prove that a feature causes obesity.

Feature importance represents predictive influence, not medical causation.

---

# Reproducibility

The project uses:

```text
random_state = 42
```

for reproducible data splitting and model-development procedures where applicable.

The final saved model records:

```text
scikit-learn version = 1.8.0
```

Using the same Scikit-learn version is recommended when loading the persisted model.

---

# License

This project is licensed under the MIT License.

See:

```text
LICENSE
```

for details.

---

# Project Progress

```text
Data Understanding       ██████████ 100%
EDA                      ██████████ 100%
Preprocessing            ██████████ 100%
Baseline Modelling       ██████████ 100%
Model Tuning             ██████████ 100%
Final Model Evaluation   ██████████ 100%
Explainability           ██████████ 100%
Flask API                ░░░░░░░░░░   0%
Streamlit UI             ░░░░░░░░░░   0%
Database Integration     ░░░░░░░░░░   0%
Deployment               ░░░░░░░░░░   0%
```

---

## Current Milestone

**Phases 1–7 complete.**

The machine learning research, training, evaluation, and explainability components are ready.

The next milestone is building the production-style Flask REST API around the persisted machine learning pipeline.