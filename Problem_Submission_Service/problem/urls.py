from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from problemService.views import *
# from .views import MetadataViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('solver-models/<int:model_id>/create-metadata/', MetadataCreateView.as_view(), name='metadata-create'),
    path('', home, name='home'),  # Root path of the app #
    path('vehicle_probelm_submision', vehicle, name='vehicle'), #
    path('job_shop_probelm_subision', job_shop, name='job-shop'), #
    path('problem_submission/<str:problem_name>/', submit_problem, name='submit_problem'),
    path('metadata/', MetadataViewSet.as_view({'get': 'list'}), name='metadata-list'),
    path('metadata/delete/', MetadataViewSet.as_view({
        'delete': 'destroy',
    }), name='metadata-detail'),
]


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
