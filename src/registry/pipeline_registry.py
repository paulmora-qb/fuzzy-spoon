"""Project pipelines."""

from quotes import (
    create_pipeline as create_quotes_pipeline,
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
    return {"quote_pipeline": create_quotes_pipeline()}
