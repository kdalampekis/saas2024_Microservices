from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from problemService.views import *

# Initialize the default router
router = DefaultRouter()

# Register MetadataViewSet with the router
router.register(r'metadata', MetadataViewSet, basename='metadata')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),    # Include router URL
    path('problem/', include('problemService.urls'))
]

# Note: No need to manually define the 'list' or 'delete' for Metadata as the router handles it.