"""Pipeline for quotes with author information."""

from kedro.pipeline import Pipeline, node, pipeline

from pipelines.image_creation.functions import (
    apply_text_on_image,
    create_white_image,
    create_text_for_image,
    save_pasts_text,
)
from pipelines.insta_publish import create_pipeline as create_insta_publish_pipeline


def create_image_creation_pipeline(namespace: str) -> Pipeline:
    nodes = [
        node(
            func=create_white_image,
            inputs="params:canvas_settings",
            outputs="white_canvas",
            name="create_white_canvas",
        ),
        node(
            func=create_text_for_image,
            inputs={
                "system_message": "params:system_message",
                "instruction_message": "params:instruction_message",
                "pydantic_object_path": "params:pydantic_object_path",
                "past_texts": "past_texts",
            },
            outputs="text_for_image",
            name="create_text_for_image",
        ),
        node(
            func=save_pasts_text,
            inputs={
                "text": "text_for_image",
                "past_texts": "past_texts",
            },
            outputs="adjusted_past_texts",
            name="save_past_texts",
        ),
        node(
            func=apply_text_on_image,
            inputs={
                "image": "white_canvas",
                "text": "text_for_image",
                "quote_font": "quote_font",
                "author_font": "author_font",
                "params": "params:final_image",
            },
            outputs="final_image",
            name="create_final_image",
        ),
    ]
    return pipeline(pipe=Pipeline(nodes), namespace=namespace)


def create_pipeline(variants: list[str]) -> Pipeline:
    """Pipeline for quotes with author information.

    Args:
        variants (list[str]): Variants of the pipeline.

    Returns:
        Pipeline: Pipeline for quotes with author information.
    """
    return sum(
        create_image_creation_pipeline(namespace=namespace)
        + create_insta_publish_pipeline(namespace=namespace)
        for namespace in variants
    )
