"""Dataset for fonts."""

from typing import Any, Dict

import numpy as np
from kedro.io import AbstractDataset
from PIL import ImageFont


class FontDataset(AbstractDataset[np.ndarray, np.ndarray]):
    """``FontDataset`` loads font data.

    Example:
    -------
    ::

        >>> FontDataset(filepath='/img/file/path.png')

    """

    def __init__(self, filepath: str, fontsize: int):
        """Create a new instance of FontDataset to load / save filepath.

        Args:
        ----
            filepath: The location of the font file to load / save data.
            fontsize: The size of the font.

        """
        self._filepath = filepath
        self._fontsize = fontsize

    def _load(self) -> ImageFont.FreeTypeFont:
        """Load data from the image file.

        Returns
        -------
            Data from the image file as a numpy array.

        """
        return ImageFont.truetype(self._filepath, self._fontsize)

    def _save(self, data: np.ndarray) -> None:
        """Not intended to save the font data."""
        pass

    def _describe(self) -> Dict[str, Any]:
        """Return the attributes of the dataset."""
        pass
