from rest_framework import viewsets, permissions, filters
from .models import Task, Status
from .serializers import TaskSerializer, StatusSerializer
from .permissions import IsManagerOrDirector, IsEmployeeOrManager
from django.db.models import Q

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsManagerOrDirector()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # For list action, filter by project_id; for detail/update/destroy, return all
        if self.action == 'list':
            project_id = self.request.query_params.get('project_id')
            if project_id:
                return Status.objects.filter(
                    Q(project__isnull=True)  # global statuses
                    | Q(project_id=project_id)  # project-specific statuses
                ).order_by('order')
            # if no project_id, return only global statuses
            return Status.objects.filter(project__isnull=True).order_by('order')
        return Status.objects.all()

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
        if user.role == 'employee':
            return Task.objects.filter(assigned_to=user)
        elif user.role == 'manager':
            return Task.objects.filter(project__manager=user)
        elif user.role == 'director':
            return Task.objects.filter(project__director=user)
        return Task.objects.none()

    def perform_create(self, serializer):
        # Include due_date if provided in request data
        due_date = self.request.data.get('due_date')
        save_kwargs = {'created_by': self.request.user}
        if due_date is not None:
            save_kwargs['due_date'] = due_date
        serializer.save(**save_kwargs)

    def perform_update(self, serializer):
        # Handle due_date updates along with updated_by
        due_date = self.request.data.get('due_date')
        save_kwargs = {'updated_by': self.request.user}
        if due_date is not None:
            save_kwargs['due_date'] = due_date
        serializer.save(**save_kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


#=======================================================================>

# from rest_framework import viewsets, permissions, filters, status
# from rest_framework.response import Response
# from .models import Task, Status
# from .serializers import TaskSerializer, StatusSerializer
# from .permissions import IsManagerOrDirector, IsEmployeeOrManager
# from django.db.models import Q

# class StatusViewSet(viewsets.ModelViewSet):
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             return [permissions.IsAuthenticated(), IsManagerOrDirector()]
#         return [permissions.IsAuthenticated()]

#     def get_queryset(self):
#         # For list action, filter by project_id; for detail/update/destroy, return all
#         if self.action == 'list':
#             project_id = self.request.query_params.get('project_id')
#             if project_id:
#                 return Status.objects.filter(
#                     Q(project__isnull=True)  # global statuslar
#                     | Q(project_id=project_id)  # loyiha statuslari
#                 ).order_by('order')
#             # agar project_id berilmasa, faqat global statuslarni qaytaradi!!!
#             return Status.objects.filter(project__isnull=True).order_by('order')
#         return Status.objects.all()

#     def perform_update(self, serializer):
#         serializer.save()


#     class TaskViewSet(viewsets.ModelViewSet):
#         queryset = Task.objects.all().select_related('project', 'status', 'assigned_to')
#         serializer_class = TaskSerializer
#         filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#         search_fields = ['title', 'description']
#         ordering_fields = ['created_at', 'due_date']

#         def get_permissions(self):
#             if self.action in ['create', 'destroy']:
#                 return [permissions.IsAuthenticated(), IsManagerOrDirector()]
#             if self.action in ['update', 'partial_update']:
#                 return [permissions.IsAuthenticated(), IsEmployeeOrManager()]
#             return [permissions.IsAuthenticated()]

#     def get_queryset(self):
#         user = self.request.user
#         if user.role == 'employee':
#             return Task.objects.filter(assigned_to=user)
#         elif user.role == 'manager':
#             return Task.objects.filter(project__manager=user)
#         elif user.role == 'director':
#             return Task.objects.filter(project__director=user)
#         return Task.objects.none()

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)                       

#     def perform_update(self, serializer):
#         serializer.save(updated_by=self.request.user)

#     def partial_update(self, request, *args, **kwargs):
#         return super().partial_update(request, *args, **kwargs)


#===================================================================>

# from rest_framework import viewsets, permissions, filters, status
# from rest_framework.response import Response
# from .models import Task, Status
# from .serializers import TaskSerializer, StatusSerializer
# from .permissions import IsManagerOrDirector, IsEmployeeOrManager

# class StatusViewSet(viewsets.ModelViewSet):
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             return [permissions.IsAuthenticated(), IsManagerOrDirector()]
#         return [permissions.IsAuthenticated()]

#     def get_queryset(self):
#         project_id = self.request.query_params.get('project_id')
#         if project_id:
#             return Status.objects.filter(project_id=project_id).order_by('order')
#         return Status.objects.none()

#     def perform_update(self, serializer):
#         # Update order or name
#         serializer.save()


# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all().select_related('project', 'status', 'assigned_to')
#     serializer_class = TaskSerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['title', 'description']
#     ordering_fields = ['created_at', 'due_date']

#     def get_permissions(self):
#         if self.action in ['create', 'destroy']:
#             # Only manager or director can create/delete tasks
#             return [permissions.IsAuthenticated(), IsManagerOrDirector()]
#         if self.action in ['update', 'partial_update']:
#             # Employee can update their own tasks; managers/directors can update any
#             return [permissions.IsAuthenticated(), IsEmployeeOrManager()]
#         return [permissions.IsAuthenticated()]

#     def get_queryset(self):
#         user = self.request.user
#         if user.role == 'employee':
#             return Task.objects.filter(assigned_to=user)
#         elif user.role == 'manager':
#             return Task.objects.filter(project__manager=user)
#         elif user.role == 'director':
#             return Task.objects.filter(project__director=user)
#         return Task.objects.none()

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)

#     def perform_update(self, serializer):
#         # Handle inline edits or status changes
#         serializer.save(updated_by=self.request.user)

#     def partial_update(self, request, *args, **kwargs):
#         # Allow partial updates for inline edits
#         return super().partial_update(request, *args, **kwargs)


