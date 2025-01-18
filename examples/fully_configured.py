import json
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path

from media_analyzer import MediaAnalyzer
from media_analyzer.data.anaylzer_config import AnalyzerSettings
from media_analyzer.data.enums.config_types import CaptionerProvider, LLMProvider

config = AnalyzerSettings(
    media_languages=("eng",),
    captions_provider=CaptionerProvider.MINICPM,
    llm_provider=LLMProvider.MINICPM,
    enable_text_summary=True,
    enable_document_summary=True,
    document_detection_threshold=50,
    face_detection_threshold=0.5,
    # You can turn off modules by selecting only the ones you need:
    # enabled_file_modules={"ExifModule"},
    # enabled_visual_modules={"CaptionModule"},
)
analyzer = MediaAnalyzer(config=config)
media_file = Path(__file__).parents[1] / "tests/assets/tent.jpg"
result = analyzer.photo(media_file)


# Serialize result to json
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        return obj.total_seconds()
    raise TypeError(f"Type {type(obj)} not serializable")


print(json.dumps(asdict(result), indent=2, default=custom_serializer))

# print(asdict(result))
