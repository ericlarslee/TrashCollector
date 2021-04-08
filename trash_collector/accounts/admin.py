from django.contrib import admin
from .models import User
# Register your models here.

# Registering our custom user in the admin interface
admin.site.register(User)
