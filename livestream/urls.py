from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'sessions', views.SessionViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'tokens', views.ClientTokenViewSet)

app_name = 'livestream'
urlpatterns = [
	# path('', views.IndexView.as_view(), name='index')
]

urlpatterns += router.urls
