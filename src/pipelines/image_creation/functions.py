import ast

import numpy as np
import openai
from PIL import Image, ImageDraw, ImageFont
from kedro.config import OmegaConfigLoader  # noqa: E402


def create_white_image(params: dict[str]) -> Image:
    """Function to create a white canvas.

    Args:
        params (dict[str]): Contains the information about background color, image length and width.

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


def apply_text_on_image(image: Image, text: str, params: dict[str]) -> Image:
    """Function to apply the generated text on the white image canvas.

    For doing that, one needs to create the font, including style and size. Also
    the location of where the font is placed on the image needs to be decided.

    Args:
        image (Image): The canvas that we produced earlier.
        text (str): The quote that is to be printed on the image.

    Returns:
        Image: The inputted image with the text placed in the middle of the file.
    """
    font_color = ast.literal_eval(params["font_color"])
    font_file_path = params["font_location"]
    font_size = params["font_size"]
    margin_percentage = params["margin_percentage"]

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_file_path, font_size)

    # Calculate the maximum line length.
    max_line_length = _calculate_max_line_length(
        image_width=image.width,
        margin_percentage=margin_percentage,
        font=font,
        font_size=font_size,
    )

    # Calculate the total height of the text.
    adjusted_text = _introduce_line_breaks(text=text, max_line_length=max_line_length)
    total_text_height = sum(
        [draw.textsize(line, font=font)[1] for line in adjusted_text]
    )

    # Calculate the starting y-coordinate to center the text vertically
    y_start = (image.height - total_text_height) // 2

    # Draw each line of text
    for line in adjusted_text:
        text_width, text_height = draw.textsize(line, font=font)
        x = (image.width - text_width) // 2
        draw.text((x, y_start), line, font=font, fill=font_color)
        y_start += text_height  # Move down for the next line

    return image


def _calculate_max_line_length(
    image_width: int, margin_percentage: float, font, font_size: int
) -> int:
    """_summary_

    Args:
        image_width (float): _description_
        left_margin (float): _description_
        right_margin (float): _description_

    Returns:
        int: _description_
    """
    usable_width = image_width * (1 - (margin_percentage * 2))

    sample_character_width = ImageDraw.Draw(Image.new("RGB", (1, 1))).textsize(
        "X", font=font
    )[0]
    return usable_width // sample_character_width


def _introduce_line_breaks(text: str, max_line_length: int) -> str:
    """This function breaks the text to fit it within the maximum line length.

    Args:
        text (str): Text that needs to be broken into lines.
        max_line_length (int): Maximum length of each line.

    Returns:
        str: Text with line breaks.
    """
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) < max_line_length:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines
