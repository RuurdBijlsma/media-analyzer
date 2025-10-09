from pathlib import Path

import pytest

from media_analyzer.data.anaylzer_config import AnalyzerSettings
from media_analyzer.data.enums.analyzer_module import VisualModule


@pytest.fixture
def assets_folder() -> Path:
    """Return the path to the assets folder."""
    return Path(__file__).parent / "assets"


@pytest.fixture
def default_config() -> AnalyzerSettings:
    """Return a default instance of AnalyzerSettings."""
    return AnalyzerSettings()


@pytest.fixture
def non_cuda_config() -> AnalyzerSettings:
    """Return a non-cuda instance of AnalyzerSettings."""
    return AnalyzerSettings(
        enabled_visual_modules={
            VisualModule.FACES,
            VisualModule.OBJECTS,
            VisualModule.OCR,
            VisualModule.QUALITY_DETECTION,
            VisualModule.SUMMARY,
            VisualModule.COLOR,
        }
    )
