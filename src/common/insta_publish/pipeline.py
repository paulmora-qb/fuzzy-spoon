"""Kedro pipelines for the insta_publish package."""

from functools import partial

from common.insta_publish.functions import post_image
from kedro.pipeline import Pipeline, node, pipeline


def create_insta_publish_pipeline(
    namespace: str = None, publish: bool = True
) -> Pipeline:
    """Create a pipeline for publishing images to Instagram."""
    nodes = (
        [
            node(
                func=partial(post_image, namespace=namespace),
                inputs={"image": "final_image", "hashtags": "hashtags"},
                outputs=None,
                name="post_image",
            ),
        ]
        if publish
        else []
    )
    return pipeline(pipe=Pipeline(nodes), namespace=namespace)
