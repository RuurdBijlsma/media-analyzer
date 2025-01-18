from pathlib import Path
from unittest.mock import patch

import pytest

from media_analyzer.data.anaylzer_config import AnalyzerSettings, FullAnalyzerConfig
from media_analyzer.media_analyzer import MediaAnalyzer


def test_media_analyzer_none_settings() -> None:
    """Test the MediaAnalyzer with no settings."""
    analyzer = MediaAnalyzer()
    assert isinstance(analyzer.config, FullAnalyzerConfig)


@pytest.mark.parametrize(
    "photo_filename",
    ["tent.jpg", "sunset.jpg", "ocr.jpg", "cluster.jpg", "cat.jpg", "face2_b.jpg"],
)
def test_media_analyzer(assets_folder: Path, default_config: AnalyzerSettings,
                        photo_filename: str) -> None:
    """Test the MediaAnalyzer functionality."""
    mock_caption_text = "A mock caption."
    with (
        patch("media_analyzer.machine_learning.caption.blip_captioner.BlipCaptioner.raw_caption")
        as mock_raw_caption
    ):
        mock_raw_caption.return_value = mock_caption_text
        analyzer = MediaAnalyzer(default_config)
        result = analyzer.photo(assets_folder / photo_filename)

    assert len(result.frame_data) == 1
    assert len(result.image_data.frames) == len(result.frame_data)
    assert result.image_data.path.name == photo_filename

    assert result.image_data.exif is not None
    assert result.image_data.dataurl is not None
    assert result.image_data.gps is not None
    assert result.image_data.time is not None
    assert result.image_data.weather is not None
