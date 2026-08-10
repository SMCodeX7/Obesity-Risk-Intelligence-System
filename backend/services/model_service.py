from pathlib import Path
import json

import joblib
import sklearn


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)

DEFAULT_MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "obesity_risk_pipeline.joblib"
)

DEFAULT_METADATA_PATH = (
    PROJECT_ROOT
    / "models"
    / "model_metadata.json"
)


class ModelService:
    def __init__(
        self,
        model_path=DEFAULT_MODEL_PATH,
        metadata_path=DEFAULT_METADATA_PATH,
    ):
        self.model_path = Path(
            model_path
        )

        self.metadata_path = Path(
            metadata_path
        )

        self.model = None
        self.metadata = None

        self._load()

    def _load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found: "
                f"{self.model_path}"
            )

        if not self.metadata_path.exists():
            raise FileNotFoundError(
                f"Model metadata not found: "
                f"{self.metadata_path}"
            )

        with open(
            self.metadata_path,
            "r",
            encoding="utf-8",
        ) as file:
            self.metadata = json.load(
                file
            )

        saved_sklearn_version = (
            self.metadata.get(
                "scikit_learn_version"
            )
        )

        current_sklearn_version = (
            sklearn.__version__
        )

        if (
            saved_sklearn_version
            != current_sklearn_version
        ):
            raise RuntimeError(
                "scikit-learn version mismatch. "
                f"Current="
                f"{current_sklearn_version}, "
                f"Model="
                f"{saved_sklearn_version}"
            )

        self.model = joblib.load(
            self.model_path
        )

    def get_model_info(self):
        return {
            "project":
                self.metadata[
                    "project"
                ],

            "selected_model":
                self.metadata[
                    "selected_candidate"
                ],

            "model_family":
                self.metadata[
                    "model_family"
                ],

            "configuration":
                self.metadata[
                    "configuration"
                ],

            "predictive_feature_count":
                self.metadata[
                    "predictive_feature_count"
                ],

            "transformed_feature_count":
                self.metadata[
                    "transformed_feature_count"
                ],

            "target_class_count":
                self.metadata[
                    "target_class_count"
                ],

            "predictive_features":
                self.metadata[
                    "predictive_features"
                ],

            "target_classes":
                self.metadata[
                    "target_classes"
                ],

            "scikit_learn_version":
                self.metadata[
                    "scikit_learn_version"
                ],

            "final_test_metrics": {
                "accuracy":
                    self.metadata[
                        "final_test_accuracy"
                    ],

                "balanced_accuracy":
                    self.metadata[
                        "final_test_balanced_accuracy"
                    ],

                "macro_f1":
                    self.metadata[
                        "final_test_macro_f1"
                    ],

                "weighted_f1":
                    self.metadata[
                        "final_test_weighted_f1"
                    ],
            },

            "model_loaded":
                self.model is not None,
        }