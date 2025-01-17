from PIL.Image import Image

from media_analyzer.data.interfaces.visual_data import CaptionData, VisualData
from media_analyzer.processing.pipeline.base_module import VisualModule


class CaptionModule(VisualModule):
    def process(self, frame: Path, data: VisualData, image: Image, analyzer: MediaAnalyzer) -> CaptionData:
        caption = analyzer.captioner.caption(image)

        return CaptionData(
            **data.model_dump(),
            caption=caption,
        )
