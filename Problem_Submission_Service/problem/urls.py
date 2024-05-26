from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from problemService.views import MetadataCreateView, home, vehicle, job_shop, submit_problem, MetadataViewSet

# Initialize the default router
router = DefaultRouter()

# Register MetadataViewSet with the router
router.register(r'metadata', MetadataViewSet, basename='metadata')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include router URLs
    # path('', include(router.urls)),
    # Custom paths
    # path('', home, name='home'),  # Root path of the app
    path('vehicle_problem_submission/', vehicle, name='vehicle'),  # Corrected typo in the path
    path('job_shop_problem_submission/', job_shop, name='job-shop'),  # Corrected typo in the path
    path('problem_submission/<str:problem_name>/', submit_problem, name='submit_problem'),
    path('solver-models/<int:model_id>/create-metadata/', MetadataCreateView.as_view(), name='metadata-create'),
]

# Note: No need to manually define the 'list' or 'delete' for Metadata as the router handles it.

"""
Για να βαλεις στη βαση ενα καινουριο submission θελεις ενα url της μορφης:

http://localhost:8003/solver-models/1/create-metadata/ (αυτο αφορα το μοντελο με id=1)

και του δινεις ενα body της μορφης:
{
    "username": "sere",
}

Στο frontend θα συσχετισετε τα προβληματα με τα αντιστοιχα credits τους, οποτε εχοντας το id στο url
θα ξερετε και το κοστος για να το περασετε στο body.
"""
