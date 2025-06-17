from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def ensure_default_statuses(sender, **kwargs):
    if sender.name == "tasks":
        Status = apps.get_model("tasks", "Status")
        defaults = [
            ("Start",   0, True),
            ("Overdue", 1, False),
            ("Finish",  2, False),
        ]
        for name, order, is_def in defaults:
            Status.objects.get_or_create(
                name=name,
                defaults={'order': order, 'is_default': is_def}
            )
            print("✅ signals.py yuklandi")