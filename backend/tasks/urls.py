from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TaskViewSet, StatusViewSet, StatusesViewSet, SimpleTaskViewSet

router = DefaultRouter()
router.register('statuses', StatusViewSet, basename='status')
router.register('global-statuses', StatusesViewSet, basename='global-status')
router.register('simple-tasks', SimpleTaskViewSet, basename='simple-tasks')
router.register('', TaskViewSet, basename='task')

urlpatterns = router.urls
