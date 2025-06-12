from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from django.db.models import Q 
from accounts.serializers import UserSerializer

User = get_user_model() 

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'chat_room', 'sender', 'content', 'timestamp')
        read_only_fields = ('sender', 'timestamp')

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        source='participants'
    )
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ('id', 'participants', 'participant_ids', 'created_at', 'last_message', 'unread_count')

    def get_last_message(self, obj):
        last = obj.messages.last()
        if last:
            return MessageSerializer(last).data
        return None
    
    def get_unread_count(self, obj):
        user = self.context['request'].user

        return obj.messages.filter(~Q(read_by=user)).count()
