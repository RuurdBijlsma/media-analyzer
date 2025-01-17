from PIL.Image import Image

from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.interfaces.visual_data import CaptionData, VisualData
from media_analyzer.processing.pipeline.base_module import VisualModule


class CaptionModule(VisualModule):
    def process(self, data: VisualData, image: Image, config: FullAnalyzerConfig) -> CaptionData:
        caption = config.captioner.caption(image)

        return CaptionData(
            **data.model_dump(),
            caption=caption,
        )
