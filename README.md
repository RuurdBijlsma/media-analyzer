# Media Analyzer

Media Analyzer is a Python library designed to analyze media files, providing insights into their
content and metadata. It supports various functionalities, including image classification,
captioning, optical character recognition (OCR), and facial recognition.

## Features

- **Image Classification**: Identify objects, activities, animals, and events present in images.
- **Image Captioning**: Generate descriptive captions for images using models like BLIP and
  LLM-based captioners.
- **Optical Character Recognition (OCR)**: Extract text from images to identify documents, receipts,
  menus, and more.
- **Facial Recognition**: Detect faces in images and provide details such as age, sex, and facial
  landmarks.

## Installation

To install Media Analyzer, use pip:

```bash
pip install media-analyzer
```

### Requirements

You must have the following in PATH.

* ExifTool: https://exiftool.org/
* Tesseract OCR: https://tesseract-ocr.github.io/tessdoc/Installation.html

## Usage

Here's a basic example of how to use Media Analyzer:

```python
from media_analyzer import MediaAnalyzer
from pathlib import Path

analyzer = MediaAnalyzer()
media_file = Path("image.jpg")
result = analyzer.photo(media_file)

# Access analysis results
print(result.image_data)
print(result.frame_data)
```

Configuration

The AnalyzerSettings class allows you to customize various aspects of the analysis:

    media_languages: List of languages for OCR to consider.
    captions_provider: The provider for image captioning (e.g., 'BLIP', 'LLM').
    enable_text_summary: Enable or disable text summarization.
    enable_document_summary: Enable or disable document summarization.
    document_detection_threshold: Confidence threshold for document detection.
    face_detection_threshold: Confidence threshold for face detection.
    enabled_file_modules: List of file modules to enable (e.g., exif data, gps, weather detection).
    enabled_visual_modules: List of visual modules to enable (e.g., 'classification', 'captioning', 'ocr', 'facial_recognition').

Full docs can be found
at https://ruurdbijlsma.github.io/media-analyzer/media_analyzer.html#MediaAnalyzer.