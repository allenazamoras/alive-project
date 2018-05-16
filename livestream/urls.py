from django.urls import path
from rest_framework import routers
from . import views


app_name = 'livestream'

router = routers.DefaultRouter()
router.register(r'request', views.RequestViewSet, base_name='request')
router.register(r'user', views.UserViewSet, base_name='user')
# router.register(r'token', views.ClientTokenViewSet, base_name='token')

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    # It worked I have no idea how ref: livestream/index.html
    path('request/<int:pk>', views.RequestDetailView.as_view(), name='stream'),
]

urlpatterns += router.urls
