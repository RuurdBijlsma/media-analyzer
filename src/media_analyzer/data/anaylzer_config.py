from dataclasses import dataclass

from media_analyzer.data.enums.config_types import CaptionerProvider, LLMProvider
from media_analyzer.machine_learning.caption.captioner_protocol import CaptionerProtocol
from media_analyzer.machine_learning.classifier.base_classifier import BaseClassifier
from media_analyzer.machine_learning.embedding.embedder_protocol import EmbedderProtocol
from media_analyzer.machine_learning.ocr.ocr_protocol import OCRProtocol
from media_analyzer.machine_learning.visual_llm.base_visual_llm import BaseVisualLLM


@dataclass
class AnalyzerSettings:
    media_languages: tuple[str, ...] = ("nld", "eng")
    captions_provider: CaptionerProvider = CaptionerProvider.BLIP
    llm_provider: LLMProvider = LLMProvider.MINICPM
    enable_text_summary: bool = False
    enable_document_summary: bool = False
    document_detection_threshold: int = 65
    face_detection_threshold: float = 0.7


@dataclass
class FullAnalyzerConfig:
    llm: BaseVisualLLM
    captioner: CaptionerProtocol
    ocr: OCRProtocol
    classifier: BaseClassifier
    embedder: EmbedderProtocol
    settings: AnalyzerSettings
