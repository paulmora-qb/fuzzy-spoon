"""Project pipelines."""

from pipelines.image_creation.pipeline import (
    create_pipeline as image_create_pipeline,
)
from kedro.pipeline import Pipeline

DYNAMIC_PIPELINES_MAPPING = {
    "image_on_text": ["quotes", "quiz"],
}


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    return {
        "image_creation": image_create_pipeline(
            variants=DYNAMIC_PIPELINES_MAPPING["image_on_text"]
        )
    }
