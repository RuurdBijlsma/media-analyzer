from PIL.Image import Image

from media_analyzer.data.interfaces.visual_data import SummaryData, VisualData
from media_analyzer.media_analyzer import MediaAnalyzer
from media_analyzer.processing.pipeline.base_module import VisualModule


class SummaryModule(VisualModule):
    def process(self, data: VisualData, image: Image, analyzer: MediaAnalyzer) -> SummaryData:
        if not analyzer.config.enable_text_summary:
            return SummaryData(
                **data.model_dump(),
                summary=None,
            )
        prompt = (
            "Describe this image in a way that captures all essential details "
            "for a search database. Include the setting, key objects, actions, "
            "number and type of people or animals, and any noticeable visual "
            "features. Make the description clear, concise, and useful for "
            "someone searching this image in a library. Avoid subjective "
            "interpretations or ambiguous terms."
        )

        caption = analyzer.llm.image_question(image, prompt)

        return SummaryData(
            **data.model_dump(),
            summary=caption,
        )
