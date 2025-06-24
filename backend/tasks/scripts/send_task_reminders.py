# import os
# import django
# import datetime
# import requests
# import sys

# sys.path.append("C:/Users/user/Desktop/nebula projects/web_programs/control_humanity/backend")

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# django.setup()

# print("Ishlayapti")

# from tasks.models import Task
# from django.contrib.auth import get_user_model
# from django.conf import settings

# User = get_user_model()

# API_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

# def send_message(chat_id, text):
#     if chat_id:
#         requests.post(API_URL, data={
#             'chat_id': chat_id,
#             'text': text
#         })

# def run():
#     today = datetime.datetime.now().date()
#     week_later_start = today + datetime.timedelta(days=7)
#     week_later_end = week_later_start + datetime.timedelta(days=1)

#     tasks = Task.objects.filter(
#         due_date__date__gte=week_later_start,
#         due_date__date__lt=week_later_end,
#         assigned_to__isnull=False
#     )

#     for task in tasks:
#         user = task.assigned_to
#         if hasattr(user, 'telegram_id') and user.telegram_id:
#             text = f"🕓 Eslatma: Sizga tayinlangan '{task.title}' vazifa muddati {task.due_date.strftime('%Y-%m-%d')} sanasida tugaydi. Yana 7 kun qoldi!"
#             send_message(user.telegram_id, text)

# if __name__ == "__main__":
#     run()

import os
import django
import requests
import sys

# Django project yo‘lini qo‘shish
sys.path.append("C:/Users/user/Desktop/nebula projects/web_programs/control_humanity/backend")

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Sozlamalarni olish
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
API_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

def send_message(chat_id, text):
    if chat_id:
        requests.post(API_URL, data={
            'chat_id': chat_id,
            'text': text
        })

def run():
    users = User.objects.exclude(telegram_id=None)
    for user in users:
        send_message(user.telegram_id, "automatic launch completed!")

if __name__ == "__main__":
    run()
