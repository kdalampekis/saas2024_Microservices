from django.urls import path
from problemService.views import *


urlpatterns = [
    path('initialize_models/', initialize_models),    # adds the solver_models into the database
    path('create-metadata/<str:solver_name>/', MetadataCreateView.as_view()),    # inserts a new metadata and input instance into the database
    path('submit_problem/<int:sub_id>/', submit_problem),    # sends the submission <int:id> for computing
    path('change_status/<int:sub_id>/', change_status),     # changes a metadata status to 'executed'
    
    path('vehicle_problem_submission/', vehicle),   # test html page for vrp
    path('job_shop_submission', job_shop)   # test html page job_shop
]


"""
To create a new metadata instance for problem <str:solver_name> go to url:
http://localhost:8003/problem/create-metadata/<str:solver_name>/

To run the problem based on the metadata and the input go to url:
http://localhost:8003/problem/submit_problem/<int:sub_id>/
"""