from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'cities', views.CityViewSet, basename='cities')

urlpatterns = [
    path('', views.reverse_on_api),
    path('api/v1/delete/', views.CityViewSet.as_view({'DELETE': 'delete_city'})),
    path('api/v1/', include(router.urls)),

]
