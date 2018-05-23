from rest_framework import routers
from django.urls import path, include
from django.conf.urls import url
from userprofile import views

app_name = 'userprofile'

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, base_name='user')

urlpatterns = [
    url(r'^login', views.LoginView.as_view()),
]

urlpatterns += router.urls
