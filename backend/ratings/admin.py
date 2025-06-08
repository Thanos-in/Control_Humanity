from django.contrib import admin
from .models import Rating
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'score_stars', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = (
        'from_user__username', 
        'from_user__email',
        'to_user__username',
        'to_user__email',
        'comment'
    )
    readonly_fields = ('created_at',)
    list_select_related = ('from_user', 'to_user')
    list_per_page = 30
    
    fieldsets = (
        (None, {
            'fields': ('from_user', 'to_user', 'score')
        }),
        ('Qoʻshimcha maʼlumot', {
            'fields': ('comment', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def score_stars(self, obj):
        return format_html(
            '<span style="color: gold;">{}</span>',
            '★' * obj.score + '☆' * (5 - obj.score)
        )
    score_stars.short_description = 'Baholar'


# @admin.register(Rating)
# class RatingAdmin(admin.ModelAdmin):
#     list_display = ('from_user', 'to_user', 'score', 'created_at')
#     list_filter = ('score', 'created_at')
#     search_fields = (
#         'from_user__username', 
#         'from_user__email',
#         'to_user__username',
#         'to_user__email',
#         'comment'
#     )
#     readonly_fields = ('created_at',)
#     fieldsets = (
#         (None, {
#             'fields': ('from_user', 'to_user', 'score')
#         }),
#         ('Additional Information', {
#             'fields': ('comment', 'created_at'),
#             'classes': ('collapse',)
#         }),
#     )