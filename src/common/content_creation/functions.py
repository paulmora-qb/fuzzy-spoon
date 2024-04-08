import ast

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from common.llm.prompt_engineering.functions import prompt_wrapper
import pandas as pd
from common.utilities.text_tools import (
    calc_total_text_width_height,
    calculate_max_line_length,
    introduce_line_breaks,
)
from common.utilities.text_tools.text_tools import _adjust_output_parser_key


def save_pasts_text(
    namespace: str,
    text_dictionary: str,
    past_texts: pd.DataFrame,
) -> pd.DataFrame:
    """Function to save the past texts.

    Args:
        namespace (str): Namespace of the text.
        text (str): Text to be saved.
        past_texts (pd.DataFrame): DataFrame containing author and text.

    Returns:
        pd.DataFrame: DataFrame containing the topic, text and timestamp of the post.
    """
    entire_text = "".join(text_dictionary.keys())
    data = pd.DataFrame(
        {
            "topic": [namespace],
            "text": [entire_text],
            "timestamp": [pd.Timestamp.now()],
        }
    )
    return pd.concat([past_texts, data])


def create_text_for_image(
    system_message: str,
    instruction_message: str,
    output_parser_key: str,
    past_texts: pd.DataFrame,
) -> str:
    """Function to create the text that will be placed on the image.

    Args:
        system_message (str): System message which states how the AI should behave.
        instruction_message (str): Instruction message which states what the AI should
            do.
        output_parser_key (str): Key to the right output parser for the llm.
        past_texts (pd.DataFrame): DataFrame containing author and text.

    Returns:
        str: The output of the pipeline. This oftentimes is a class which has different
            attributes.
    """
    list_of_past_texts = past_texts.loc[:, "text"].tolist()
    parser_key, topic = _adjust_output_parser_key(output_parser_key=output_parser_key)
    adjusted_instruction_message = instruction_message.format(
        past_texts=str(list_of_past_texts),
        topic=topic,
        format_instructions="{format_instructions}",
    )
    return prompt_wrapper(
        system_message=system_message,
        instruction_message=adjusted_instruction_message,
        output_parser_key=parser_key,
    )


def create_white_image(params: dict[str]) -> Image:
    """Function to create a white canvas.

    Args:
        params (dict[str]): Contains the information about background color, image
            length and width.

    Returns:
        Image: Background image.
    """
    image_width = params["image_width"]
    image_length = params["image_length"]
    background_color = params["background_color"]

    white_array = np.full(
        (image_width, image_length, 3), background_color, dtype=np.uint8
    )
    return Image.fromarray(white_array, "RGB")


def apply_text_on_image(
    image: Image,
    text_dictionary: dict[str, ImageFont.FreeTypeFont],
    params: dict[str],
) -> Image:
    """Function to apply the generated text on the white image canvas.

    For doing that, one needs to create the font, including style and size. Also
    the location of where the font is placed on the image needs to be decided.

    Args:
        image (Image): Image on which the text needs to be placed.
        text_dictionary (dict[str, ImageFont.FreeTypeFont]): Dictionary containing the
            text and font used for the text.
        params (dict[str]): Contains the information about font color and margin

    Returns:
        Image: Image with the text placed on it.
    """
    font_color = ast.literal_eval(params["font_color"])
    draw = ImageDraw.Draw(image)

    # Calculate the total height of the text.
    _, total_height = calc_total_text_width_height(text_dictionary=text_dictionary)

    # # Calculate the starting y-coordinate to center the text vertically.
    y_start = (image.height - total_height) // 2

    # # Draw each line of text.
    for text, font in text_dictionary.items():
        _, _, text_width, text_height = draw.textbbox((0, 0), text=text, font=font)
        x = (image.width - text_width) // 2
        draw.text((x, y_start), text, font=font, fill=font_color)
        y_start += text_height  # Move down for the next line

    return image


def create_hashtags(
    text_dictionary: dict[str, ImageFont.FreeTypeFont],
    system_message: str,
    instruction_message: str,
    output_parser_key: str,
) -> list[str]:
    """This function creates hashtags for an Instagram post.

    Args:
        text_dictionary (dict[str, ImageFont.FreeTypeFont]): The text that will be
            placed on the image.
        system_message (str): System message which tells AI how to behave.
        instruction_message (str): Instruction message which tells AI what to do.
        output_parser_key (str): The key to the output parser.

    Returns:
        list[str]: The hashtags to be included in the Instagram post.
    """
    text_on_image = "".join(text_dictionary.keys())
    adjusted_instruction_message = instruction_message.format(
        topic="love", format_instructions="{format_instructions}"
    )

    return prompt_wrapper(
        system_message=system_message,
        instruction_message=adjusted_instruction_message,
        output_parser_key=output_parser_key,
    ).hashtag


def create_text_dictionary(
    text_for_image: str,
    font: ImageFont.FreeTypeFont,
) -> dict[str, str]:
    """Create a dictionary from the text for the image.

    Args:
        text_for_image: Text for the image.

    Returns:
        Dictionary with the text for the image.
    """
    text = text_for_image.text

    # Calculate the maximum line length.
    max_line_length = calculate_max_line_length(
        font=font,
    )

    # Introduce line breaks in the quote text.
    adjusted_text = introduce_line_breaks(text=text, max_line_length=max_line_length)
    adjusted_text += [" "]

    return {i: font for i in adjusted_text}
