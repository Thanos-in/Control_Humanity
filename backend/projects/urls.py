from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ModuleViewSet  

router = DefaultRouter()
router.register('', ProjectViewSet, basename='project')
router.register('/modules/', ModuleViewSet, basename='modules')

urlpatterns = router.urls
