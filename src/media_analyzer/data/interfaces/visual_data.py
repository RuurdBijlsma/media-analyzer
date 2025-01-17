from pathlib import Path

from pydantic import BaseModel

from media_analyzer.data.enums.classification.activity_type import ActivityType
from media_analyzer.data.enums.classification.animal_type import AnimalType
from media_analyzer.data.enums.classification.document_type import DocumentType
from media_analyzer.data.enums.classification.event_type import EventType
from media_analyzer.data.enums.classification.object_type import ObjectType
from media_analyzer.data.enums.classification.people_type import PeopleType
from media_analyzer.data.enums.classification.scene_type import SceneType
from media_analyzer.data.enums.classification.weather_condition import WeatherCondition
from media_analyzer.data.interfaces.ml_types import FaceBox, ObjectBox, OCRBox


class VisualData(BaseModel):
    index: int
    path:Path


class EmbeddingData(VisualData):
    embedding: list[float]


class ClassificationData(EmbeddingData):
    scene_type: SceneType
    people_type: PeopleType | None
    animal_type: AnimalType | None
    document_type: DocumentType | None
    object_type: ObjectType | None
    activity_type: ActivityType | None
    event_type: EventType | None
    weather_condition: WeatherCondition | None
    is_outside: bool
    is_landscape: bool
    is_cityscape: bool
    is_travel: bool


class OCRData(ClassificationData):
    has_legible_text: bool
    ocr_text: str | None
    document_summary: str | None
    ocr_boxes: list[OCRBox]


class FacesData(OCRData):
    faces: list[FaceBox]


class SummaryData(FacesData):
    summary: str | None


class CaptionData(SummaryData):
    caption: str


class ObjectsData(CaptionData):
    objects: list[ObjectBox]


class MediaAnalyzerFrame(ObjectsData):
    measured_sharpness: float
    measured_noise: int
    measured_brightness: float
    measured_contrast: float
    measured_clipping: float
    measured_dynamic_range: float
    quality_score: float
