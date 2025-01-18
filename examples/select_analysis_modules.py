from pathlib import Path

from media_analyzer import MediaAnalyzer
from media_analyzer.data.anaylzer_config import AnalyzerSettings

config = AnalyzerSettings(
    enabled_file_modules={"ExifModule"},  # Only do exif data analysis on file
    enabled_visual_modules={"CaptionModule"},  # Only do caption module as visual module
)
analyzer = MediaAnalyzer(config=config)
media_file = Path(__file__).parents[1] / "tests/assets/tent.jpg"
result = analyzer.photo(media_file)

print(result)

# Resulting json:
# {
#   "image_data": {
#     "exif": {
#       "width": 5312,
#       "height": 2988,
#       ...
#     },
#     "dataurl": null,
#     "gps": null,
#     "time": null,
#     "weather": null
#   },
#   "frame_data": [
#     {
#       "index": 0,
#       "ocr": null,
#       "embedding": null,
#       "faces": null,
#       "summary": null,
#       "caption": "There is a car parked next to a tent with a lot of luggage",
#       "objects": null,
#       "classification": null,
#       "measured_quality": null
#     }
#   ]
# }
