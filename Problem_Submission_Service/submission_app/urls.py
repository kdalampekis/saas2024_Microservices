from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),  # Root path of the app
    path('vehicle_probelm_submision', vehicle, name='vehicle'),
    path('job_shop_probelm_submision', job_shop, name='job-shop'),
    # Add more paths as needed
]
