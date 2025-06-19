from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Task
from tasks.utils import send_telegram_message

# @receiver(post_migrate)
# def ensure_default_statuses(sender, **kwargs):
#     if sender.name == "tasks":
#         Status = apps.get_model("tasks", "Status")
#         defaults = [
#             ("Start",   0, True),
#             ("Overdue", 1, False),
#             ("Finish",  2, False),
#         ]
#         for name, order, is_def in defaults:
#             Status.objects.get_or_create(
#                 name=name,
#                 defaults={'order': order, 'is_default': is_def}
#             )


# @receiver(post_save, sender=Task)
# def notify_on_task_create(sender, instance, created, **kwargs):
#     if created and instance.assigned_to and instance.assigned_to.telegram_id:
#         text = f"Salom {instance.assigned_to.first_name}!\nSizga yangi vazifa: {instance.title}"
#         send_telegram_message.delay(instance.assigned_to.telegram_id, text)
#         print('good!')