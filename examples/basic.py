import json
from dataclasses import asdict
from pathlib import Path

from media_analyzer import MediaAnalyzer

analyzer = MediaAnalyzer()
media_file = Path(__file__).parents[1] / "tests/assets/ocr.jpg"
result = analyzer.photo(media_file)

print(json.dumps(asdict(result), indent=2))
