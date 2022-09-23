from asyncio.windows_events import NULL
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TripSerializer
from .models import Profile, Reservation, Trip
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import uuid 



class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
          try:
            user = UserModel.objects.get(username=username)
          except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
          return user
        return None


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
        {
            'Endpoint' : '/trips/e_Wallet/charge/',
            'method' : 'PUT',
            'body' : {'body': ""},
            'description' : 'Charge an existing account with specific amount.'
        },
        {
            'Endpoint' : '/signup/',
            'method' : 'POST',
            'body' : {'body': ""},
            'description' : 'Create new account.'
        },
        {
            'Endpoint' : '/login/',
            'method' : 'POST',
            'body' : {'body': ""},
            'description' : 'Login to existing account.'
        },
        {
            'Endpoint' : '/logout/',
            'method' : 'GET',
            'body' : None,
            'description' : 'Logout from the authenticated account.'
        },

    ]
    return Response(routes)

@api_view(['POST'])
def sign_up(request):
#   if request.user.is_authenticated:
#     return Response('Already logged in!')

  if request.method == "POST":
    data = request.data
    first_name = data['first_name']
    last_name = data['last_name']
    public_Number = data['public_Number']
    phone = data['phone']
    gender = data['gender']
    password = data['password']
    password_confirm = data['password_confirm']

    if Profile.objects.filter(phone = phone):
      return Response('Client is already exist!')

    if not len(phone) == 10 :
      return Response('phone must be exactly 10 numbers!')

    if len(password)<8:
      return Response('Password must be at least 8 characters!')

    if password != password_confirm:
      return Response('password did not match!')

    email = phone + "_TEC@gmail.com"
    my_user = User.objects.create_user(phone,email,password)
    my_user.first_name = first_name
    my_user.last_name = last_name
    my_user.is_active = True
    my_user.save()

    
    e_wallet = uuid.uuid4().hex[:6].upper()
    new_profile = Profile(user = my_user, gender = gender, phone = phone, public_Number = public_Number, e_Wallet = e_wallet)
    new_profile.save()

    return Response('Account created successfully!')
    

  return Response('Nothing!')      



@api_view(['POST'])
def log_in(request):
#    if request.user.is_authenticated:
#       return Response('Already looged in!')

   if request.method == "POST":
      data = request.data
      phone = data['phone']
      password = data['password']

      user = authenticate(username=phone, password=password)
      if user is not None:
        login(request, user)
        return Response('Logged in!')

      return Response('Something went wrong!')
      
   return Response('Nothing!')      

    
@api_view(['GET'])
def sign_out(request):
    logout(request)
    return Response('Logged out successfully.')


@api_view(['GET'])
def getTrips(request):
    trips = Trip.objects.all()
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# def getMyTrips(request):
#     trips = Trip.objects.get()
#     serializer = TripSerializer(trips, many=True)
#     return Response(serializer.data)

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
    source = data['source']
    destination = data['destination']

    trip = Trip(title = title, date = date, trip_Time = trip_Time, is_Vip = is_Vip, cost = cost, source = source, destination = destination)
    trip.save()

    serializer = TripSerializer(trip, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def editTrip(request, tid):
    trip = Trip.objects.get(id = tid)

    serializer = TripSerializer(trip, data=request.data)
    if serializer.is_valid():
        serializer.save()
        
    return Response('Successfully edited!')

@api_view(['DELETE'])
def removeTrip(request, tid):
    Trip.objects.get(id = tid).delete() 
    return Response('Trip deleted successfully!')


@api_view(['GET'])
def search(request, source, destination):
    if Trip.objects.filter(source = source, destination = destination).exists():
        trips = Trip.objects.filter(source = source, destination = destination)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    return Response('No results!')

@api_view(['PUT'])
def takePlace(request, tid):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
        trip = Trip.objects.get(id = tid)
        if trip.capacity <= trip.counter:
            return Response('The bus is full!')

        data = request.data
        sits = data['sits']
        sitsINT = int(sits)

        if sitsINT <= trip.capacity:
            total = sitsINT * trip.cost
            reservation = Reservation(owner_name = profile.user.username, phone = profile.phone, sits_amount = sitsINT, total_cost = total)
            reservation.save()
            trip.reservations.add(reservation)
            trip.counter += sitsINT
            return Response('Reservation successfully done.')
        else:
            return Response('No enough space!')
        
    return Response('Client is not logged in!')



@api_view(['PUT'])
def charge(request, e_wallet):
    if Profile.objects.filter(e_Wallet = e_wallet).exists():
        profile = Profile.objects.get(e_Wallet = e_wallet)
        data = request.data
        amount = data['amount']
        amountINT = int(amount)
        profile.balance += amountINT
        profile.save()
        return Response('Successfully charged!')
    else:
        return Response('The client is not exists!')

