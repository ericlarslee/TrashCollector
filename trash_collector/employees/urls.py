from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the customer user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('update_account/', views.update, name="update"),
    path('upcoming_pickups/', views.upcoming_pickups, name='upcoming_pickups'),
    path('pickup_location/', views.pickup_location, name='pickup_location')
]