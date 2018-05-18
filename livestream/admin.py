from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Appeal
from userprofile.models import User

# Register your models here.

admin.site.register(Appeal)
admin.site.register(User, UserAdmin)
