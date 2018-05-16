from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Request, User

# Register your models here.

admin.site.register(Request)
admin.site.register(User, UserAdmin)
