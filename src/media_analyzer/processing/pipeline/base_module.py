import time
from abc import ABC, abstractmethod
from typing import TypeVar

from PIL.Image import Image

from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.interfaces.image_data import ImageData
from media_analyzer.data.interfaces.visual_data import VisualData

T = TypeVar("T")


class BaseModule(ABC):
    run_times: list[float]
    name: str

    def __init__(self) -> None:
        self.name = self.__class__.__name__
        self.run_times = []


class FileModule(BaseModule):
    def run(self, data: ImageData, config: FullAnalyzerConfig) -> ImageData:
        start_time = time.time()
        result = self.process(data, config)
        self.run_times.append(time.time() - start_time)
        return result

    @abstractmethod
    def process(self, data: ImageData, config: FullAnalyzerConfig) -> ImageData: ...


class VisualModule(BaseModule):
    def run(self, data: VisualData, image: Image, config: FullAnalyzerConfig) -> VisualData:
        start_time = time.time()
        result = self.process(data, image, config)
        self.run_times.append(time.time() - start_time)
        return result

    @abstractmethod
    def process(self, data: VisualData, image: Image, config: FullAnalyzerConfig) -> VisualData: ...
