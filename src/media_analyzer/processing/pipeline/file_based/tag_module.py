import math
from datetime import timedelta
from typing import ClassVar

from meteostat import Hourly, Point

from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.enums.classification.weather_condition import WeatherCondition
from media_analyzer.data.enums.analyzer_module import FileModule
from media_analyzer.data.interfaces.image_data import ImageData, WeatherData, TagData
from media_analyzer.processing.pipeline.pipeline_module import PipelineModule


class TagModule(PipelineModule[ImageData, FileModule]):
    """Extract weather data from the time and place an image was taken."""

    depends: ClassVar[set[FileModule]] = {FileModule.EXIF}

    def process(self, data: ImageData, _: FullAnalyzerConfig) -> None:
        """Get tags such as is_panorama, is_night_sight, is_motion_photo, etc."""
        assert data.exif is not None
        is_panorama = data.exif.width / data.exif.height > 2

        # TODO the rest

        data.tags = TagData(
            is_hdr=False,
            is_360=False,
            is_burst=False,
            is_panorama=is_panorama,
            is_timelapse=False,
            is_slowmotion=False,
            is_night_sight=False,
            is_motion_photo=False,
        )
