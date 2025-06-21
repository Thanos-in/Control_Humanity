from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        # Ro'yhatga olishga (create) hamma uchun ruxsat
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        # Create uchun RegisterSerializer, boshqalari uchun UserSerializer
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        user_to_delete = self.get_object()

        # 1) employee rolidagi foydalanuvchi hech kimni o'chira olmaydi
        if request.user.role == 'employee':
            return Response(
                {"detail": "Sizda bu amalni bajarish huquqi yoʻq."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 2) superuserni o'chirishga ruxsat yoʻq
        if user_to_delete.is_superuser:
            return Response(
                {"detail": "Superuserni oʻchirib boʻlmaydi."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 3) o'zini o'zi o'chirishga ruxsat yo'q
        if user_to_delete == request.user:
            return Response(
                {"detail": "Oʻzingizni oʻchirib boʻlmaysiz."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Hammasi joyida bo'lsa, odatdagi o'chirishni bajar
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def managers(self, request):
        qs = User.objects.filter(role='manager')

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def employees(self, request):
        qs = User.objects.filter(role='employee')

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class BindTelegramView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        telegram_id = request.data.get("telegram_id")

        if not phone or not telegram_id:
            return Response({"error": "phone va telegram_id talab qilinadi."}, status=400)

        try:
            user = User.objects.get(phone=phone)
            user.telegram_id = telegram_id
            user.save()
            return Response({"message": "Telegram ID muvaffaqiyatli bog‘landi."})
        except User.DoesNotExist:
            return Response({"error": "Bu telefon raqam bilan foydalanuvchi topilmadi."}, status=404)


#=======================================================================>>>>


# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from .serializers import RegisterSerializer, UserSerializer
# from .models import User

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = RegisterSerializer

# class ProfileView(generics.RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = UserSerializer

#     def get_object(self):
#         return self.request.user
    

# class AllProfileView(generics.RetrieveUpdateDestroyAPIView):

#     queryset = User.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = UserSerializer

#     lookup_field     = 'pk'
#     lookup_url_kwarg = 'userId'

#     def delete(self, request, *args, **kwargs):

#         if request.user.role == 'employee':
#             return Response(
#                 {"detail": "Вы не можете удалять!."},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         user_to_delete = self.get_object()
#         if user_to_delete.is_superuser:
#             return Response(
#                 {"detail": "Вы не можете удалять!."},
#                 status=status.HTTP_403_FORBIDDEN
#             )
#         if user_to_delete == request.user:
#             return Response(
#                 {"detail": "Вы не можете удалять!."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         return super().delete(request, *args, **kwargs)


# class ManagerListView(generics.ListAPIView):
#     queryset = User.objects.filter(role='manager')
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = UserSerializer
    
# class UserListView(generics.ListAPIView):
#     queryset = User.objects.filter(role='employee')
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = UserSerializer
    
# class AllUserListView(generics.ListAPIView):
#     queryset = User.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = UserSerializer