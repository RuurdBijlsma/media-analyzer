from PIL.Image import Image

from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.interfaces.visual_data import FacesData, VisualData
from media_analyzer.machine_learning.facial_recognition.insight_facial_recognition import (
    InsightFacialRecognition,
)
from media_analyzer.processing.pipeline.base_module import VisualModule

facial_recognition = InsightFacialRecognition()


class FacesModule(VisualModule):
    def process(self, data: VisualData, image: Image, _: FullAnalyzerConfig) -> FacesData:
        faces = facial_recognition.get_faces(image)

        return FacesData(
            **data.model_dump(),
            faces=faces,
        )
