"""Kedro pipelines for the insta_publish package."""

from kedro.pipeline import Pipeline, node, pipeline

from common.insta_publish.functions import post_image


def create_insta_publish_pipeline(namespace: str = None) -> Pipeline:
    nodes = [
        node(
            func=post_image,
            inputs={"image": "final_image", "hashtags": "hashtags"},
            outputs=None,
            name="post_image",
        ),
    ]
    return pipeline(pipe=Pipeline(nodes), namespace=namespace)
