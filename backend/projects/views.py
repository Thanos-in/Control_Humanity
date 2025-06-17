from rest_framework import viewsets, permissions
from .models import Project
from rest_framework.permissions import AllowAny
from .serializers import ProjectSerializer
from .permissions import IsDirector

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsDirector()]
        else:
            return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(director=self.request.user)
