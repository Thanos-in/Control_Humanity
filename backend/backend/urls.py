from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tasks.views import TelegramTaskView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/ratings/', include('ratings.urls')),
    path('api/telegram-tasks/', TelegramTaskView.as_view(), name='telegram_tasks'),
    #path("django-rq/", include("django_rq.urls"))
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
