from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the customer user stories, add a path for each in urlpatterns

app_name = "customers"
urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name='create_account'),
    path('update_account/', views.update_account_info, name='update_account_info'),
    path('account_status/', views.update_account_status, name='update_account_status'),
    path('pickup_day/', views.change_pickup_day, name='change_pickup_day')

]
