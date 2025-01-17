from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from media_analyzer.data.enums.classification.weather_condition import WeatherCondition
from media_analyzer.data.interfaces.location_types import GeoLocation


class ImageData(BaseModel):
    path: Path
    frames: list[Path]


class ExifData(ImageData):
    width: int
    height: int
    duration: float | None
    size_bytes: int
    format: str
    # frontend filters
    is_motion_photo: bool
    is_hdr: bool
    is_night_sight: bool
    is_selfie: bool
    is_panorama: bool
    # exiftool output:
    exif_tool: dict[str, Any]
    file: dict[str, Any]
    composite: dict[str, Any]
    exif: dict[str, Any] | None
    xmp: dict[str, Any] | None
    jfif: dict[str, Any] | None
    icc_profile: dict[str, Any] | None
    gif: dict[str, Any] | None
    quicktime: dict[str, Any] | None
    matroska: dict[str, Any] | None


class DataUrlData(ExifData):
    data_url: str


class GpsData(DataUrlData):
    latitude: float | None = None
    longitude: float | None = None
    altitude: float | None = None
    datetime_utc: datetime | None = None
    location: GeoLocation | None = None


class TimeData(GpsData):
    datetime_local: datetime
    datetime_source: str
    timezone_name: str | None
    timezone_offset: timedelta | None


class WeatherData(TimeData):
    weather_recorded_at: datetime | None = None
    weather_temperature: float | None = None
    weather_dewpoint: float | None = None
    weather_relative_humidity: float | None = None
    weather_precipitation: float | None = None
    weather_wind_gust: float | None = None
    weather_pressure: float | None = None
    weather_sun_hours: float | None = None
    weather_condition: WeatherCondition | None = None
