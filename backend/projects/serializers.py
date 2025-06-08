from rest_framework import serializers
from .models import Project
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    director = UserSerializer(read_only=True)
    manager = UserSerializer(read_only=True)
    manager_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='manager'), source='manager', write_only=True, required=False
    )

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'director', 'manager', 'manager_id', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['director'] = user
        return super().create(validated_data)
