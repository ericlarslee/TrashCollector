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
    suspend_start = models.DateField(null=True, blank=True)
    suspend_end = models.DateField(null=True, blank=True)
    pickup_day = models.CharField(max_length=50, blank=True)
    specific_date = models.DateField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=5, decimal_places=2, blank=True)

    def __str__(self):
        return self.name
