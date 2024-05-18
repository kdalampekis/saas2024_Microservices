from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),  # Root path of the app
    path('solve', index, name='index'),
    path('solve-vrp/', solve_vrp, name='solve-vrp'),
    path('api/problem/vehicle', IncomeData.as_view(), name='income_data'),
    path('queens/', nqueens_api, name='n-queens'),
    # Add more paths as needed
]
nqueens_api