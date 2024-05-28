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
    # Include router URLs
    path('', include(router.urls)),
    path('vehicle_problem_submission/', vehicle, name='vehicle'),  # Corrected typo in the path
    path('job_shop_problem_submission/', job_shop, name='job-shop'),  # Corrected typo in the path
    path('problem_submission/<str:problem_name>/', submit_problem, name='submit_problem'),
    path('solver-models/<str:solver_name>/create-metadata/', MetadataCreateView.as_view(), name='metadata-create'),     # inserts a new metadata into the database
    path('initialize_solver_models/', initialize_solver_models, name='initialize_solver_models'),    # adds the solver_models into the database
    path('change_metadata_status/<int:sub_id>/', change_metadata_status, name='change_metadata_status')     # changes a metadata status to 'executed'
]

# Note: No need to manually define the 'list' or 'delete' for Metadata as the router handles it.

"""
Για να βαλεις στη βαση ενα καινουριο submission θελεις ενα url της μορφης:

http://localhost:8003/solver-models/solve-vrp/create-metadata/ (αυτο αφορα το μοντελο με name=solve-vrp)

και του δινεις ενα body της μορφης:
{
    "username": "sere",
    "credit_cost": "20"
}

Στο frontend θα συσχετισετε τα προβληματα με τα αντιστοιχα credits τους, οποτε εχοντας το id στο url
θα ξερετε και το κοστος για να το περασετε στο body.
"""