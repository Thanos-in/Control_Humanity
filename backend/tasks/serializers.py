from rest_framework import serializers
from .models import Task, Status
from accounts.serializers import UserSerializer
from projects.serializers import ProjectSerializer
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'name', 'order', 'project', 'color')

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task, Status, Project
from .serializers import UserSerializer, StatusSerializer, ProjectSerializer

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    # Read-only nested serializers
    assigned_to   = UserSerializer(read_only=True)
    status        = StatusSerializer(read_only=True)
    project       = ProjectSerializer(read_only=True)

    # Write-only PK fields
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='employee'),
        source='assigned_to',
        write_only=True,
        required=False
    )
    status_id      = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(),
        source='status',
        write_only=True
    )
    project_id     = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source='project',
        write_only=True
    )

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description',
            'project',      'project_id',
            'assigned_to',  'assigned_to_id',
            'status',       'status_id',
            'created_by',   'created_at',
            'updated_at',   'due_date',
            'color',
        )
        read_only_fields = ('created_by',)

    def validate_assigned_to(self, user):
        """Foydalanuvchi faqat role='employee' bo‘lsa ruxsat beramiz."""
        if user and user.role != 'employee':
            raise serializers.ValidationError("Назначить можно только сотрудника.")
        return user

    def create(self, validated_data):
        # Avtomatik created_by qo‘shish
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # assigned_to yozilsa, yangilab qo‘yish
        if 'assigned_to' in validated_data:
            instance.assigned_to = validated_data.pop('assigned_to')
        return super().update(instance, validated_data)

