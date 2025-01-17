import base64
from io import BytesIO

import PIL
import pillow_avif  # noqa: F401

from media_analyzer.data.interfaces.image_data import DataUrlData, ImageData
from media_analyzer.processing.pipeline.base_module import FileModule


class DataUrlModule(FileModule):
    def process(self, input_media: InputMedia, data: ImageData, analyzer: MediaAnalyzer) -> DataUrlData:
        tiny_height = 6
        with PIL.Image.open(input_media.frames[0]) as pil_image:
            img = pil_image.resize(
                (
                    int(pil_image.width / pil_image.height * tiny_height),
                    tiny_height,
                ),
            )
            buffered = BytesIO()
            img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return DataUrlData(
            **data.model_dump(),
            data_url=f"data:image/png;base64,{img_str}",
        )
