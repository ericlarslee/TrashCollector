from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from .models import Employee
from django.apps import apps
from datetime import date, datetime
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
                    today_date = date.today()
                    for customer in customers:
                        if customer.pickup_day == today or customer.specific_date == today_date:
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
        return render(request, 'employees/update_account.html')


def day_name():
    today_day = date.today()
    today_day = calendar.day_name[today_day.weekday()]
    return today_day


def upcoming_pickups(request):
    Customer = apps.get_model('customers.Customer')
    customers = Customer.objects.all()
    user = request.user
    today = date.today()
    employee = Employee.objects.get(user=user.id)
    # filtered = Customer.objects.all().filter(zipcode=employee.zipcode, account_status=True)
    # filtered_list = list(filtered)
    if request.method == 'POST':
        selected_day = request.POST.get('selected_day')
        date_converter = selected_day.strptime( '%Y-%B-%d')
        selected_day_name = calendar.day_name[selected_day.weekday()]
        customer_list = []
        for customer in customers:
            # Check for selected day from employee drop down
            if customer.zipcode == employee.zipcode and customer.account_status is True:
                customer_list.append(customer)
                if customer.pickup_day is not selected_day_name or customer.specific_date is not selected_day:
                    customer_list.remove(customer)
            context = {
                'customers': customer_list,
                'date': today
            }
            return render(request, 'employees/upcoming_pickups.html', context)
    context_main = {
        'employee': employee,
        'customers': customers
    }

    return render(request, 'employees/upcoming_pickups.html', context_main)
