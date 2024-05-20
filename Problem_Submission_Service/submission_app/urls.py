from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),  # Root path of the app
    path('vehicle_probelm_submision', vehicle, name='vehicle'),
    path('job_shop_probelm_subision', job_shop, name='job-shop'),
    path('problem_submission/<str:problem_name>/', submit_problem, name='submit_problem'),
    # Add more paths as needed
]
