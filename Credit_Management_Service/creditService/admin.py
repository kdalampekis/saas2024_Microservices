# Register your models here.
from django.contrib import admin
from .models import CreditTransaction

@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'credits', 'created_at')
    search_fields = ('user_id',)
