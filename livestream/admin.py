from django.contrib import admin
from livestream.models import Appeal, Rating
from userprofile.models import User

# Register your models here.


admin.site.register(Appeal)
admin.site.register(Rating)
admin.site.register(User)
