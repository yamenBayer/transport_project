import imp
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('signup/', views.sign_up),
    path('login/', views.log_in),
    path('logout/', views.sign_out),
    path('trips/', views.getTrips),
    path('trips/me/', views.getMyTrips),
    path('search/<str:source>/<str:destination>/<str:date>/<str:time>', views.search),
    path('trips/create/', views.createTrip),
    path('trips/<str:tid>/update', views.editTrip),
    path('trips/<str:tid>/delete', views.removeTrip),
    path('trips/<str:e_wallet>/charge', views.charge),
    path('trips/<str:tid>/reservation', views.takePlace),
    path('trips/<str:tid>/', views.getTrip),
]
