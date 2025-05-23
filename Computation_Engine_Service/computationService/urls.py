from django.urls import path
from .views import *


urlpatterns = [
    # problem api
    path('vrp/', vrp_api, name='solve-vrp'),
    path('queens/', nqueens_api, name='n-queens'),
    path('bin_packing/', binpacking_api, name='bin-packing'),
    path('linear_programming/', linear_programming_api, name='linear-programming'),
    path('job_shop/', job_shop_api, name='job_shop_api'),
    path('multiple_knapsack/', mkp_api, name='multiple-knapsack'),
    path('max_flow/', max_flow_api, name='max_flow'),
    path('lin_sum_assignment/', lin_sum_assignment_api, name='lin_sum_assignment'),
    # Add more paths for other problems

    # other api
    path('result/<int:sub_id>/', result_detail, name='result_detail'),
    path('delete_result/<int:sub_id>/', delete_result_view, name='delete_result_view'),
    # path('problem_submission/', computation_view, name='computation_view'),
]