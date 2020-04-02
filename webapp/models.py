from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class AffinityGroupView(models.Model):
    IP = models.CharField(max_length=40)
    port = models.CharField(max_length=5)
    rtt = models.FloatField(validators=[MinValueValidator(0.0)])
    heartbeatCount = models.IntegerField(validators=[MinValueValidator(0)])
    timestamp = models.IntegerField(default=0, validators=[MinValueValidator(0)])

class Contact(models.Model):
    groupID = models.CharField(max_length=40)
    IP = models.CharField(max_length=40)
    port = models.CharField(max_length=5)
    rtt = models.FloatField(validators=[MinValueValidator(0.0)])
    heartbeatCount = models.IntegerField(validators=[MinValueValidator(0)])
    timestamp = models.IntegerField(default=0, validators=[MinValueValidator(0)])

class Filetuple(models.Model):
    fileName = models.CharField(max_length=100)
    IP = models.CharField(max_length=40)
    port = models.CharField(max_length=5)
    heartbeatCount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    timestamp = models.IntegerField(default=0, validators=[MinValueValidator(0)])

class Counter(models.Model):
    name = models.CharField(max_length=40)
    count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
