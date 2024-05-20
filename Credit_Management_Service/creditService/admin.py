# Register your models here.
from django.contrib import admin
from .models import *

@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'credits', 'created_at')
    search_fields = ('user_id',)

@admin.register(UserCreditBalance)
class UserCreditBalance(admin.ModelAdmin):
    list_display = ('user_id', 'balance')
    search_fields = ('user_id',)
