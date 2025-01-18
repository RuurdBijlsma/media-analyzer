from pathlib import Path

from media_analyzer.data.anaylzer_config import AnalyzerSettings, FullAnalyzerConfig
from media_analyzer.data.interfaces.api_io import InputMedia, MediaAnalyzerOutput
from media_analyzer.machine_learning.caption.get_captioner import get_captioner_by_provider
from media_analyzer.machine_learning.classifier.clip_classifier import CLIPClassifier
from media_analyzer.machine_learning.embedding.clip_embedder import CLIPEmbedder
from media_analyzer.machine_learning.ocr.resnet_tesseract_ocr import ResnetTesseractOCR
from media_analyzer.machine_learning.visual_llm.get_llm import get_llm_by_provider
from media_analyzer.processing.pipeline.pipeline import run_metadata_pipeline


class MediaAnalyzer:
    """Analyze media using a machine learning models, file based analysis, and exif data."""

    config: FullAnalyzerConfig

    def __init__(self, config: AnalyzerSettings | None = None) -> None:
        """Initialize the media analyzer with the given configuration."""
        if config is None:
            config = AnalyzerSettings()
        embedder = CLIPEmbedder()
        self.config = FullAnalyzerConfig(
            llm=get_llm_by_provider(config.llm_provider),
            captioner=get_captioner_by_provider(config.captions_provider),
            ocr=ResnetTesseractOCR(),
            embedder=embedder,
            classifier=CLIPClassifier(embedder),
            settings=config,
        )

    def analyze(self, input_media: InputMedia) -> MediaAnalyzerOutput:
        """Analyze the given photo or video."""
        image_data, frame_data = run_metadata_pipeline(input_media, self.config)
        return MediaAnalyzerOutput(image_data=image_data, frame_data=frame_data)

    def photo(self, image_path: Path) -> MediaAnalyzerOutput:
        """Analyze a photo."""
        return self.analyze(InputMedia(image_path, frames=[image_path]))
