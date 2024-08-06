from django.urls import path, include
from .views import InfoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', InfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]