from pathlib import Path

from media_analyzer.data.anaylzer_config import AnalyzerSettings
from media_analyzer.media_analyzer import MediaAnalyzer


def test_media_analyzer(assets_folder: Path, default_config:AnalyzerSettings)->None:
    analyzer = MediaAnalyzer(default_config)
    result = analyzer.photo(assets_folder / "tent.jpg")
    assert result is not None
