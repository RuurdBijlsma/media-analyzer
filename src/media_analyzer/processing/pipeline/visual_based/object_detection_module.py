from PIL.Image import Image

from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.interfaces.visual_data import ObjectsData, VisualData
from media_analyzer.machine_learning.object_detection.resnet_object_detection import (
    ResnetObjectDetection,
)
from media_analyzer.processing.pipeline.base_module import VisualModule

detector = ResnetObjectDetection()


class ObjectsModule(VisualModule):
    def process(self, data: VisualData, image: Image, _: FullAnalyzerConfig) -> ObjectsData:
        objects = detector.detect_objects(image)

        return ObjectsData(
            **data.model_dump(),
            objects=objects,
        )
