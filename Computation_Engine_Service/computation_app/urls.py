from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),  # Root path of the app
    path('solve', index, name='index'),
    path('solve-vrp/', solve_vrp, name='solve-vrp'),

    path('queens/', nqueens_api, name='n-queens'),
    path('bin_packing/', binpacking_api, name='bin-packing'),
    path('linear_programming/', linear_programming_api, name='linear-programming'),
    path('job_shop/', job_shop_api, name='job_shop_api'),
    path('multiple_knapsack/', mkp_api, name='multiple-knapsack'),
    path('max_flow/', max_flow_api, name='max_flow'),
    path('lin_sum_assignment/', lin_sum_assignment_api, name='lin_sum_assignment'),
    # Add more paths as needed

    path('sent_data/', sent_data, name='sent_data'),
]