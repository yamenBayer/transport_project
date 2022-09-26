from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.BooleanField()
    phone = models.CharField(max_length=10, unique=True)
    public_Number = models.CharField(max_length=11, unique=True)
    e_Wallet = models.CharField(max_length=10, unique=True)
    is_Admin = models.BooleanField(default=False)
    is_Charger = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username    




class Trip(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField(default=datetime.now)
    trip_Time = models.TimeField(auto_now=False, auto_now_add=False)
    is_Vip = models.BooleanField(default=False)
    cost = models.IntegerField(default=0)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    capacity = models.IntegerField(default=35)
    counter = models.IntegerField(default=0)
    
    updated = models.DateTimeField(auto_now=True)
    cretaed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class meta:
        ordering = ['-updated']


class Reservation(models.Model):
    owner_name = models.CharField(max_length=100)
    trip = models.ForeignKey(Trip, related_name='trip' , on_delete= models.CASCADE)
    phone = models.CharField(max_length=10)
    cost = models.IntegerField()

    def __str__(self):
        return self.owner_name

    class meta:
        ordering = ['updated']

    


