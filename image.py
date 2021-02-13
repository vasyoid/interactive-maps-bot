import os

from io import BytesIO
from typing import Tuple

from PIL import Image


class ImageGenerator:

    def __init__(self):
        self._map_image: Image.Image = Image.open(os.path.join(os.getcwd(), "res", "map.jpg"))
        self._pointer_image: Image.Image = Image.open(os.path.join(os.getcwd(), "res", "pointer.png"))
        self._pointer_offset = (-self._pointer_image.size[0] // 2, -self._pointer_image.size[1])

    def _validate_pos(self, pos: Tuple[int, int]) -> bool:
        return 0 <= pos[0] < self._map_image.size[0] and 0 <= pos[1] < self._map_image.size[1]

    def generate(self, pos: Tuple[int, int]):
        if not self._validate_pos(pos):
            return None
        result = self._map_image.copy()
        pos = (pos[0] + self._pointer_offset[0], pos[1] + self._pointer_offset[1])
        result.paste(self._pointer_image, pos, self._pointer_image)
        with BytesIO() as fp:
            result.save(fp, format="JPEG")
            return fp.getbuffer().tobytes()
