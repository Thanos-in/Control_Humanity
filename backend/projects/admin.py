from django.contrib import admin
from .models import Project
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'director', 'manager', 'created_at', 'data_input')  
    list_filter = ('created_at', 'director', 'manager')  
    search_fields = ('name', 'description', 'director__username', 'manager__username')
    autocomplete_fields = ('director', 'manager')  

    date_hierarchy = 'created_at'
    list_per_page = 25
    list_select_related = ('director', 'manager')

# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('name', 'director', 'manager', 'created_at')
#     list_filter = ('created_at', 'director', 'manager')
#     search_fields = ('name', 'description', 'director__username', 'manager__username')
#     autocomplete_fields = ('director', 'manager')
