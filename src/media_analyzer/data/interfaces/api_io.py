from dataclasses import dataclass
from pathlib import Path

from media_analyzer.data.interfaces.image_data import WeatherData
from media_analyzer.data.interfaces.visual_data import MediaAnalyzerFrame


@dataclass
class InputMedia:
    path: Path
    frames: list[Path]

class MediaAnalyzerOutput(WeatherData):
    frame_data: list[MediaAnalyzerFrame]
