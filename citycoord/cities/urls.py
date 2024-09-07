from django.urls import path

from . import views

urlpatterns = [
    path('', views.reverse_on_api),
    path('api/v1/cities/', views.GetCityViewSet.as_view({'get': 'list'}), name='list'),
    path('api/v1/cities/create/', views.CRUDCityViewSet.as_view({'post': 'create'})),
    path('api/v1/cities/delete/', views.CRUDCityViewSet.as_view({'delete': 'destroy'})),

]
