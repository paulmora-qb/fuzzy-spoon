"""Kedro pipelines for the insta_publish package."""

from kedro.pipeline import Pipeline, node, pipeline

from .functions import post_image


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=post_image,
                inputs={"image": "final_image"},
                outputs=None,
                name="post_image",
            ),
        ]
    )
