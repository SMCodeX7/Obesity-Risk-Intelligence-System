from sklearn.pipeline import (
    Pipeline,
)

from backend.services.model_service import (
    ModelService,
)


def test_model_service_loads_pipeline():
    service = ModelService()

    assert service.model is not None

    assert isinstance(
        service.model,
        Pipeline,
    )

    assert (
        service.metadata[
            "selected_candidate"
        ]
        == "Tuned Gradient Boosting"
    )

    assert (
        service.metadata[
            "predictive_feature_count"
        ]
        == 16
    )

    assert (
        service.metadata[
            "target_class_count"
        ]
        == 7
    )