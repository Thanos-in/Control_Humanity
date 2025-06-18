from rest_framework import viewsets, permissions
from .models import Project, Module
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .serializers import ProjectSerializer, ModuleSerializer
from .permissions import IsDirector
from rest_framework.response import Response

class ProjectViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == 'archive':
            return Project.objects.all()  
        return Project.objects.filter(is_archived=False)
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsDirector()]
        else:
            return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(director=self.request.user)
        
    @action(detail=True, methods=['patch'], url_path='archive')
    def archive(self, request, pk=None):
        project = self.get_object()
        is_archived = request.data.get('is_archived')
        if is_archived is None:
            return Response({'detail': 'is_archived required'}, status=status.HTTP_400_BAD_REQUEST)
        project.is_archived = is_archived
        project.save()
        serializer = self.get_serializer(project)
        return Response(serializer.data)    

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated()]

    # При желании можно переопределить методы list/create/update/destroy
    # для кастомной логики. Например:
    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)