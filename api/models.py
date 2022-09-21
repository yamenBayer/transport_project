from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.BooleanField()
    phone = models.IntegerField(max_length=10)
    public_Number = models.IntegerField(max_length=11)
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
    start_Place = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    members = models.ManyToManyField(Profile, related_name='members',null=True, blank=True)

    
    updated = models.DateTimeField(auto_now=True)
    cretaed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class meta:
        ordering = ['-updated']


