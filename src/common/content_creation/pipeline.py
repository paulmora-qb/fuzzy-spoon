"""Pipeline for general content information."""

from kedro.pipeline import Pipeline, node, pipeline

from common.content_creation.functions import (
    apply_text_on_image,
    create_white_image,
    create_text_for_image,
    save_pasts_text,
    create_hashtags,
    create_text_dictionary,
)
from functools import partial


def create_text_object_pipeline(namespace: str = None, inputs: str = None) -> Pipeline:
    nodes = [
        node(
            func=partial(create_text_for_image, output_parser_key=namespace),
            inputs={
                "system_message": "params:system_message",
                "instruction_message": "params:instruction_message",
                "past_texts": "past_texts",
            },
            outputs="text_for_image",
            name="create_text_for_image",
        ),
        node(
            func=create_text_dictionary,
            inputs={
                "text_for_image": "text_for_image",
                "font": "font",
            },
            outputs="text_dictionary",
            name="create_text_dictionary",
        ),
        node(
            func=partial(save_pasts_text, namespace=namespace),
            inputs={
                "text_dictionary": "text_dictionary",
                "past_texts": "past_texts",
            },
            outputs="adjusted_past_texts",
            name="save_pasts_text",
        ),
    ]
    return pipeline(pipe=Pipeline(nodes), namespace=namespace, inputs=inputs)


def create_image_creation_pipeline(
    inputs: str = None, namespace: str = None
) -> Pipeline:
    nodes = [
        node(
            func=create_white_image,
            inputs="params:canvas_settings",
            outputs="white_canvas",
            name="create_white_canvas",
        ),
        node(
            func=apply_text_on_image,
            inputs={
                "image": "white_canvas",
                "text_dictionary": "text_dictionary",
                "params": "params:final_image",
            },
            outputs="final_image",
            name="create_final_image",
        ),
    ]
    return pipeline(pipe=Pipeline(nodes), namespace=namespace, inputs=inputs)


def create_hashtags_pipeline(inputs: str = None, namespace: str = None) -> Pipeline:
    nodes = [
        node(
            func=partial(create_hashtags, output_parser_key="hashtag"),
            inputs={
                "text_dictionary": "text_dictionary",
                "system_message": "params:hashtag_system_message",
                "instruction_message": "params:hashtag_instruction_message",
            },
            outputs="hashtags",
            name="create_hashtags",
        ),
    ]
    return pipeline(pipe=Pipeline(nodes), namespace=namespace, inputs=inputs)


def create_content_pipeline(inputs: str = None, namespace: str = None) -> Pipeline:
    return (
        create_text_object_pipeline(namespace=namespace, inputs={"past_texts", "font"})
        + create_image_creation_pipeline(namespace=namespace)
        + create_hashtags_pipeline(namespace=namespace)
    )
