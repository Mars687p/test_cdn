from decimal import Decimal
from typing import Optional, TypedDict


class CityResponseDict(TypedDict):
    name: str
    longitude: Decimal
    latitude: Decimal
    distance_km: Optional[Decimal]
