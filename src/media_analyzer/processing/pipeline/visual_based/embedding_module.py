from PIL.Image import Image

from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.interfaces.visual_data import EmbeddingData, VisualData
from media_analyzer.machine_learning.embedding.clip_embedder import CLIPEmbedder
from media_analyzer.processing.pipeline.base_module import VisualModule

embedder = CLIPEmbedder()


class EmbeddingModule(VisualModule):
    def process(self, data: VisualData, image: Image, _: FullAnalyzerConfig) -> EmbeddingData:
        embedding = embedder.embed_image(image)
        return EmbeddingData(
            **data.model_dump(),
            embedding=embedding.tolist(),  # type: ignore[arg-type]
        )
