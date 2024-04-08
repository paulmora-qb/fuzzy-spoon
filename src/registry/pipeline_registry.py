"""Project pipelines."""

from quote import create_pipeline as create_quote_pipeline
from fact import create_pipeline as create_fact_pipeline

from kedro.pipeline import Pipeline

DYNAMIC_PIPELINES_MAPPING = {
    "quote": ["inspirational", "breakup", "love", "life"],
    "fact": ["animals", "countries", "history", "science"],
}


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    return {
        "quote_pipeline": create_quote_pipeline(
            namespace="quote", variants=DYNAMIC_PIPELINES_MAPPING["quote"]
        ),
        "fact_pipeline": create_fact_pipeline(
            namespace="fact", variants=DYNAMIC_PIPELINES_MAPPING["fact"]
        ),
    }
