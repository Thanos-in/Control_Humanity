from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TaskViewSet, StatusViewSet

router = DefaultRouter()
router.register('statuses', StatusViewSet, basename='status')
router.register('', TaskViewSet, basename='task')

urlpatterns = router.urls

# router = DefaultRouter()
# router.register('statuses', StatusViewSet, basename='status')
# router.register('tasks', TaskViewSet, basename='task')

# urlpatterns = router.urls 





# from rest_framework.routers import DefaultRouter
# from .views import TaskViewSet, StatusViewSet

# router = DefaultRouter()
# router.register('statuses', StatusViewSet, basename='status')
# router.register('', TaskViewSet, basename='task')

# urlpatterns = router.urls
