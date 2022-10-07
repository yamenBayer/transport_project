from asyncio.windows_events import NULL
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProfileSerializer, ReservationSerializer, TripSerializer
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
            'Endpoint' : '/trips',
            'method' : 'GET',
            'body' : None,
            'description' : 'Returns an array of trips'
        },
        {
            'Endpoint' : '/trips/<id>',
            'method' : 'GET',
            'body' : None,
            'description' : 'Returns a single trip object'
        },
        {
            'Endpoint' : '/trips/create',
            'method' : 'POST',
            'body' : {
                'title': "String|Required",
                'date': "Date",
                'trip_Time': "Time",
                'is_Vip': "Boolean",
                'cost': "Integer",
                'source': "String|Required",
                'destination': "String|Required"
            },
            'description' : 'Create new trip with data sent in post request'
        },
        {
            'Endpoint' : '/trips/<id>/update',
            'method' : 'PUT',
            'body' : {
                'title': "String|Required",
                'date': "Date",
                'trip_Time': "Time",
                'is_Vip': "Boolean",
                'cost': "Integer",
                'source': "String|Required",
                'destination': "String|Required"
                },
            'description' : 'Update trip information with data sent in post request'
        },
        {
            'Endpoint' : '/trips/<id>/delete',
            'method' : 'DELETE',
            'body' : None,
            'description' : 'Deletes an existing trip'
        },
        {
            'Endpoint' : '/<e_Wallet>/charge/',
            'method' : 'PUT',
            'body' : {
                'e_Wallet': "String|Required",
                'amount': "Integer|Required"
                },
            'description' : 'Charge an existing account with specific amount.'
        },
        {
            'Endpoint' : '/signup',
            'method' : 'POST',
            'body' : {
                'first_name': "String",
                'last_name': "String",
                'birthday': "String|Required",
                'phone': "String|Required",
                'gender': "String|Required",
                'password': "String|Required",
                'password_confirm': "String|Required"
                },
            'description' : 'Create new account.'
        },
        {
            'Endpoint' : '/adminSignup',
            'method' : 'POST',
            'body' : {
                'first_name': "String",
                'last_name': "String",
                'birthday': "String|Required",
                'phone': "String|Required",
                'gender': "String|Required",
                'password': "String|Required",
                'password_confirm': "String|Required",
                'is_Admin': "Boolean",
                'is_Charger': "Boolean",
                'balance': "Integer",
                },
            'description' : 'Create new account /Admin interface/.'
        },
        {
            'Endpoint' : '/login',
            'method' : 'POST',
            'body' : {
                'phone': "String|Required",
                'password': "String|Required"
                },
            'description' : 'Login to existing account.'
        },
        {
            'Endpoint' : '/logout',
            'method' : 'GET',
            'body' : None,
            'description' : 'Logout from the authenticated account.'
        },
        {
            'Endpoint' : '/trips/me/<e_Wallet>',
            'method' : 'GET',
            'body' : None,
            'description' : 'Returns list of reservation for specific profile.'
        },
        {
            'Endpoint' : 'trips/<trip_id>/<e_Wallet>/reservation',
            'method' : 'PUT',
            'body' : {
                'seatNum': "Integer|Required",
                'for i=0 to seatNum do:'
                'seat_name_i': "String|Required",
                'seat_birthday_i': "String|Required",
                'seat_gender_i': "String|Required",
                },
            'description' : 'Make new reservation for one user or more.'
        },
        {
            'Endpoint' : '/search',
            'method' : 'POST',
            'body' : {
                'source': "String",
                'destination': "String",
                'date': "date",
                'time': "time"
                },
            'description' : 'Search for specific trip.'
        },
        {
            'Endpoint' : '/changePhone/<e_Wallet>',
            'method' : 'PUT',
            'body' : {
                'newPhone': "String"
                },
            'description' : 'Change phone number.'
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
    birthday = data['birthday']
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
    new_profile = Profile(user = my_user,first_name = my_user.first_name, last_name = my_user.last_name, gender = gender, phone = phone, birthday = birthday, e_Wallet = e_wallet)
    new_profile.save()

    return Response('Account created successfully!')
    

  return Response('Nothing!')     

@api_view(['POST'])
def admin_sign_up(request):
  if request.method == "POST":
    data = request.data

    first_name = data['first_name']
    last_name = data['last_name']
    birthday = data['birthday']
    phone = data['phone']
    gender = data['gender']
    password = data['password']
    password_confirm = data['password_confirm']

    is_Admin = data['is_Admin']
    is_Charger = data['is_Charger']
    balance = data['balance']

    if int(balance) < 0:
        return Response('Can not insert negative balance!')

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
    new_profile = Profile(user = my_user, first_name = my_user.first_name, last_name = my_user.last_name, gender = gender, phone = phone, birthday = birthday, e_Wallet = e_wallet)
    new_profile.is_Admin = is_Admin
    new_profile.is_Charger = is_Charger
    new_profile.balance = int(balance)
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
        prof = Profile.objects.get(user = user)
        serializer = ProfileSerializer(prof, many=False)
        return Response(serializer.data)

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

@api_view(['GET'])
def getTrip(request, tid):
    trip = Trip.objects.get(id = tid)
    serializer = TripSerializer(trip, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getMyTrips(request, e_wallet):
    profile = Profile.objects.get(e_Wallet = e_wallet)
    reservations = Reservation.objects.filter(phone = profile.phone)
    serializer = ReservationSerializer(reservations, many=True)
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
    else:
        return Response('The form is invalid!')
        
    

@api_view(['DELETE'])
def removeTrip(request, tid):
    Trip.objects.get(id = tid).delete() 
    return Response('Trip deleted successfully!')


@api_view(['POST'])
def search(request):
    data = request.data
    source = data['source']
    destination = data['destination']
    date = data['date']
    time = data['time']
    if Trip.objects.filter(source = source, destination = destination, date = date, trip_Time = time).exists():
        trips = Trip.objects.filter(source = source, destination = destination, date = date, trip_Time = time)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    return Response('No results!')

@api_view(['PUT'])
def takePlace(request, tid, e_wallet):
    profile = Profile.objects.get(e_Wallet = e_wallet)
    try:
        trip = Trip.objects.get(id = tid)
    except Trip.DoesNotExist:
        return Response('Trip is not exists!')
    if trip.capacity <= trip.counter:
        return Response('The bus is full!')

    data = request.data
    seat = data['seatNum']
    seatINT = int(seat)

    if seatINT <= trip.capacity:
        total = seatINT * trip.cost
        if total <= profile.balance:
            line = ''
            for i in range(seatINT):
                name = birthday = gender = ''
                next_name = 'seat_name_' + str(i)
                next_birthday = 'seat_birthday_' + str(i)
                next_gender = 'seat_gender_' + str(i)
                try:
                    name = data[next_name]
                    birthday = data[next_birthday]
                    gender = data[next_gender]
                except Exception as e:
                    return Response('There is something wrong with the input fields!')
                line += name + ' | ' + birthday + ' | ' + gender + '\n'
                line += '------------------------------\n'
                
                # try:
                #     users.append(Profile.objects.get(phone = next_phone))
                # except Profile.DoesNotExist:
                #     return Response('There is a user who does not exist!')
            
            next_reservation = Reservation(desc = line, trip = trip, phone = profile.phone, cost = total)
            next_reservation.save()

            profile.balance -= total
            profile.save()
            trip.counter += seatINT
            trip.save()
            return Response('Reservation successfully done.')
        else:
            return Response('No enouph money!')
    else:
        return Response('No enough space!')
        



@api_view(['PUT'])
def charge(request, from_Wallet):
    data = request.data

    forUser_Wallet = data['forUser_Wallet']
    if Profile.objects.filter(e_Wallet = forUser_Wallet).exists():
        for_profile = Profile.objects.get(e_Wallet = forUser_Wallet)
        from_profile = Profile.objects.get(e_Wallet = from_Wallet)
        if from_profile.is_Charger:
            amount = data['amount']
            amountINT = int(amount)
            if from_profile.balance >= amountINT:
                for_profile.balance += amountINT
                from_profile.balance -= amountINT
                from_profile.save()
                for_profile.save()
                return Response('Successfully charged!')
            else:
                return Response('No enouph money!')
        else:
            return Response('The profile is not charger!')
    else:
        return Response('The client is not exists!')

@api_view(['PUT'])
def change_phone(request, e_wallet):
    data = request.data

    newPhone = data['newPhone']
    my_profile = Profile.objects.get(e_Wallet = e_wallet)
    my_profile.phone = newPhone
    my_profile.user.username = newPhone
    my_profile.save()
    return Response('Phone changed successfully.')


