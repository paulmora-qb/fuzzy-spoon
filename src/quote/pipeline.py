"""Pipeline for quote image creation."""

from common.content_creation import create_content_pipeline
from common.insta_publish import create_insta_publish_pipeline
from kedro.pipeline import Pipeline


def create_pipeline(namespace: str, variants: list[str] = None) -> Pipeline:
    """Pipeline for quotes with author information.

    Args:
        namespace (str): Namespace for the pipeline.
        variants (list[str]): Variants of the pipeline.

    Returns:
        Pipeline: Pipeline for quotes with author information.
    """
    namespaces = [f"{namespace}.{variant}" for variant in variants]
    return sum(
        [
            create_content_pipeline(namespace=namespace)
            + create_insta_publish_pipeline(namespace=namespace)
            for namespace in namespaces
        ]
    )
