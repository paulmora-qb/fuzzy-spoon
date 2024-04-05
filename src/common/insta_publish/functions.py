"""Functions for the insta_publish pipeline."""

from PIL import Image
from instagrapi import Client
import os


def post_image(image: Image, hashtags: list[str]) -> None:
    """This function posts an image to Instagram.

    This function posts an image to instagram using the instagrapi library. Before
    posting the image, the function logs into the Instagram account using the
    provided username and password. The image is then uploaded to the account.

    Args:
        image (Image): The image to be posted.
        hashtags (list[str]): The hashtags to be included in the Instagram post.
    """
    # Extract the Instagram credentials.
    username = os.environ.get("INSTA_USERNAME")
    password = os.environ.get("INSTA_PASSWORD")

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
    cl.photo_upload(path=temp_image_path, caption=" ".join(hashtags))
    os.remove(temp_image_path)
