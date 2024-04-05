"""Functions for quote creation pipeline."""

from PIL import ImageFont, ImageDraw, Image


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
    a = 1
    # # Calculate the maximum line length.
    # max_line_length = _calculate_max_line_length(
    #     image_width=image.width,
    #     margin_percentage=margin_percentage,
    #     font=quote_font,
    # )

    # # Separate texts.
    # quote_text = text.quote
    # author_text = text.author

    # # Introduce line breaks in the quote text.
    # adjusted_text = _introduce_line_breaks(
    #     text=quote_text, max_line_length=max_line_length
    # )
    # adjusted_text += [" "]

    # # Calculate the total height of the text.
    # _, quote_text_height = _textsize(adjusted_text[0], font=quote_font)
    # _, author_text_height = _textsize(author_text, font=author_font)
    # total_text_height = (quote_text_height * len(adjusted_text)) + author_text_height

    # text_font_dict = {i: quote_font for i in adjusted_text}
    # text_font_dict[text.author] = author_font
    return {"text": text_for_image}


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
