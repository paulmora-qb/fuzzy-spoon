"""Functions for quote creation pipeline."""

from PIL import ImageFont
from common.utilities.text_tools import calculate_max_line_length, introduce_line_breaks


def create_text_dictionary(
    text_for_image: str,
    quote_font: ImageFont.FreeTypeFont,
    author_font: ImageFont.FreeTypeFont,
) -> dict[str, str]:
    """Create a dictionary from the text for the image.

    Args:
        text_for_image: Text for the image.

    Returns:
        Dictionary with the text for the image.
    """
    # Separate texts.
    quote_text = text_for_image.quote
    author_text = text_for_image.author

    # Calculate the maximum line length.
    max_line_length = calculate_max_line_length(
        font=quote_font,
    )

    # Introduce line breaks in the quote text.
    adjusted_text = introduce_line_breaks(
        text=quote_text, max_line_length=max_line_length
    )
    adjusted_text += [" "]

    text_font_dict = {i: quote_font for i in adjusted_text}
    text_font_dict[author_text] = author_font
    return text_font_dict
