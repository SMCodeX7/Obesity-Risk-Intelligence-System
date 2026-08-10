CREATE TABLE IF NOT EXISTS prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    age REAL NOT NULL,
    height REAL NOT NULL,
    weight REAL NOT NULL,

    fcvc REAL NOT NULL,
    ncp REAL NOT NULL,
    ch2o REAL NOT NULL,
    faf REAL NOT NULL,
    tue REAL NOT NULL,

    caec TEXT NOT NULL,
    calc TEXT NOT NULL,
    gender TEXT NOT NULL,
    family_history_with_overweight TEXT NOT NULL,
    favc TEXT NOT NULL,
    smoke TEXT NOT NULL,
    scc TEXT NOT NULL,
    mtrans TEXT NOT NULL,

    predicted_class TEXT NOT NULL,

    confidence REAL NOT NULL
        CHECK (
            confidence >= 0.0
            AND confidence <= 1.0
        ),

    probabilities_json TEXT NOT NULL,

    model_name TEXT NOT NULL,
    scikit_learn_version TEXT NOT NULL,

    created_at TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS
idx_prediction_history_created_at
ON prediction_history(created_at);