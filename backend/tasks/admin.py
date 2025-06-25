from django.contrib import admin
from .models import Status, Task, SimpleTask, TaskMarkedUser
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html

from django.contrib import admin
from django.utils.html import format_html
from .models import Status

class StatusAdmin(admin.ModelAdmin):
    list_display   = ('name', 'project', 'user', 'order', 'color_display')
    list_filter    = ('project',)
    search_fields  = ('name', 'project__name')
    ordering       = ('project', 'order')
    list_per_page  = 20

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['project'].required = False
        return form

    def color_display(self, obj):
        return format_html(
            '<span style="display: inline-block; width: 20px; height: 20px; '
            'background-color: {}; border: 1px solid #ddd;"></span>',
            obj.color
        )
    color_display.short_description = 'Цвет'


# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('title', 'project', 'status', 'assigned_to', 'data_input', 'due_date', 'color_display')  
#     list_filter = ('project', 'status', 'assigned_to', 'created_by')
#     search_fields = ('title', 'description', 'project__name')
#     raw_id_fields = ('project', 'assigned_to', 'created_by')
#     date_hierarchy = 'created_at'
#     ordering = ('-created_at',)
#     list_select_related = ('project', 'status', 'assigned_to', 'created_by')
#     list_per_page = 30
#     readonly_fields = ('color_display',)
       
#     def color_display(self, obj):

#         if obj.status and hasattr(obj.status, 'color'):
#             return format_html(
#                 '<span style="display: inline-block; width: 20px; height: 20px; '
#                 'background-color: {}; border: 1px solid #ddd;"></span>',
#                 obj.status.color  # Access color through status relation
#             )
#         return ""
#     color_display.short_description = 'Цвет'
    
#     fieldsets = (
#         (None, {
#             'fields': ('title', 'description', 'project', 'status',  'color_display')
#         }),
#         ('Назначение', {
#             'fields': ('assigned_to', 'created_by', 'due_date')
#         }),
#     )
    
class TaskMarkedUserInline(admin.TabularInline):
    model = TaskMarkedUser
    extra = 1  # Qo‘shimcha 1 ta bo‘sh qator ko‘rsatadi
    autocomplete_fields = ['user']

class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskMarkedUserInline]
    list_display = ('title', 'assigned_to', 'due_date', 'is_archived')
    search_fields = ['title', 'description']

admin.site.register(Task, TaskAdmin)    
    
    
    
admin.site.register(Status, StatusAdmin)
#admin.site.register(Task) #, TaskAdmin

admin.site.register(SimpleTask)
