from django.urls import path
from rest_framework import routers
from . import views


app_name = 'livestream'

router = routers.DefaultRouter()
router.register(r'request', views.AppealViewSet, base_name='request')
router.register(r'pending', views.ApprovalRequestViewSet, base_name='pending')
router.register(r'category', views.CategoryViewSet, base_name='category')

urlpatterns = [
]

urlpatterns += router.urls
