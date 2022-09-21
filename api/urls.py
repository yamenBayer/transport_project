import imp
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('trips/', views.getTrips),
    path('trips/create/', views.createTrip),
    path('trips/<str:tid>/update', views.editTrip),
    path('trips/<str:tid>/delete', views.removeTrip),
    path('trips/<str:tid>/', views.getTrip),
]
