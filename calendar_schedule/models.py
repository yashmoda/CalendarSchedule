from django.contrib.auth.models import User
from django.db import models


class UserData(models.Model):
    name = models.CharField(max_length=255)
    email_id = models.EmailField(unique=True)
    password = models.TextField()


class CalendarData(models.Model):
    user_id = models.ForeignKey(UserData, on_delete=models.PROTECT)
    event_name = models.CharField(max_length=255)
    event_description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    is_deleted = models.BooleanField(default=False)
