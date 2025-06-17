from django.contrib import admin
from .models import Project, Module
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'director', 'manager', 'start_date', 'end_date')  
    list_filter = ('start_date', 'director', 'manager')  
    search_fields = ('name', 'description', 'director__username', 'manager__username')
    autocomplete_fields = ('director', 'manager')  

    date_hierarchy = 'start_date'
    list_per_page = 25
    list_select_related = ('director', 'manager')
    
admin.site.register(Module)    