from django.urls import path
from . import views

urlpatterns = [
    path('vehicle_problem/', views.income_data, name='income_data'),
]
