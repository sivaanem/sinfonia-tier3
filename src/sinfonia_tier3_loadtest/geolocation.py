from dataclasses import dataclass


@dataclass(init=True)
class GeoLocation:
    lat: float = 0
    long: float = 0
    