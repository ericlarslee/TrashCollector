from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404, redirect
from .models import Customer
from django.forms import ModelForm
# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'user', 'street', 'city', 'zipcode', 'specific_date', 'pickup_day', 'user', 'account_status', 'subtotal']


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
            if customer.user_id == user.pk:
                customer = Customer.objects.get(user=user.id)
                context = {
                    'customer': customer
                }
                print(customer)
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
        pickup_day = request.POST.get('pickup_day')
        new_customer = Customer(name=name, user=user, street=street, city=city, zipcode=zipcode,
                                account_status=True, pickup_day=pickup_day, subtotal=0)
        new_customer.save()
        new_customer.clean_fields('specific_date')
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/create.html')


def update_account_info(request):
    user = request.user
    customer = get_object_or_404(Customer, user_id=user.pk)
    form = CustomerForm(request.POST or None, instance=customer)
    form.fields.pop('specific_date')
    form.fields.pop('user')
    form.fields.pop('subtotal')
    form.fields.pop('account_status')
    form.fields.pop('pickup_day')
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('customers:index'))
    context ={
        'form': form,
        'customer': customer
    }
    return render(request, 'customers/update_account.html', context)

def update_account_status(request):
    user = request.user
    customer = get_object_or_404(Customer, user_id=user.pk)
    form = CustomerForm(request.POST or None, instance=customer)
    form.fields.pop('specific_date')
    form.fields.pop('user')
    form.fields.pop('subtotal')
    form.fields.pop('account_status')
    form.fields.pop('pickup_day')
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('customers:index'))
    context ={
        'form': form,
        'customer': customer
    }
    return render(request, 'customers/update_account.html', context)
