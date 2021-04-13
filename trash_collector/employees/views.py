from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from .models import Employee
from django import forms
from django.contrib.admin import widgets
from django.apps import apps
from datetime import date, datetime, timedelta
import calendar
from django.forms import ModelForm


# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'zipcode']
        labels = {
            'name': 'Name',
            'zipcode': 'Zipcode'
        }


class EmployeeDateSelectionForm(forms.Form):
    today = date.today()
    end_date = today + timedelta(days=6)
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'min': today, 'max': end_date}))


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
    employee = Employee.objects.get(user=user.id)
    form = EmployeeDateSelectionForm(request.POST or None)

    context_main = {
        'employee': employee,
        'customers': customers,
        'form': form
    }

    if form.is_valid():
        selected_date = form.cleaned_data.get('date')
        selected_day_name = selected_date.strftime('%A')

        for customer in customers:
            if customer.zipcode == employee.zipcode and customer.account_status is True:
                filtered_date = customers.filter(specific_date=selected_date)
                filtered_day = customers.filter(pickup_day=selected_day_name)
                filtered = filtered_date | filtered_day
                context = {
                    'customers': filtered,
                    'form': form
                }
                return render(request, 'employees/upcoming_pickups.html', context)

    return render(request, 'employees/upcoming_pickups.html', context_main)
