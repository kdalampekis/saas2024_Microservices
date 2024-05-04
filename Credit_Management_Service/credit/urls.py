from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from creditService.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('credits/balance/<int:user_id>/', GetBalanceView.as_view(), name='get-balance'),
    path('credits/purchase/', PurchaseCreditsView.as_view(), name='purchase-credits'),
]

""""
Για να καλέσετε το credits/purchase/ πρέπει να δώσετε
στο request (ως body) ένα JSON της μορφής:

{
    "user_id": 10,
    "credits": 2000
}

Το credits είναι δεκαδικό μέχρι 2 ψηψία και το id ακέραιο
""""