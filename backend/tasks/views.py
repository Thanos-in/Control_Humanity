from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters, status
from .models import Task, Status, SimpleTask, TaskMarkedUser
from .serializers import TaskSerializer, StatusSerializer, SimpleTaskSerializer
from .permissions import IsManagerOrDirector, IsEmployeeOrManager
from accounts.models import User
from django.db.models import Q
from tasks.utils import send_telegram_message
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny 
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

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
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date']

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'archive']:
            return [permissions.IsAuthenticated(), IsManagerOrDirector()]
        if self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsEmployeeOrManager()]
        if self.action == 'archivedtasks':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.select_related('project', 'status', 'assigned_to')

        if getattr(user, 'role', None) in ('admin', 'director') or user.is_superuser:
            base_qs = qs
        elif getattr(user, 'role', None) == 'employee':
            base_qs = qs.filter(assigned_to=user)
        elif getattr(user, 'role', None) == 'manager':
            base_qs = qs.filter(project__manager=user)
        else:
            return Task.objects.none()

        if self.action == 'archive':
            return base_qs

        if self.action == 'archivedtasks':
            return base_qs.filter(is_archived=True)

        if self.action == 'retrieve':
            include = (
                self.request.query_params.get('include_archived')
                or self.request.query_params.get('is_archived')
            )
            if include and include.lower() in ['1', 'true', 'yes']:
                return base_qs
            return base_qs.filter(is_archived=False)

        return base_qs.filter(is_archived=False)

    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user

        if request.data.get("done") is True:
            marked_users = [
                tmu.user for tmu in TaskMarkedUser.objects.filter(task=task).order_by("order")
            ]
            if user in marked_users:
                idx = marked_users.index(user)
                if idx + 1 < len(marked_users):
                    task.assigned_to = marked_users[idx + 1]
                    task.done = False
                else:
                    def_status = get_object_or_404(Status, name='Finish')
                    #task.assigned_to = None
                    task.done = True
                    task.status = def_status

                task.save()
                task.refresh_from_db(fields=["assigned_to"])
                serializer = self.get_serializer(task)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return super().partial_update(request, *args, **kwargs)



    def perform_create(self, serializer):
        default_status = get_object_or_404(Status, name='Start')
        due_date = self.request.data.get('due_date')
        save_kwargs = {
            'created_by': self.request.user,
            'status': default_status    
        }
        if due_date is not None:
            save_kwargs['due_date'] = due_date

        task = serializer.save(**save_kwargs)

        # Telegram xabari
        user = task.assigned_to
        if user and getattr(user, 'telegram_id', None):
            text = (
                f"Привет {user.first_name}!\n"
                f"Вам дали новое задание:\n"
                f"• Имя: {task.title}\n"
                f"• Описание: {task.description}\n"
                f"• Срок: {task.due_date}\n"
            )
            send_telegram_message(user.telegram_id, text)

    def perform_update(self, serializer):
        due_date = self.request.data.get('due_date')
        save_kwargs = {'updated_by': self.request.user}
        if due_date is not None:
            save_kwargs['due_date'] = due_date
        serializer.save(**save_kwargs)

    @action(detail=True, methods=['patch'], url_path='archive')
    def archive(self, request, pk=None):
        task = self.get_object()
        is_archived = request.data.get('is_archived')
        if is_archived is None:
            return Response(
                {'detail': 'is_archived field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # String yoki boolean bo‘lishini to‘g‘ri pars qilish
        if isinstance(is_archived, str):
            low = is_archived.lower()
            if low in ['true', '1', 'yes']:
                val = True
            elif low in ['false', '0', 'no']:
                val = False
            else:
                return Response(
                    {'detail': 'is_archived qiymati true yoki false bo‘lishi kerak.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            val = bool(is_archived)

        task.is_archived = val
        task.save()
        task.refresh_from_db()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='archivedtasks')
    def archivedtasks(self, request):
        qs = self.get_queryset().filter(is_archived=True)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

#===========================================================>>>>
# class TaskViewSet(viewsets.ModelViewSet):
#     serializer_class = TaskSerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['title', 'description']
#     ordering_fields = ['created_at', 'due_date']

#     def get_permissions(self):
#         if self.action in ['create', 'destroy', 'archive']:
#             return [permissions.IsAuthenticated(), IsManagerOrDirector()]
#         if self.action in ['update', 'partial_update']:
#             return [permissions.IsAuthenticated(), IsEmployeeOrManager()]
#         if self.action == 'archivedtasks':
#             return [permissions.IsAuthenticated()]
#         return [permissions.IsAuthenticated()]

#     def get_queryset(self):
#         user = self.request.user
#         qs = Task.objects.select_related('project', 'status', 'assigned_to')

#         # Ролга қараб асосий фильтр
#         if hasattr(user, 'role') and user.role == 'employee':
#             qs = qs.filter(assigned_to=user)
#         elif hasattr(user, 'role') and user.role == 'manager':
#             qs = qs.filter(project__manager=user)
#         elif hasattr(user, 'role') and user.role == 'director':
#             qs = qs.filter(project__director=user)
#         else:
#             return Task.objects.none()

#         # Агар archive toggle экшни келса, барчани олиб келиш
#         if self.action == 'archive':
#             return qs

#         # Агар archivedtasks экшни келса, фақат архивалганларни қайтариш
#         if self.action == 'archivedtasks':
#             return qs.filter(is_archived=True)

#         # Агар retrieve экшни келса, include_archived параметрини инобатга олиш
#         if self.action == 'retrieve':
#             include_archived = (
#                 self.request.query_params.get('include_archived')
#                 or self.request.query_params.get('is_archived')
#             )
#             if include_archived and include_archived.lower() in ['1', 'true', 'yes']:
#                 return qs
#             return qs.filter(is_archived=False)

#         # Бошқа ҳолатларда (list, update, partial_update, destroy) доим фақат is_archived=False
#         return qs.filter(is_archived=False)

#         def partial_update(self, request, *args, **kwargs):
#             task = self.get_object()
#             user = request.user

#             # Faqat current_assignee bo'lgan employee update qila oladi
#             if user.role != "employee" or task.assigned_to != user:
#                 return Response({"detail": "Ruxsat yo'q"}, status=403)

#             # Faqat done=true yuborilgan holatni maxsus ishlaymiz
#             if request.data.get("done") is True:
#                 marked_users = list(task.marked_to.all())
#                 if user in marked_users:
#                     index = marked_users.index(user)
#                     if index + 1 < len(marked_users):
#                         task.assigned_to = marked_users[index + 1]
#                         task.done = False
#                     else:
#                         task.assigned_to = None
#                         task.done = True
#                     task.save()
#                     serializer = self.get_serializer(task)
#                     return Response(serializer.data)

#             # Agar boshqa fieldlar bo‘lsa, default patch ishlatilsin
#             return super().partial_update(request, *args, **kwargs)

#     def perform_create(self, serializer):
#         due_date = self.request.data.get('due_date')
#         save_kwargs = {
#             'created_by': self.request.user,
#             'status': Status.objects.get(pk=39)
#         }
#         if due_date is not None:
#             save_kwargs['due_date'] = due_date

#         task = serializer.save(**save_kwargs)

#         # Telegram xabar yuborish
#         user = task.assigned_to
#         if user and getattr(user, 'telegram_id', None):
#             text = (
#                 f"Привет {user.first_name}!\n"
#                 f"Вам дали новое задание:\n"
#                 f"• Имя: {task.title}\n"
#                 f"• Описание: {task.description}\n"
#                 f"• Срок: {task.due_date}\n"
#             )
#             send_telegram_message(user.telegram_id, text)

#     def perform_update(self, serializer):
#         due_date = self.request.data.get('due_date')
#         save_kwargs = {'updated_by': self.request.user}
#         if due_date is not None:
#             save_kwargs['due_date'] = due_date
#         serializer.save(**save_kwargs)

#     # PATCH /tasks/{pk}/archive/  body: {"is_archived": true} or false
#     @action(detail=True, methods=['patch'], url_path='archive')
#     def archive(self, request, pk=None):
#         task = self.get_object()
#         is_archived = request.data.get('is_archived')
#         if is_archived is None:
#             return Response(
#                 {'detail': 'is_archived field is required.'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         # parse boolean-like strings if needed
#         if isinstance(is_archived, str):
#             low = is_archived.lower()
#             if low in ['true', '1', 'yes']:
#                 val = True
#             elif low in ['false', '0', 'no']:
#                 val = False
#             else:
#                 return Response(
#                     {'detail': 'is_archived qiymati true yoki false bo‘lishi kerak.'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#         else:
#             val = bool(is_archived)
#         task.is_archived = val
#         task.save()
#         serializer = self.get_serializer(task)
#         return Response(serializer.data)

#         # GET /tasks/archivedtasks/
#     @action(detail=False, methods=['get'], url_path='archivedtasks')
#     def archivedtasks(self, request):
#         qs = self.get_queryset().filter(is_archived=True)
#         page = self.paginate_queryset(qs)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(qs, many=True)
#         return Response(serializer.data)    

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
