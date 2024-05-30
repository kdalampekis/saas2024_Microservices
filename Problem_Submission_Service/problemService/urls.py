from django.urls import path
from problemService.views import *


urlpatterns = [
    path('initialize_models/', initialize_models),    # adds the solver_models into the database
    path('create-metadata/<str:solver_name>/', MetadataCreateView.as_view()),    # inserts a new metadata and input instance into the database
    path('submit_problem/<int:sub_id>/', submit_problem),    # sends the submission <int:id> for computing
    path('change_status/<int:sub_id>/', change_status),     # changes a metadata status to 'executed'
    
    path('vehicle_problem_submission/', vehicle, name='vehicle'),
]


"""
Για να βαλεις στη βαση ενα καινουριο submission θελεις ενα url της μορφης:

http://localhost:8003/problem/create-metadata/vrp/ (αυτο αφορα το μοντελο με name=vrp)

και του δινεις ενα body της μορφης:
{
    "username": "sere",
    "credit_cost": "20"
}

Στο frontend θα συσχετισετε τα προβληματα με τα αντιστοιχα credits τους, οποτε εχοντας το id στο url
θα ξερετε και το κοστος για να το περασετε στο body.
"""