from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MetadataViewSet



urlpatterns = [
    path('', home, name='home'),  # Root path of the app
    path('vehicle_probelm_submision', vehicle, name='vehicle'),
    path('job_shop_probelm_subision', job_shop, name='job-shop'),
    path('problem_submission/<str:problem_name>/', submit_problem, name='submit_problem'),
    path('metadata/', MetadataViewSet.as_view({'get': 'list'}), name='metadata-list'),
    path('metadata/delete/', MetadataViewSet.as_view({
        'delete': 'destroy',
    }), name='metadata-detail'),
    # Add more paths as needed
]
