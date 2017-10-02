from __future__ import unicode_literals

from django.db import models
# Create your models here.


class Reminder(models.Model):
    '''
    id user_id reminder date vald_flag
    '''
    user_id=models.CharField(max_length=50)
    reminder=models.TextField()
    date=models.DateField(auto_now=True)
    vald_flag=models.BooleanField()


class Last_command(models.Model):
    user_id = models.CharField(max_length=50,primary_key=True)
    command=models.CharField(max_length=100)
