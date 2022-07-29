from django.db import models


# Create your models here.
class Customer(models.Model):
    fullname = models.CharField(max_length=60)
    address = models.CharField(max_length=180)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=55)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=55)
    class Meta:
        db_table = "customer"

    # class Meta used to rename data_app_customer to only customer


class Encryption(models.Model):
    data = models.CharField(max_length=80)
    key = models.CharField(max_length=50)
    username = models.CharField(max_length=40)
    receiver = models.CharField(max_length=75)
    enc_data = models.CharField(max_length=295)