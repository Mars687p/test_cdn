
from rest_framework import serializers

from .models import City
from .services import get_coord_by_name


class CreateCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'name',
        )

    def create(self, validated_data: dict) -> City:
        city_coord = get_coord_by_name(validated_data.get('name'))
        if city_coord is not None:
            city = City.objects.filter(name=city_coord['name'])
            if len(city) != 0:
                return city.values()
            return City.objects.create(**city_coord)


class GetCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'name',
            'longitude',
            'latitude',
        )
