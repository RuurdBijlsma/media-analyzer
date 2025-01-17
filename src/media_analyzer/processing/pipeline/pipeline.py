from dataclasses import dataclass
from pathlib import Path

import PIL.Image
import pillow_avif  # noqa: F401

from media_analyzer.data.interfaces.image_data import ImageData, WeatherData
from media_analyzer.data.interfaces.api_io import InputMedia
from media_analyzer.data.interfaces.visual_data import MediaAnalyzerFrame, VisualData
from media_analyzer.media_analyzer import MediaAnalyzer
from media_analyzer.processing.pipeline.base_module import FileModule, VisualModule
from media_analyzer.processing.pipeline.file_based.data_url_module import DataUrlModule
from media_analyzer.processing.pipeline.file_based.exif_module import ExifModule
from media_analyzer.processing.pipeline.file_based.gps_module import GpsModule
from media_analyzer.processing.pipeline.file_based.time_module import TimeModule
from media_analyzer.processing.pipeline.file_based.weather_module import WeatherModule
from media_analyzer.processing.pipeline.visual_based.caption_module import CaptionModule
from media_analyzer.processing.pipeline.visual_based.classification_module import (
    ClassificationModule,
)
from media_analyzer.processing.pipeline.visual_based.embedding_module import EmbeddingModule
from media_analyzer.processing.pipeline.visual_based.face_detection_module import FacesModule
from media_analyzer.processing.pipeline.visual_based.object_detection_module import ObjectsModule
from media_analyzer.processing.pipeline.visual_based.ocr_module import OCRModule
from media_analyzer.processing.pipeline.visual_based.quality_detection_module import QualityDetectionModule
from media_analyzer.processing.pipeline.visual_based.summary_module import SummaryModule
from media_analyzer.processing.processing.process_utils import pil_to_jpeg


@dataclass
class ScannableFrame:
    image_path: Path
    snapshot_time_ms: int = 0


image_pipeline: list[FileModule] = [
    ExifModule(),
    DataUrlModule(),
    GpsModule(),
    TimeModule(),
    WeatherModule(),
]

visual_pipeline: list[VisualModule] = [
    EmbeddingModule(),
    ClassificationModule(),
    OCRModule(),
    FacesModule(),
    SummaryModule(),
    CaptionModule(),
    ObjectsModule(),
    QualityDetectionModule(),
]


def run_metadata_pipeline(
        input_media: InputMedia,
        analyzer: MediaAnalyzer,
) -> tuple[WeatherData, list[MediaAnalyzerFrame]]:
    image_data = ImageData(path=input_media.path, frames=input_media.frames)

    for image_module in image_pipeline:
        image_data = image_module.run(image_data, analyzer)
    assert isinstance(image_data, WeatherData)

    visual_datas: list[MediaAnalyzerFrame] = []
    for i, frame_image_path in enumerate(input_media.frames):
        with PIL.Image.open(frame_image_path) as frame_image:
            jpeg_image = pil_to_jpeg(frame_image)

        visual_data = VisualData(index=i, path=frame_image_path)
        for visual_module in visual_pipeline:
            visual_data = visual_module.run(visual_data, jpeg_image, analyzer)
        assert isinstance(visual_data, MediaAnalyzerFrame)
        visual_datas.append(visual_data)
        jpeg_image.close()

    return image_data, visual_datas
