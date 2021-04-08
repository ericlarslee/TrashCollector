from django.db import models

# Create your models here.

# TODO: Create an Employee model with properties required by the user stories


class Employee(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', default=0, on_delete=models.CASCADE)
    zipcode = models.IntegerField(default=None)

