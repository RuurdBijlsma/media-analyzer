import networkx as nx
import PIL.Image
import pillow_avif  # noqa: F401

from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.interfaces.api_io import InputMedia
from media_analyzer.data.interfaces.frame_data import FrameData
from media_analyzer.data.interfaces.image_data import ImageData
from media_analyzer.processing.pipeline.file_based.data_url_module import DataUrlModule
from media_analyzer.processing.pipeline.file_based.exif_module import ExifModule
from media_analyzer.processing.pipeline.file_based.gps_module import GpsModule
from media_analyzer.processing.pipeline.file_based.time_module import TimeModule
from media_analyzer.processing.pipeline.file_based.weather_module import WeatherModule
from media_analyzer.processing.pipeline.pipeline_module import PipelineModule
from media_analyzer.processing.pipeline.visual_based.caption_module import CaptionModule
from media_analyzer.processing.pipeline.visual_based.classification_module import (
    ClassificationModule,
)
from media_analyzer.processing.pipeline.visual_based.embedding_module import EmbeddingModule
from media_analyzer.processing.pipeline.visual_based.faces_module import FacesModule
from media_analyzer.processing.pipeline.visual_based.objects_module import ObjectsModule
from media_analyzer.processing.pipeline.visual_based.ocr_module import OCRModule
from media_analyzer.processing.pipeline.visual_based.quality_detection_module import (
    QualityDetectionModule,
)
from media_analyzer.processing.pipeline.visual_based.summary_module import SummaryModule
from media_analyzer.processing.process_utils import pil_to_jpeg

pipeline_classes = [DataUrlModule, ExifModule, GpsModule, TimeModule, WeatherModule, CaptionModule,
                    ClassificationModule, EmbeddingModule, FacesModule, ObjectsModule, OCRModule,
                    QualityDetectionModule, SummaryModule]
name_to_pipeline = {cls.__name__: cls for cls in pipeline_classes}


def topological_sort(modules: set[type[PipelineModule]]) -> list[str]:
    """Sort modules topologically based on their dependencies."""
    graph = nx.DiGraph()
    for module in modules:
        graph.add_node(module.__name__)
        for dependency in module.depends:
            graph.add_edge(module.__name__, dependency)

    try:
        return reversed(list(nx.topological_sort(graph)))
    except nx.NetworkXUnfeasible as e:
        raise ValueError("A cycle was detected in the dependency graph, "
        "and topological sorting is not possible.") from e


def run_metadata_pipeline(
    input_media: InputMedia,
    config: FullAnalyzerConfig,
) -> tuple[ImageData, list[FrameData]]:
    """Run the metadata pipeline on the input media."""
    image_data = ImageData(path=input_media.path, frames=input_media.frames)

    file_modules = [name_to_pipeline[module_name]() for module_name in topological_sort(
        {name_to_pipeline[name] for name in config.settings.enabled_file_modules}
    )]
    for image_module in file_modules:
        image_module.run(image_data, config)

    frame_datas: list[FrameData] = []
    for i, frame_image_path in enumerate(input_media.frames):
        with PIL.Image.open(frame_image_path) as frame_image:
            jpeg_image = pil_to_jpeg(frame_image)

        frame_data = FrameData(index=i, path=frame_image_path, image=jpeg_image)
        visual_modules = [name_to_pipeline[module_name]() for module_name in topological_sort(
            {name_to_pipeline[name] for name in config.settings.enabled_visual_modules}
        )]
        for visual_module in visual_modules:
            visual_module.run(frame_data, config)
        frame_datas.append(frame_data)
        jpeg_image.close()

    return image_data, frame_datas
