from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from django.forms import ModelForm
# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'street', 'city', 'zipcode']

def index(request):
    # get the logged in user within any view function
    user = request.user

    all_customers = Customer.objects.all()

    for customer in all_customers:
        if customer.user.is_authenticated:
            print(user)
            break
    else:
        create(request)

    # This will be useful while creating a customer to assign the logged in user as the user foreign key
    # Will also be useful in any function that needs

    #if user does not exist

    return render(request, 'customers/index.html')

def create(request):
    form = CustomerForm(request.POST or None)

    context = {
        'form': form
    }

    if form.is_valid():
        form.save()
        return redirect('customers:index')
    else:
        return render(request, 'customers/index.html', context)
