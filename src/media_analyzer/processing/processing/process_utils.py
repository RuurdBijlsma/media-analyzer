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


def readable_bytes(num: int, suffix: str = "B") -> str:
    fnum = float(num)
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        si_unit_max = 1024.0
        if abs(fnum) < si_unit_max:
            return f"{fnum:3.1f}{unit}{suffix}"
        fnum /= 1024.0
    return f"{fnum:.1f}Yi{suffix}"


def hash_image(image_path: Path, chunk_size: int = 65536) -> str:
    hasher = hashlib.sha256()

    with image_path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hasher.update(chunk)

    return hasher.hexdigest()
