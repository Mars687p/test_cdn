
from django.db import connection, models

from .types import CityResponseDict


class City(models.Model):
    name = models.CharField('Наименование',
                            max_length=128,
                            blank=True,
                            )
    longitude = models.DecimalField('Долгота',
                                    max_digits=9,
                                    decimal_places=6,
                                    blank=True,
                                    )
    latitude = models.DecimalField('Широта',
                                   max_digits=9,
                                   decimal_places=6,
                                   blank=True,
                                   )

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['longitude', 'latitude']
        indexes = [models.Index(fields=['name'])]

    def __str__(self) -> str:
        return f'Город: {self.name}'

    @staticmethod
    def get_nearest_cities(latitude, longitude) -> list[CityResponseDict]:
        """Здесь используется сырой запрос, который из строки с широтой и долготой
           создает обьект PostGis, которая оптимизирована для работы с географическими
           и геометрическими метками.
           Запрос возвращает 2 ближайших города от заданных координат
        """
        format_coord = 'SRID=4326;POINT({lat} {lng})'.format(lat=latitude,
                                                             lng=longitude)

        sql = """
            SELECT name, longitude, latitude, ST_Distance(format('SRID=4326;POINT(%%s %%s)',
                                                          longitude, latitude)::geography,
                                  %s::geography)/1000 as dist_km
            FROM cities_city
            ORDER BY format('SRID=4326;POINT(%%s %%s)', longitude, latitude)::geography <-> %s
            LIMIT 2;
            """

        with connection.cursor() as cursor:
            cursor.execute(sql, [format_coord, format_coord])
            rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(CityResponseDict(
                                {
                                    'name': row[0],
                                    'longitude': row[1],
                                    'latitude': row[2],
                                    'distance_km': row[3]
                                }
                ))
        return result
