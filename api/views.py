from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TripSerializer
from .models import Trip

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint' : '/trips/',
            'method' : 'GET',
            'body' : None,
            'description' : 'Returns an array of trips'
        },
        {
            'Endpoint' : '/trips/id',
            'method' : 'GET',
            'body' : None,
            'description' : 'Returns a single trip object'
        },
        {
            'Endpoint' : '/trips/create/',
            'method' : 'POST',
            'body' : {'body': ""},
            'description' : 'Create new trip with data sent in post request'
        },
        {
            'Endpoint' : '/trips/id/update/',
            'method' : 'PUT',
            'body' : {'body': ""},
            'description' : 'Update trip information with data sent in post request'
        },
        {
            'Endpoint' : '/trips/id/delete/',
            'method' : 'DELETE',
            'body' : None,
            'description' : 'Deletes an existing trip'
        },

    ]
    return Response(routes)

@api_view(['GET'])
def getTrips(request):
    trips = Trip.objects.all()
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTrip(request, tid):
    trip = Trip.objects.get(id = tid)
    serializer = TripSerializer(trip, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createTrip(request):
    data = request.data

    title = data['title']
    date = data['date']
    trip_Time = data['trip_Time']
    is_Vip = data['is_Vip']
    cost = data['cost']
    start_Place = data['start_Place']
    destination = data['destination']

    trip = Trip(title = title, date = date, trip_Time = trip_Time, is_Vip = is_Vip, cost = cost, start_Place = start_Place, destination = destination)
    trip.save()

    serializer = TripSerializer(trip, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def editTrip(request, tid):
    trip = Trip.objects.get(id = tid)

    serializer = TripSerializer(trip, data=request.data)
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)

@api_view(['DELETE'])
def removeTrip(request, tid):
    Trip.objects.get(id = tid).delete() 
    return Response('Trip deleted successfully!')


