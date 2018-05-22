from rest_framework import routers
from . import views

app_name = 'approvalrequest'

router = routers.DefaultRouter()
router.register(r'approvalrequest', views.ApprovalRequestViewSet,
                base_name='approvalrequest')

urlpatterns = []

urlpatterns += router.urls
