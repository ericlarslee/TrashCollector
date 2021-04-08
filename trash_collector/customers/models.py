from django.db import models


# Create your models here.

# TODO: Finish customer model by adding necessary properties to fulfill user stories

class Customer(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', default=0, on_delete=models.CASCADE)
    street = models.CharField(max_length=50, default=None)
    city = models.CharField(max_length=50, default=None)
    zipcode = models.IntegerField(default=None)
    account_status = models.BooleanField(default=True)
    pickup_days = models.CharField(max_length=50, default=None)
    specific_date = models.DateField(default=None)
    subtotal = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name
