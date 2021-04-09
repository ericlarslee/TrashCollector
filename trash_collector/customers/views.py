from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from django.forms import ModelForm
# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


def index(request):
    # get the logged in user within any view function
    user = request.user
    print(user)
    # This will be useful while creating a customer to assign the logged in user as the user foreign key
    # Will also be useful in any function that needs
    #if user does not exist
    customers = Customer.objects.all()

    if len(customers) == 0:
        return render(request, 'customers/index.html')
    else:
        for customer in customers:
            if user.pk != customer.user_id:
                return render(request, 'customers/index.html')
        else:
            customer = Customer.objects.get(user=user.id)
            context = {
                'customer': customer
            }
            print(customer)
            return render(request, 'customers/index.html', context)


def create(request):
    form = CustomerForm(request.POST or None)
    context = {
        'form': form
    }

    if form.is_valid():
        form.save()
        return redirect('customers:index')
    else:
        return render(request, 'customers/create.html', context)
