from rest_framework import routers
from django.urls import path, include
from django.conf.urls import url

app_name = 'userprofile'

router = routers.DefaultRouter()

urlpatterns = []

urlpatterns += router.urls
