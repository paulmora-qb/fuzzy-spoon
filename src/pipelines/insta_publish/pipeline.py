"""Kedro pipelines for the insta_publish package."""

from kedro.pipeline import Pipeline, node, pipeline

from .functions import post_image, create_hashtags


def create_pipeline(namespace: str) -> Pipeline:
    nodes = [
        node(
            func=create_hashtags,
            inputs={
                "text_on_image": "text_for_image",
                "system_message": "params:hashtag_system_message",
                "instruction_message": "params:hashtag_instruction_message",
                "pydantic_object_path": "params:hashtag_pydantic_object_path",
            },
            outputs="hashtags",
            name="create_hashtags",
        ),
        node(
            func=post_image,
            inputs={"image": "final_image", "hashtags": "hashtags"},
            outputs=None,
            name="post_image",
        ),
    ]
    return pipeline(pipe=Pipeline(nodes), namespace=namespace)
