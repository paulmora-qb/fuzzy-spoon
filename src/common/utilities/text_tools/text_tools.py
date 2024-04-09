"""Text tools functions."""

from PIL import Image, ImageDraw, ImageFont


def calculate_max_line_length(
    font: ImageFont.FreeTypeFont,
    image_width: int = 1080,
    margin_percentage: float = 0.1,
) -> int:
    """Calculate the maximum line length that can fit in the image.

    Args:
    ----
        image_width (int): Width of the image.
        margin_percentage (float): Percentage of the margin.
        font (ImageFont.FreeTypeFont): Font used for the text.

    Returns:
    -------
        int: Maximum line length.

    """
    usable_width = image_width * (1 - (margin_percentage * 2))
    sample_character_width, _ = _calc_text_width_height("a", font=font)
    return usable_width // sample_character_width


def introduce_line_breaks(text: str, max_line_length: int) -> str:
    """Break the text to fit it within the maximum line length.

    Args:
    ----
        text (str): Text that needs to be broken into lines.
        max_line_length (int): Maximum length of each line.

    Returns:
    -------
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


def calc_total_text_width_height(
    text_dictionary: dict[str, ImageFont.FreeTypeFont],
) -> tuple[int, int]:
    """Calculate the total width and height of the text.

    Args:
    ----
        text_dictionary (dict[str, ImageFont.FreeTypeFont]): Dictionary containing the
            text and font used for the text.

    Returns:
    -------
        tuple[int, int]: Total width and height of the text.

    """
    width_height_tuple = [
        _calc_text_width_height(text, font) for text, font in text_dictionary.items()
    ]
    max_width = max([width for width, _ in width_height_tuple])
    total_height = sum([height for _, height in width_height_tuple])
    return max_width, total_height


def _calc_text_width_height(text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    """Calculate the width and height of the text.

    Args:
    ----
        text (str): Text whose size needs to be calculated.
        font (ImageFont.FreeTypeFont): Font used for the text.

    Returns:
    -------
        tuple[int, int]: Width and height of the text.

    """
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def _adjust_output_parser_key(output_parser_key: str) -> str:
    """Adjust the output parser key.

    Args:
    ----
        output_parser_key (str): Name of the output parser key.

    Returns:
    -------
        str: Adjusted output parser key.

    """
    return output_parser_key.split(".")
