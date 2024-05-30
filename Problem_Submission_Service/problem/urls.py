from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from problemService.views import *

# Initialize the default router
router = DefaultRouter()

# Register MetadataViewSet with the router
router.register(r'metadata', MetadataViewSet, basename='metadata')

urlpatterns = [
    path('', include(router.urls)),    # Include router URL
    path('admin/', admin.site.urls),
    path('initialize_solver_models/', initialize_solver_models, name='initialize_solver_models'),    # adds the solver_models into the database
    path('solver-models/<str:solver_name>/create-metadata/', MetadataCreateView.as_view(), name='metadata-create'),    # inserts a new metadata, with its inputs, into the database
    path('submit_problem/<int:sub_id>/', submit_problem, name='submit_problem'),    # sends the submission <int:id> for computing
    path('change_metadata_status/<int:sub_id>/', change_metadata_status, name='change_metadata_status'),     # changes a metadata status to 'executed'
    
    path('vehicle_problem_submission/', vehicle, name='vehicle'),
]

# Note: No need to manually define the 'list' or 'delete' for Metadata as the router handles it.

"""
Για να βαλεις στη βαση ενα καινουριο submission θελεις ενα url της μορφης:

http://localhost:8003/solver-models/vrp/create-metadata/ (αυτο αφορα το μοντελο με name=vrp)

και του δινεις ενα body της μορφης:
{
    "username": "sere",
    "credit_cost": "20"
}

Στο frontend θα συσχετισετε τα προβληματα με τα αντιστοιχα credits τους, οποτε εχοντας το id στο url
θα ξερετε και το κοστος για να το περασετε στο body.
"""