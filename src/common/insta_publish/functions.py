"""Functions for the insta_publish pipeline."""

import os

from instagrapi import Client
from kedro.config import OmegaConfigLoader
from PIL import Image
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging

logger = logging.getLogger()


def post_image(namespace: str, image: Image, hashtags: list[str]) -> None:
    """Post an image to Instagram.

    This function posts an image to instagram using the instagrapi library. Before
    posting the image, the function logs into the Instagram account using the
    provided username and password. The image is then uploaded to the account.

    Args:
    ----
        namespace (str): The namespace for the pipeline.
        image (Image): The image to be posted.
        hashtags (list[str]): The hashtags to be included in the Instagram post.

    """
    top_level_namespace, variant = namespace.split(".")
    conf_loader = OmegaConfigLoader(conf_source="./conf")
    insta_params = conf_loader["credentials"][top_level_namespace][variant]

    # Extract the Instagram credentials.
    username = insta_params["username"]
    password = insta_params["password"]

    # Login to the Instagram account.
    cl = Client()
    cl.login(username, password)

    # Delete the temporary image file if it exists.
    temp_image_path = "temp_image.png"
    if os.path.exists(temp_image_path):
        try:
            os.remove(temp_image_path)
        except Exception as e:
            raise NewException("An error occurred") from err

    # Save the image to a temporary file and upload it to Instagram.
    image.save(temp_image_path)
    cl.photo_upload(path=temp_image_path, caption=" ".join(hashtags))
    os.remove(temp_image_path)
