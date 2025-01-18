from dataclasses import dataclass


@dataclass
class GeoLocation:
    """Represents a reverse geocoded location where a photo/video was taken.

    Attributes:
        country: The country name.
        city: The city name.
        province: The province or state name, if applicable.
        latitude: The latitude coordinate of the location.
        longitude: The longitude coordinate of the location.
    """

    country: str
    city: str
    province: str | None
    latitude: float
    longitude: float
