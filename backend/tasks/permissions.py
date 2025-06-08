from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'

class IsDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'director'

class IsManagerOrDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.role == 'manager' or user.role == 'director')

class IsEmployeeOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and
            (obj.assigned_to == user or obj.project.manager == user or user.role == 'director')
        )





# from rest_framework import permissions

# class IsDirector(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == 'director'

# class IsManager(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == 'manager'

# class IsEmployeeOrManager(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         user = request.user
#         return (
#             user.is_authenticated and
#             (obj.assigned_to == user or obj.project.manager == user or user.role == 'director')
#         )
