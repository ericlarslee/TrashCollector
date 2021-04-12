from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from .models import Employee
from django.apps import apps
from datetime import date
import calendar
from django.forms import ModelForm
from django.contrib.auth.models import Group


# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

 #this index seems redundant and unneeded compared to the simple import
def index(request):
    # Get the Customer model from the other app, it can now be used to query the db
    user = request.user
    employees = Employee.objects.all()
    if len(employees) == 0:
        return render(request, 'employees/update_account.html')
    else:
        for employee in employees:
            if employee.user_id == user.pk:
                employee = Employee.objects.get(user=user.id)
                if employee.zipcode is None:
                    return render(request, 'employees/update_account.html')
                else:
                    Customer = apps.get_model('customers.Customer')
                    customers = Customer.objects.all()
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
                        'customers': customer_list,
                        'employee': employee
                    }
                    return render(request, 'employees/index.html', context)


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'zipcode']
        labels = {
            'name': 'Name',
            'zipcode': 'Zipcode'
        }


def update(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        zipcode = request.POST.get('zipcode')
        new_employee = Employee(name=name, user=user, zipcode=zipcode)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'employee': employee
        }
        return render(request, 'employees/update_account.html', context)


def day_name():
    today_day = date.today()
    today_day = calendar.day_name[today_day.weekday()]
    return today_day


def today_customer_list(request):
    customer_group = Group.objects.get(name="Customers")
    customers = customer_group.user_set_all()
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
    customer_group = Group.objects.get(name="Customers")
    customers = customer_group.user_set_all()
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
