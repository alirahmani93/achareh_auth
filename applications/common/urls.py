from rest_framework import routers

from .views import AppViewSet

router = routers.DefaultRouter()

router.register('app', AppViewSet, basename='app')
