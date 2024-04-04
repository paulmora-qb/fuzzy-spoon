from kedro.pipeline import Pipeline, node, pipeline

from pipelines.image_creation.functions import (
    apply_text_on_image,
    create_white_image,
    create_text_for_image,
    save_pasts_text,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
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
    )
