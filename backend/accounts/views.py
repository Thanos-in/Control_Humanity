from rest_framework import generics, permissions
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
    
class AllProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    lookup_field       = 'pk'         
    lookup_url_kwarg   = 'userId'

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