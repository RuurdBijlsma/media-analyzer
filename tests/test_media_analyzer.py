from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from media_analyzer.data.anaylzer_config import AnalyzerSettings, FullAnalyzerConfig
from media_analyzer.data.enums.classification.activity_type import ActivityType
from media_analyzer.data.enums.classification.people_type import PeopleType
from media_analyzer.data.enums.classification.scene_type import SceneType
from media_analyzer.media_analyzer import MediaAnalyzer


def test_media_analyzer_none_settings() -> None:
    analyzer = MediaAnalyzer()
    assert isinstance(analyzer.config, FullAnalyzerConfig)


@pytest.mark.parametrize(
    "photo_filename",
    ["tent.jpg", "sunset.jpg", "ocr.jpg", "cluster.jpg", "cat.jpg", "face2_b.jpg"],
)
def test_media_analyzer(assets_folder: Path, default_config: AnalyzerSettings, photo_filename: str) -> None:
    with patch("media_analyzer.machine_learning.caption.blip_captioner.BlipCaptioner.raw_caption") as mock_raw_caption:
        mock_raw_caption.return_value = "A mock caption."
        analyzer = MediaAnalyzer(default_config)
        result = analyzer.photo(assets_folder / photo_filename)

    assert isinstance(result.frames, list)
    assert isinstance(result.frame_data, list)
    assert len(result.frame_data) == len(result.frames)
    assert isinstance(result.latitude, float | None)
    assert isinstance(result.longitude, float | None)
    assert isinstance(result.altitude, float | None)
    assert isinstance(result.composite, dict)
    assert isinstance(result.exif, dict | None)
    assert isinstance(result.file, dict)
    assert isinstance(result.datetime_local, datetime | None)
    assert isinstance(result.datetime_source, str)
    assert isinstance(result.datetime_utc, datetime | None)
    if result.location is not None:
        assert isinstance(result.location.country, str)
        assert isinstance(result.location.city, str)
        assert isinstance(result.location.province, str | None)
    assert isinstance(result.weather_temperature, float | None)
    assert isinstance(result.width, int)
    assert isinstance(result.height, int)
    assert isinstance(result.timezone_name, str | None)
    assert isinstance(result.timezone_offset, timedelta | None)
    # Assertions for the visual data
    assert len(result.frame_data) == 1
    frame_data = result.frame_data[0]
    assert isinstance(frame_data.index, int)
    assert isinstance(frame_data.activity_type, ActivityType | None)
    assert isinstance(frame_data.scene_type, SceneType | None)
    assert isinstance(frame_data.caption, str)
    assert isinstance(frame_data.has_legible_text, bool)
    assert isinstance(frame_data.is_cityscape, bool)
    assert isinstance(frame_data.measured_brightness, float)
    assert isinstance(frame_data.measured_clipping, float)
    assert isinstance(frame_data.measured_contrast, float)
    assert isinstance(frame_data.measured_dynamic_range, float)
    assert isinstance(frame_data.measured_sharpness, float)
    assert isinstance(frame_data.measured_noise, int)
    assert isinstance(frame_data.objects, list)
    assert all(isinstance(obj.label, str) for obj in frame_data.objects)
    assert all(isinstance(obj.confidence, float) for obj in frame_data.objects)
    assert isinstance(frame_data.faces, list)
    assert isinstance(frame_data.ocr_boxes, list)
    assert isinstance(frame_data.ocr_text, str | None)
    assert isinstance(frame_data.people_type, PeopleType | None)
