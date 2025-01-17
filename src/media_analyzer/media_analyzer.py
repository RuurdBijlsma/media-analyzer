from media_analyzer.data.anaylzer_config import AnalyzerConfig
from media_analyzer.data.interfaces.input_media import InputMedia
from media_analyzer.machine_learning.caption.captioner_protocol import CaptionerProtocol
from media_analyzer.machine_learning.caption.get_captioner import get_captioner_by_provider
from media_analyzer.machine_learning.visual_llm.base_visual_llm import BaseVisualLLM
from media_analyzer.machine_learning.visual_llm.get_llm import get_llm_by_provider


class MediaAnalyzer:
    config: AnalyzerConfig
    llm: BaseVisualLLM
    captioner: CaptionerProtocol

    def __init__(self, config: AnalyzerConfig = AnalyzerConfig()):
        self.config = config
        self.llm = get_llm_by_provider(config.llm_provider)
        self.captioner = get_captioner_by_provider(config.captions_provider)

    def analyze(self, input_media: InputMedia):
        result=run_metadata_pipeline()
