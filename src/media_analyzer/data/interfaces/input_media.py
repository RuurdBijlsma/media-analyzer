from dataclasses import dataclass
from pathlib import Path


@dataclass
class InputMedia:
    path: Path
    frames: list[Path]
