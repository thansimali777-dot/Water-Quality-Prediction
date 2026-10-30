from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#
class user_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    phoneno=models.CharField(max_length=100)

class water_table(models.Model):
    pH=models.CharField(max_length=100)
    Hardness=models.CharField(max_length=100)
    Solids=models.CharField(max_length=100)
    Chloramines=models.CharField(max_length=100)
    Sulfate=models.CharField(max_length=100)
    Potability=models.CharField(max_length=100)
    predictionresult=models.CharField(max_length=100)
    featurecontribution=models.CharField(max_length=100)


class feedback_table(models.Model):
    message=models.CharField(max_length=200)
    reply=models.CharField(max_length=100)

class Complaint_table(models.Model):
    complaint=models.CharField(max_length=100)
    complaintreply=models.CharField(max_length=100)

