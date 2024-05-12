from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),  # Root path of the app
    path('solve', index, name='index'),
    path('solve-vrp/', solve_vrp, name='solve-vrp')
    # Add more paths as needed
]
