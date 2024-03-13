from kedro.pipeline import Pipeline, node, pipeline

from .functions import apply_text_on_image, create_white_image
from .llms.functions import obtain_text


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
                func=obtain_text,
                inputs={
                    "text_params": "params:text_settings",
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
