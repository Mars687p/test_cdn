from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .exceptions import EmptyResponseGEocoder, RequestGeocoderUncomplited
from .models import City
from .serializers import CreateCitySerializer, GetCitySerializer


class CRUDCityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CreateCitySerializer
    http_method_names = ['post', 'delete', 'put']

    def create(self, request: Request,
               *args: tuple, **kwargs: dict) -> Response:
        try:
            return super().create(request, *args, **kwargs)
        except (RequestGeocoderUncomplited, EmptyResponseGEocoder):
            return Response({'error': 'Не удалось найти город'}, 404)

    def destroy(self, request: Request) -> Response:
        if request.data.get('name') is not None:
            city = City.objects.filter(
                                name=request.data.get('name'))
            if len(city) > 0:
                return Response(city[0].delete())
        if request.data.get('id') is not None:
            return Response(City.objects.get(id=request.data.get('id')).delete())
        return Response({'error': 'Не удалось найти город'}, 404)


class GetCityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = GetCitySerializer
    http_method_names = ['get']

    def list(self, request: Request,
             *args: tuple, **kwargs: dict) -> Response:
        if request.query_params.get('name') is not None:
            return Response(City.objects.filter(
                        name__icontains=request.query_params.get('name')).values()
                            )

        if request.query_params.get('longitude') and request.query_params.get('latitude'):
            nearest_cities = City.get_nearest_cities(
                                          request.query_params.get('latitude'),
                                          request.query_params.get('longitude')
                                          )
            return Response(nearest_cities)
        return super().list(request, *args, **kwargs)


def reverse_on_api(request: HttpRequest) -> HttpResponseRedirect:
    return HttpResponseRedirect(reverse('list'))
