from django.contrib import admin
from .models import *


class SolverModelAdmin(admin.ModelAdmin):
    list_display = ('model_id', 'title', 'name', 'notes')
    search_fields = ('title', 'name')
    ordering = ('model_id',)

class MetadataAdmin(admin.ModelAdmin):
    list_display = ('submission_id', 'username', 'date', 'credit_cost', 'model_id', 'is_executed', 'is_ready')
    search_fields = ('username', 'model_id_title')
    list_filter = ('is_executed', 'is_ready', 'date', 'model_id')
    readonly_fields = ('date',)
    
class InputAdmin(admin.ModelAdmin):
    list_display = ('get_submission_id', 'input_file', 'input_data')
    search_fields = ('metadata__username', 'metadata__model_id__title')

    def get_submission_id(self, obj):
        return obj.metadata.submission_id
    get_submission_id.short_description = 'Submission ID'


admin.site.register(SolverModel, SolverModelAdmin)
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(Input, InputAdmin)
