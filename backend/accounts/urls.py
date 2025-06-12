from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, AllProfileView, ProfileView, ManagerListView, UserListView, AllUserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profiles/<int:userId>/', AllProfileView.as_view(), name='profile_detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/managers/', ManagerListView.as_view(), name='manager-list'),
    path('users/users/', UserListView.as_view(), name='user-list'),
    path('users/allusers/', AllUserListView.as_view(), name='user-list'),
]
