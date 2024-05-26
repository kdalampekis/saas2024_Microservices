from django.contrib import admin
from django.urls import path, include
from creditService.views import GetBalanceView, PurchaseCreditsView, SpendCreditsView, InitializeUserCreditBalanceView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('credits/balance/<str:user_id>/', GetBalanceView.as_view(), name='get-balance'),
    path('credits/purchase/', PurchaseCreditsView.as_view(), name='purchase-credits'),
    path('credits/<str:user_id>/spend/', SpendCreditsView.as_view(), name='update-credits'),
    path('credits/initialize_user_credits/', InitializeUserCreditBalanceView.as_view(), name='initialize_user_credits'),
]

"""
Για να καλέσετε το credits/purchase/ πρέπει να δώσετε
στο request (ως body) ένα JSON της μορφής:

{
    "user_id": 10,
    "credits": 2000
}

Το credits είναι δεκαδικό μέχρι 2 ψηψία και το id ακέραιο


Για να καλέσετε το credits/<int:user_id>/spend/ πρέπει να δώσετε
το id στο url και στο request (ως body) ένα JSON της μορφής:

{
    "credits": 2000
}
"""