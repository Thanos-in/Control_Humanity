from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters, status
from .models import Task, Status, SimpleTask
from .serializers import TaskSerializer, StatusSerializer, SimpleTaskSerializer
from .permissions import IsManagerOrDirector, IsEmployeeOrManager
from accounts.models import User
from django.db.models import Q
from tasks.utils import send_telegram_message
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny 


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsManagerOrDirector()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.action == 'list':
            project_id = self.request.query_params.get('project_id')
            if project_id:
                return Status.objects.filter(
                Q(project__isnull=True) | Q(project_id=project_id)
            ).filter(
                user__isnull=True
            ).order_by('order')
            return Status.objects.filter(project__isnull=True).order_by('order')
        return Status.objects.all()

    def destroy(self, request, *args, **kwargs):
        status_obj = self.get_object()
        if status_obj.is_default:
            return Response(
                {"detail": "Default statuslarni o‘chirish mumkin emas."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related('project', 'status', 'assigned_to')
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date']

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [permissions.IsAuthenticated(), IsManagerOrDirector()]
        if self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsEmployeeOrManager()]
        return [permissions.IsAuthenticated()]


    def get_queryset(self):
            user = self.request.user
            qs = Task.objects.select_related('project', 'status', 'assigned_to')

            # Role-based filtering
            if user.role == 'employee':
                qs = qs.filter(assigned_to=user)
            elif user.role == 'manager':
                qs = qs.filter(project__manager=user)
            elif user.role == 'director':
                qs = qs.filter(project__director=user)
            else:
                return Task.objects.none()

            # Filter by project_id query param
            project_id = self.request.query_params.get('project_id')
            if project_id:
                qs = qs.filter(project_id=project_id)

            return qs


    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == 'employee':
    #         return Task.objects.filter(assigned_to=user)
    #     elif user.role == 'manager':
    #         return Task.objects.filter(project__manager=user)
    #     elif user.role == 'director':
    #         return Task.objects.filter(project__director=user)
    #     return Task.objects.none()

    
    def perform_create(self, serializer):
        due_date = self.request.data.get('due_date')
        save_kwargs = {'created_by': self.request.user,
                       'status': Status.objects.get(pk=39)
                       }
        if due_date is not None:
            save_kwargs['due_date'] = due_date

        task = serializer.save(**save_kwargs)

        user = task.assigned_to
   
        if user and getattr(user, 'telegram_id', None):
            text = (
                f"Привет {user.first_name}!\n"
                f"Вам дали новое задание:\n"
                f"• Имя: {task.title}\n"
                f"• Определение: {task.description}\n"
                f"• Продолжительность: {task.due_date}\n"
            )
            send_telegram_message(user.telegram_id, text)

    def perform_update(self, serializer):
        due_date = self.request.data.get('due_date')
        save_kwargs = {'updated_by': self.request.user}
        if due_date is not None:
            save_kwargs['due_date'] = due_date
        serializer.save(**save_kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    

class StatusesViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return Status.objects.filter(user=self.request.user).order_by('order')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SimpleTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SimpleTaskSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return SimpleTask.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TelegramTaskView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        telegram_id = request.query_params.get('telegram_id')
        
        if not telegram_id:
            return Response({"error": "telegram_id is required"}, status=400)

        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        tasks = Task.objects.filter(assigned_to=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
