"""Functions for the insta_publish pipeline."""

from PIL import Image
from instagrapi import Client
import os
from kedro.config import OmegaConfigLoader


def post_image(image: Image) -> None:
    """This function posts an image to Instagram.

    This function posts an image to instagram using the instagrapi library. Before
    posting the image, the function logs into the Instagram account using the
    provided username and password. The image is then uploaded to the account.

    Args:
        image (Image): The image to be posted.
    """
    # Load the Instagram credentials.
    conf_loader = OmegaConfigLoader(conf_source="./conf")
    insta_params = conf_loader["credentials"]["insta_login_params"]

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
            print(f"The file at '{temp_image_path}' has been successfully deleted.")
        except Exception as e:
            print(f"Error deleting the file: {e}")

    # Save the image to a temporary file and upload it to Instagram.
    image.save(temp_image_path)
    cl.photo_upload(path=temp_image_path, caption=".")
    os.remove(temp_image_path)
