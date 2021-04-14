from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse, get_object_or_404, redirect
from .models import Customer
from django import forms
from datetime import datetime,date,timedelta
from django.forms import ModelForm, SelectDateWidget
from datetime import date


# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'user', 'street', 'city', 'zipcode', 'specific_date', 'pickup_day', 'user',
                  'account_status', 'suspend_start', 'suspend_end']
        labels = {
            'name': 'Name',
            'street': 'Street Address',
            'city': 'City',
            'zipcode': 'Zip Code',
            'suspend_end': 'Suspend End',
            'suspend_start': 'Suspend Start'

        }
        widgets = {
            'suspend_start': SelectDateWidget(years=range(2021, 2021)),
            'suspend_end': SelectDateWidget(years=range(2021, 2021))
        }


class CustomerSuspendForm(forms.Form):
    today = date.today()
    max_date = today + timedelta(days=90)
    start_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'min': today, 'max': max_date}),
        label='Start Date')
    end_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'min': today, 'max': max_date}),
        label=' End Date ')


def index(request):
    # get the logged in user within any view function
    user = request.user
    customers = Customer.objects.all()

    if len(customers) == 0:
        return render(request, 'customers/index.html')
    else:
        for customer in customers:
            if customer.user_id == user.pk:
                customer = Customer.objects.get(user=user.id)
                context = {
                    'customer': customer
                }

                return render(request, 'customers/index.html', context)

        else:
            return render(request, 'customers/index.html')


def create(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')
        new_customer = Customer(name=name, user=user, street=street, city=city, zipcode=zipcode,
                                account_status=True, pickup_day='N/A')
        new_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/create.html')


def update_account_info(request):
    user = request.user
    customer = get_object_or_404(Customer, user_id=user.pk)
    form = CustomerForm(request.POST or None, instance=customer)
    form.fields.pop('specific_date')
    form.fields.pop('user')
    form.fields.pop('account_status')
    form.fields.pop('pickup_day')
    form.fields.pop('suspend_start')
    form.fields.pop('suspend_end')
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('customers:index'))
    context ={
        'form': form,
        'customer': customer
    }
    return render(request, 'customers/update_account.html', context)


def update_account_status(request):
    customers = Customer.objects.all()
    today_date = date.today()
    user = request.user
    customer = Customer.objects.get(user=user.id)
    form = CustomerSuspendForm(request.POST or None)

    context_main = {
        'customer': customer,
        'form': form
    }

    if form.is_valid():
        customer.suspend_start = form.cleaned_data.get('start_date')
        customer.suspend_end = form.cleaned_data.get('end_date')
        if customer.suspend_start <= today_date <= customer.suspend_end:
            customer.account_status = False
            customer.save()
            return redirect('customers:index')
        else:
            customer.account_status = True
            customer.save()
            return redirect('customers:index')

    return render(request, 'customers/account_status.html', context_main)


#Might be able to insert entire function into update account status function

def reactivate_account(request):
    print('Activate!!!')
    user = request.user
    customer = get_object_or_404(Customer, user_id=user.pk)

    context = {
        'customer': customer
    }

    if request.method == 'POST' and 'activate' in request.POST:
        customer.account_status = True
        customer.suspend_start = None
        customer.suspend_end = None
        customer.save()
        return redirect('customers:index')
    else:
        return render(request, 'customers/activate_account.html', context)


def change_pickup_day(request):
    user = request.user
    customer = get_object_or_404(Customer, user_id=user.pk)
    context = {
        'customer': customer
    }
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    if request.method == 'POST':
        customer.pickup_day = request.POST.get('pickup_day')
        customer.specific_date = request.POST.get('specific_date')

        #If not pickup date is selected value will equal 'N/A'
        value = 'N/A'

        if customer.specific_date == '':
            customer.specific_date = None
            if customer.pickup_day == value:
                customer.projected_total = 0
            elif customer.pickup_day in days_of_week:
                customer.projected_total = 35
            customer.save()
        else:
            if customer.pickup_day == value:
                customer.projected_total = 50

            elif customer.pickup_day in days_of_week:
                customer.projected_total = 85

            customer.save()

        return HttpResponseRedirect(reverse('customers:index'), context)
    else:
        return render(request, 'customers/pickup_day.html')
