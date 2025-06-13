from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    

class AllProfileView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    lookup_field     = 'pk'
    lookup_url_kwarg = 'userId'

    def delete(self, request, *args, **kwargs):

        if request.user.role == 'employee':
            return Response(
                {"detail": "Вы не можете удалять!."},
                status=status.HTTP_403_FORBIDDEN
            )

        user_to_delete = self.get_object()
        if user_to_delete.is_superuser:
            return Response(
                {"detail": "Вы не можете удалять!."},
                status=status.HTTP_403_FORBIDDEN
            )
        if user_to_delete == request.user:
            return Response(
                {"detail": "Вы не можете удалять!."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().delete(request, *args, **kwargs)


class ManagerListView(generics.ListAPIView):
    queryset = User.objects.filter(role='manager')
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(role='employee')
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    
class AllUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer