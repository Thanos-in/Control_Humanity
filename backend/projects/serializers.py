
from rest_framework import serializers
from .models import Project, Module
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from tasks.serializers import TaskSerializer

User = get_user_model()

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name', 'project']


class ProjectSerializer(serializers.ModelSerializer):
    director    = UserSerializer(read_only=True)
    manager     = UserSerializer(read_only=True)
    manager_id  = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='manager'),
        source='manager',
        write_only=True,
        required=False
    )
    modules     = ModuleSerializer(many=True, read_only=True)
    tasks       = TaskSerializer(many=True, read_only=True)
    period      = serializers.SerializerMethodField()
    is_archived = serializers.BooleanField()

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description',
            'director', 'manager', 'manager_id',
            'start_date', 'end_date', 'period',
            'is_archived', 'modules', 'tasks',
            'image',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['director'] = user
        return super().create(validated_data)

    def get_period(self, obj):
        if obj.end_date:
            return f"{obj.start_date:%d.%m.%Y} — {obj.end_date:%d.%m.%Y}"
        return f"{obj.start_date:%d.%m.%Y}"



#===============================================>>>>


# from rest_framework import serializers
# from .models import Project, Module
# from accounts.serializers import UserSerializer
# from django.contrib.auth import get_user_model
# from tasks.serializers import TaskSerializer

# User = get_user_model()

# class ModuleSerializer(serializers.ModelSerializer):
#     tasks = TaskSerializer(many=True, read_only=True)
#     project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

#     class Meta:
#         model = Module
#         fields = ['id', 'name', 'project', 'tasks']

# class ProjectSerializer(serializers.ModelSerializer):
#     director = UserSerializer(read_only=True)
#     manager = UserSerializer(read_only=True)
#     manager_id = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.filter(role='manager'), source='manager', write_only=True, required=False
#     )
#     tasks = TaskSerializer(many=True, read_only=True)
#     modules = ModuleSerializer(many=True, read_only=True)
#     module_id = ModuleSerializer(many=True, read_only=True)
#     period = serializers.SerializerMethodField()
#     is_archived = serializers.BooleanField()
    
#     class Meta:
#         model = Project
#         fields = (
#             'id', 'name', 'description',
#             'director', 'manager', 'period',
#             'manager_id', 'start_date', 'modules', 'tasks', 'image', 'end_date', 'is_archived', 'module_id' 
#         )

#     def create(self, validated_data):
#         user = self.context['request'].user
#         validated_data['director'] = user
#         return super().create(validated_data)

#     def get_period(self, obj): 
#         if obj.end_date:
#             return f"{obj.start_date.strftime('%d.%m.%Y')} — {obj.end_date.strftime('%d.%m.%Y')}"
#         return f"{obj.start_date.strftime('%d.%m.%Y')}"

