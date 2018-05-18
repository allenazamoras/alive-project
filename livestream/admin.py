from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Appeal
from UserProfile.models import User

# Register your models here.

admin.site.register(Appeal)
admin.site.register(User, UserAdmin)
