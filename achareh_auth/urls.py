from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.common.urls import router as common_router
from applications.user.urls import router as user_router

router = DefaultRouter()
router.registry.extend(common_router.registry)
router.registry.extend(user_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
