"""Dataset for images in png format."""

from typing import Any, Dict

import numpy as np
from kedro.io import AbstractDataset
from PIL import Image
from kedro.io.core import get_filepath_str, get_protocol_and_path
from pathlib import PurePosixPath
import fsspec
import os


class ImageDataset(AbstractDataset[np.ndarray, np.ndarray]):
    """``ImageDatset`` loads font data.

    Example:
    -------
    ::

        >>> ImageDataset(filepath='/img/file/path.png')

    """

    def __init__(self, filepath: str):
        """Create a new instance of ImageDataset to load / save filepath.

        Args:
        ----
            filepath: The location of the image file to load / save data.

        """
        protocol, path = get_protocol_and_path(filepath)
        self._protocol = protocol
        self._filepath = PurePosixPath(path)
        self._fs = fsspec.filesystem(self._protocol)

    def _load(self) -> None:
        """Not intended to load images in."""

    def _save(self, data: np.ndarray) -> None:
        """Not intended to save the font data."""
        save_path = get_filepath_str(self._filepath, self._protocol)
        folder_path = save_path.rsplit("/", 1)[0]
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with self._fs.open(save_path, mode="wb") as f:
            data.save(f)

    def _describe(self) -> Dict[str, Any]:
        """Not intended to describe the data."""
        pass
