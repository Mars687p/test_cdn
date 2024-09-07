from geopy import exc as geopy_exception
from geopy.geocoders import Yandex

from citycoord.logs import logger
from citycoord.settings import API_KEY_GEOLOCATOR

from .exceptions import EmptyResponseGEocoder, RequestGeocoderUncomplited
from .types import CityResponseDict

geolocator = Yandex(api_key=API_KEY_GEOLOCATOR,
                    timeout=3)


def get_coord_by_name(city_name: str) -> CityResponseDict:
    try:
        response = geolocator.geocode(city_name)
    except geopy_exception.GeopyError as err:
        logger.error(err)
        raise RequestGeocoderUncomplited
    if response is None:
        raise EmptyResponseGEocoder
    return CityResponseDict({
        'name': response.address,
        'longitude': response.longitude,
        'latitude': response.latitude,
    })


def get_name_by_coord(longitude: float, latitude: float) -> CityResponseDict:
    try:
        response = geolocator.reverse(f"{longitude} {latitude}")
    except geopy_exception.GeopyError as err:
        logger.error(err)
        raise RequestGeocoderUncomplited
    if response is None:
        raise EmptyResponseGEocoder

    return CityResponseDict({
        'name': response.raw['description'],
        'longitude': longitude,
        'latitude': latitude
    })
