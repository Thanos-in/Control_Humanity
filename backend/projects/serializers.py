from rest_framework import serializers
from .models import Project, Module
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from tasks.serializers import TaskSerializer

User = get_user_model()

class ModuleSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'name', 'tasks']

class ProjectSerializer(serializers.ModelSerializer):
    director = UserSerializer(read_only=True)
    manager = UserSerializer(read_only=True)
    manager_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='manager'), source='manager', write_only=True, required=False
    )
    modules = ModuleSerializer(many=True, read_only=True)
    period = serializers.SerializerMethodField()
    is_archived = serializers.BooleanField()
    
    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description',
            'director', 'manager', 'period',
            'manager_id', 'start_date', 'modules', 'image', 'end_date', 'is_archived'
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['director'] = user
        return super().create(validated_data)

    def get_period(self, obj): 
        if obj.end_date:
            return f"{obj.start_date.strftime('%d.%m.%Y')} — {obj.end_date.strftime('%d.%m.%Y')}"
        return f"{obj.start_date.strftime('%d.%m.%Y')}"

