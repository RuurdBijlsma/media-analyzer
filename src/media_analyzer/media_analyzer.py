from media_analyzer.data.anaylzer_config import AnalyzerConfig
from media_analyzer.data.interfaces.api_io import InputMedia, MediaAnalyzerOutput
from media_analyzer.machine_learning.caption.captioner_protocol import CaptionerProtocol
from media_analyzer.machine_learning.caption.get_captioner import get_captioner_by_provider
from media_analyzer.machine_learning.classifier.base_classifier import BaseClassifier
from media_analyzer.machine_learning.classifier.clip_classifier import CLIPClassifier
from media_analyzer.machine_learning.embedding.clip_embedder import CLIPEmbedder
from media_analyzer.machine_learning.embedding.embedder_protocol import EmbedderProtocol
from media_analyzer.machine_learning.ocr.ocr_protocol import OCRProtocol
from media_analyzer.machine_learning.ocr.resnet_tesseract_ocr import ResnetTesseractOCR
from media_analyzer.machine_learning.visual_llm.base_visual_llm import BaseVisualLLM
from media_analyzer.machine_learning.visual_llm.get_llm import get_llm_by_provider
from media_analyzer.processing.pipeline.pipeline import run_metadata_pipeline


class MediaAnalyzer:
    config: AnalyzerConfig
    llm: BaseVisualLLM
    captioner: CaptionerProtocol
    ocr: OCRProtocol
    classifier: BaseClassifier
    embedder: EmbedderProtocol

    def __init__(self, config: AnalyzerConfig = AnalyzerConfig()):
        self.config = config
        self.llm = get_llm_by_provider(config.llm_provider)
        self.captioner = get_captioner_by_provider(config.captions_provider)
        self.ocr = ResnetTesseractOCR()
        self.embedder = CLIPEmbedder()
        self.classifier = CLIPClassifier(self.embedder)

    def analyze(self, input_media: InputMedia) -> MediaAnalyzerOutput:
        image_data, frame_data = run_metadata_pipeline(input_media, self)
        return MediaAnalyzerOutput(**image_data.model_dump(), frames=frame_data)
