"""Project pipelines."""

from typing import Dict

from pipelines.image_creation.pipeline import (
    create_pipeline as image_create_pipeline,
)
from pipelines.insta_publish.pipeline import (
    create_pipeline as insta_create_pipeline,
)
from kedro.pipeline import Pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    return {
        "image_creation": image_create_pipeline(),
        "insta_publish": insta_create_pipeline(),
        "__default__": image_create_pipeline() + insta_create_pipeline(),
    }
