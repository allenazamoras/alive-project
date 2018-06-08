from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session
from livestream.models import Appeal, Rating, Report, Notification
from livestream.models import ApprovalRequest
from userprofile.models import User

# Register your models here.


admin.site.register(Appeal)
admin.site.register(ApprovalRequest)
admin.site.register(Rating)
admin.site.register(Report)
admin.site.register(Notification)
admin.site.register(User)
