from django.contrib import admin
from .models import ChatRoom, Message
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'participants_list', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('participants__username',)
    filter_horizontal = ('participants',)
    list_per_page = 20
    
    def participants_list(self, obj):
        return ", ".join([u.get_full_name() or u.username for u in obj.participants.all()])
    participants_list.short_description = 'Ishtirokchilar'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_room', 'sender', 'content_preview', 'timestamp')
    list_filter = ('timestamp', 'chat_room')
    search_fields = ('content', 'sender__username', 'sender__email')
    date_hierarchy = 'timestamp'
    list_select_related = ('chat_room', 'sender')
    raw_id_fields = ('sender',)
    list_per_page = 30
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Xabar matni'


# @admin.register(ChatRoom)
# class ChatRoomAdmin(admin.ModelAdmin):
#     list_display = ('id', 'participants_list', 'created_at')
#     list_filter = ('created_at',)
#     search_fields = ('participants__username',)
#     filter_horizontal = ('participants',)
    
#     def participants_list(self, obj):
#         return ", ".join([u.username for u in obj.participants.all()])
#     participants_list.short_description = 'Participants'

# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'chat_room', 'sender', 'content_preview', 'timestamp')
#     list_filter = ('timestamp', 'chat_room')
#     search_fields = ('content', 'sender__username')
#     date_hierarchy = 'timestamp'
    
#     def content_preview(self, obj):
#         return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
#     content_preview.short_description = 'Content'