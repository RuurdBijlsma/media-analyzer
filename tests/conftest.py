from pathlib import Path

import pytest

from media_analyzer.data.anaylzer_config import AnalyzerSettings


@pytest.fixture
def assets_folder() -> Path:
    return Path(__file__).parent / "assets"


@pytest.fixture
def default_config() -> AnalyzerSettings:
    return AnalyzerSettings()
