from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps
from datetime import date
import calendar
from trash_collector.customers.models import Customer


# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

 #this index seems redundant and unneeded compared to the simple import
def index(request):
    # Get the Customer model from the other app, it can now be used to query the db
    Customer = apps.get_model('customers.Customer')
    return render(request, 'employees/index.html')


def day_name():
    today_day = date.today()
    today_day = calendar.day_name[today_day.weekday()]
    return today_day


def today_customer_list(request):
    customers = Customer.objects.all()
    employee = request.user
    customer_list = []
    today = day_name()
    for customer in customers:
        if customer.pickup_day == today:
            customer_list.append(customer)
    for customer in customer_list:
        if customer.zipcode != employee.zipcode:
            customer_list.remove(customer)
        if not customer.account_status:
            customer_list.remove(customer)
    context = {
        'customers': customer_list
    }
    return render(request, 'employees/index.html', context)


def daily_customer_list(request):
    customers = Customer.objects.all()
    employee = request.user
    customer_today_list = []
    today = day_name()
    for customer in customers:
        if customer.pickup_day == today:
            customer_today_list.append(customer)
    if customer.zipcode != employee.zipcode:
        customer_today_list.remove(customer)
    context = {
        'customers': customer_today_list
    }
    return render(request, 'employees/index.html', context)
