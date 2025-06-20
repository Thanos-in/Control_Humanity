from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ModuleViewSet, ArchivedProjectsViewSet  

router = DefaultRouter()
router.register('modules', ModuleViewSet, basename='modules')
router.register('', ProjectViewSet, basename='project')

urlpatterns = router.urls
