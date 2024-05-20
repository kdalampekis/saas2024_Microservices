from django.urls import path
from .views import *

urlpatterns = [
    path('get_results/', fetch_data, name='income_data'),
]
