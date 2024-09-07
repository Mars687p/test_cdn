from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .exceptions import EmptyResponseGEocoder, RequestGeocoderUncomplited
from .models import City
from .serializers import CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def create(self, request: Request,
               *args: tuple, **kwargs: dict) -> Response:
        try:
            return super().create(request, *args, **kwargs)
        except (RequestGeocoderUncomplited, EmptyResponseGEocoder):
            return Response({'error': 'Не удалось найти город'})

    def list(self, request: Request,
             *args: tuple, **kwargs: dict) -> Response:
        if request.data.get('name') is not None:
            return Response(City.objects.filter(
                            name__icontains=request.data.get('name')).values()
                            )

        if request.data.get('longitude') and request.data.get('latitude'):
            nearest_cities = City.get_nearest_cities(
                                          request.data.get('latitude'),
                                          request.data.get('longitude')
                                          )
            return Response(nearest_cities)
        return super().list(request, *args, **kwargs)

    def destroy(self, request: Request,
                *args: tuple, **kwargs: dict) -> Response:
        if request.data.get('name') is not None:
            return Response(City.objects.filter(
                                name__icontains=request.data.get('name'))[0].delete())
        return Response({'error': 'Не удалось найти город'})


def reverse_on_api(request: HttpRequest) -> HttpResponseRedirect:
    return HttpResponseRedirect(reverse('list'))
