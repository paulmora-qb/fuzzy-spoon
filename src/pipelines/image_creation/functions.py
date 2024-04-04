import ast

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from libs.prompt_engineering.functions import prompt_wrapper
import pandas as pd


def save_pasts_text(
    text: str,
    past_texts: pd.DataFrame,
) -> pd.DataFrame:
    """Function to save the past texts.

    Args:
        text (str): Text to be saved.
        past_texts (pd.DataFrame): Dataframe containing author and text.

    Returns:
        list[str]: DataFrame containing the old dataframe and the new appended.
    """
    data = pd.DataFrame({"text": {0: text.quote}, "author": {0: text.author}})
    return pd.concat([past_texts, data])


def create_text_for_image(
    system_message: str,
    instruction_message: str,
    pydantic_object_path: str,
    past_texts: pd.DataFrame,
) -> str:
    """Function to create the text that will be placed on the image.

    Args:
        system_message (str): System message which states how the AI should behave.
        instruction_message (str): Instruction message which states what the AI should
            do.
        pydantic_object_path (str): Path of where the pydantic object is stored. This
            object states what attributes the output class should have.
        past_texts (pd.DataFrame): Dataframe containing author and text.

    Returns:
        str: The output of the pipeline. This oftentimes is a class which has different
            attributes.
    """
    list_of_past_texts = past_texts.loc[:, "text"].tolist()
    adjusted_instruction_message = instruction_message.format(
        past_texts=str(list_of_past_texts), format_instructions="{format_instructions}"
    )
    return prompt_wrapper(
        system_message=system_message,
        instruction_message=adjusted_instruction_message,
        pydantic_object_path=pydantic_object_path,
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
    text: str,
    quote_font: ImageFont.FreeTypeFont,
    author_font: ImageFont.FreeTypeFont,
    params: dict[str],
) -> Image:
    """Function to apply the generated text on the white image canvas.

    For doing that, one needs to create the font, including style and size. Also
    the location of where the font is placed on the image needs to be decided.

    Args:
        image (Image): Image on which the text needs to be placed.
        text (str): Text that needs to be placed on the image.
        quote_font (ImageFont.FreeTypeFont): Font for the quote.
        author_font (ImageFont.FreeTypeFont): Font for the author.
        params (dict[str]): Contains the information about font color and margin

    Returns:
        Image: Image with the text placed on it.
    """
    font_color = ast.literal_eval(params["font_color"])
    margin_percentage = params["margin_percentage"]
    draw = ImageDraw.Draw(image)

    # Calculate the maximum line length.
    max_line_length = _calculate_max_line_length(
        image_width=image.width,
        margin_percentage=margin_percentage,
        font=quote_font,
    )

    # Separate texts.
    quote_text = text.quote
    author_text = text.author

    # Introduce line breaks in the quote text.
    adjusted_text = _introduce_line_breaks(
        text=quote_text, max_line_length=max_line_length
    )
    adjusted_text += [" "]

    # Calculate the total height of the text.
    _, quote_text_height = _textsize(adjusted_text[0], font=quote_font)
    _, author_text_height = _textsize(author_text, font=author_font)
    total_text_height = (quote_text_height * len(adjusted_text)) + author_text_height

    text_font_dict = {i: quote_font for i in adjusted_text}
    text_font_dict[text.author] = author_font

    # Calculate the starting y-coordinate to center the text vertically.
    y_start = (image.height - total_text_height) // 2

    # Draw each line of text.
    for text, font in text_font_dict.items():
        _, _, text_width, text_height = draw.textbbox((0, 0), text=text, font=font)
        x = (image.width - text_width) // 2
        draw.text((x, y_start), text, font=font, fill=font_color)
        y_start += text_height  # Move down for the next line

    return image


def _textsize(text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    """This function calculates the width and height of the text.

    Args:
        text (str): Text whose size needs to be calculated.
        font (ImageFont.FreeTypeFont): Font used for the text.

    Returns:
        tuple[int, int]: Width and height of the text.
    """
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def _calculate_max_line_length(
    image_width: int, margin_percentage: float, font: ImageFont.FreeTypeFont
) -> int:
    """This function calculates the maximum line length that can fit in the image.

    Args:
        image_width (int): Width of the image.
        margin_percentage (float): Percentage of the margin.
        font (ImageFont.FreeTypeFont): Font used for the text.

    Returns:
        int: Maximum line length.
    """
    usable_width = image_width * (1 - (margin_percentage * 2))
    sample_character_width, _ = _textsize("a", font=font)
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
