"""Functions for the insta_publish pipeline."""

from PIL import Image
from instagrapi import Client
import os
from kedro.config import OmegaConfigLoader
from libs.prompt_engineering.functions import prompt_wrapper


def create_hashtags(
    text_on_image: str,
    system_message: str,
    instruction_message: str,
    pydantic_object_path: str,
) -> list[str]:
    """This function creates hashtags for an Instagram post.

    Args:
        text_on_image (str): The text that will be placed on the image.
        system_message (str): System message which tells AI how to behave.
        instruction_message (str): Instruction message which tells AI what to do.
        pydantic_object_path (str): Path of where the pydantic object is stored. This
            object states what attributes the output class should have.

    Returns:
        list[str]: The hashtags to be included in the Instagram post.
    """
    adjusted_instruction_message = instruction_message.format(
        text=text_on_image, format_instructions="{format_instructions}"
    )

    return prompt_wrapper(
        system_message=system_message,
        instruction_message=adjusted_instruction_message,
        pydantic_object_path=pydantic_object_path,
    ).hashtag


def post_image(image: Image, hashtags: list[str]) -> None:
    """This function posts an image to Instagram.

    This function posts an image to instagram using the instagrapi library. Before
    posting the image, the function logs into the Instagram account using the
    provided username and password. The image is then uploaded to the account.

    Args:
        image (Image): The image to be posted.
        hashtags (list[str]): The hashtags to be included in the Instagram post.
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
    cl.photo_upload(path=temp_image_path, caption=" ".join(hashtags))
    os.remove(temp_image_path)
