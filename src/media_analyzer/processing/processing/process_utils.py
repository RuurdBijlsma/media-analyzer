import hashlib
import io
from pathlib import Path

import PIL
from PIL.Image import Image


def pil_to_jpeg(pil_image: Image) -> Image:
    # Weird conversion to jpg so pytesseract can handle the image
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)
    jpeg_data = img_byte_arr.getvalue()
    return PIL.Image.open(io.BytesIO(jpeg_data))
