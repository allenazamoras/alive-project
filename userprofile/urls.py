from rest_framework import routers
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from userprofile import views

app_name = 'userprofile'

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, base_name='user')
router.register(r'rating', views.RatingViewSet, base_name='rating')
router.register(r'report', views.ReportViewSet, base_name='report')
router.register(r'notification', views.NotificationViewSet,
                base_name='notification')


urlpatterns = [
    url(r'^login', views.Login.as_view()),
    url(r'^search', views.SearchListView.as_view()),

]

urlpatterns += router.urls
