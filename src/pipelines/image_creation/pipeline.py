from kedro.pipeline import Pipeline, node, pipeline

from pipelines.image_creation.functions import apply_text_on_image, create_white_image
from libs.prompt_engineering.functions import prompt_wrapper


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
                func=prompt_wrapper,
                inputs={
                    "system_message": "params:system_message",
                    "instruction_message": "params:instruction_message",
                    "pydantic_object_path": "params:pydantic_object_path",
                },
                outputs="text_for_image",
                name="create_text_for_image",
            ),
            node(
                func=apply_text_on_image,
                inputs={
                    "image": "white_canvas",
                    "text": "text_for_image",
                    "params": "params:final_image",
                },
                outputs="final_image",
                name="create_final_image",
            ),
        ]
    )
