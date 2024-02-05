# room_booking/models.py

from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.room_number

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    access_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username
    

class RoomBookingDetail(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.IntegerField()  # Day of the month
    time_slot = models.CharField(max_length=30)
    booked_by_current_user = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.room.room_number} - {self.day} - {self.time_slot}'