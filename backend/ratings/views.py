from rest_framework import viewsets, permissions
from .models import Rating
from .serializers import RatingSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        received = self.request.query_params.get('received')
        if received == 'true':
            return Rating.objects.filter(to_user=user)
        return Rating.objects.filter(from_user=user)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)
