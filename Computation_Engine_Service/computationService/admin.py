from django.contrib import admin
from .models import *

class VRPAdmin(admin.ModelAdmin):
    list_display = ('objective_id', 'number_of_vehicles', 'maximum_distance')
    search_fields = ('objective_id', 'number_of_vehicles')
    list_filter = ('number_of_vehicles', 'maximum_distance')
    ordering = ('objective_id',)

class ResultsAdmin(admin.ModelAdmin):
    list_display = ('submission_id', 'problem_name', 'time_taken', 'timestamp')
    search_fields = ('problem_name',)
    list_filter = ('timestamp',)
    ordering = ('submission_id',)


admin.site.register(Results, ResultsAdmin)
admin.site.register(VRP, VRPAdmin)
