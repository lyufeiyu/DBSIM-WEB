from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet,system_status,database_status,application_status,network_status

router = DefaultRouter()
router.register(r'resources', ResourceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('system/', system_status, name='system_status'),
    path('database/', database_status, name='database_status'),
    path('application/', application_status, name='application_status'),
    path('network/', network_status, name='network_status'),
]
