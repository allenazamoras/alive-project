from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session
from .models import Appeal
from userprofile.models import User

# Register your models here.


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Appeal)
admin.site.register(User, UserAdmin)
admin.site.register(Session, SessionAdmin)
