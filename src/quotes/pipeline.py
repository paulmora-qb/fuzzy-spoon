"""Pipeline for quote image creation."""

from kedro.pipeline import Pipeline, node, pipeline

from common.content_creation import create_content_pipeline
from common.insta_publish import create_insta_publish_pipeline
from quotes.functions import create_text_dictionary


def create_text_dictionary_pipeline(
    namespace: str = None, inputs: str = None
) -> Pipeline:
    nodes = [
        node(
            func=create_text_dictionary,
            inputs={
                "text_for_image": "text_for_image",
                "quote_font": "quote_font",
                "author_font": "author_font",
            },
            outputs="text_dictionary",
            name="create_text_dictionary",
        )
    ]
    return pipeline(pipe=Pipeline(nodes), namespace=namespace, inputs=inputs)


def create_pipeline(variants: list[str] = None) -> Pipeline:
    """Pipeline for quotes with author information.

    Args:
        variants (list[str]): Variants of the pipeline.

    Returns:
        Pipeline: Pipeline for quotes with author information.
    """
    namespace = "quotes"
    return (
        create_text_dictionary_pipeline(
            namespace=namespace, inputs={"quote_font", "author_font"}
        )
        + create_content_pipeline(namespace=namespace)
        + create_insta_publish_pipeline(namespace=namespace)
    )