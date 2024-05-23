from django.contrib import admin
from .models import SolverModel, Metadata

class SolverModelAdmin(admin.ModelAdmin):
    list_display = ['model_id', 'title', 'notes']

class MetadataAdmin(admin.ModelAdmin):
    list_display = ['submission_id', 'username', 'date', 'credit_cost', 'problem_type', 'is_ready', 'is_executed']

admin.site.register(SolverModel, SolverModelAdmin)
admin.site.register(Metadata, MetadataAdmin)
