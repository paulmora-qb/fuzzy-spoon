"""Functions for the facts creation pipeline."""

from PIL import ImageFont
from common.utilities.text_tools import calculate_max_line_length, introduce_line_breaks


def create_text_dictionary(
    text_for_image: str,
    font: ImageFont.FreeTypeFont,
) -> dict[str, str]:
    """Create a dictionary from the text for the image.

    Args:
        text_for_image (str): Text for the image.
        font (ImageFont.FreeTypeFont): Font used for the text.

    Returns:
        Dictionary with the text for the image and the font that is used for that part.
    """
    fact_text = text_for_image.fact

    # Calculate the maximum line length.
    max_line_length = calculate_max_line_length(
        font=font,
    )

    # Introduce line breaks in the quote text.
    adjusted_text = introduce_line_breaks(
        text=fact_text, max_line_length=max_line_length
    )

    text_font_dict = {i: font for i in adjusted_text}
    return text_font_dict
