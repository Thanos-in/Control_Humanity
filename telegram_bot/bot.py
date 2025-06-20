from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from datetime import datetime   

BOT_TOKEN = '8040016996:AAGRy-acyXz_Y3UwdJINC4oxsphE39BgeyE'
BACKEND_URL = 'http://localhost:8000/api/telegram-tasks/'

async def task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    try:
        response = requests.get(BACKEND_URL, params={'telegram_id': chat_id})
        data = response.json()

        if response.status_code != 200 or not data:
            await context.bot.send_message(chat_id=chat_id, text="✅ У вас пока нет задач.")
            return

        msg = "📋 *Задачи, связанные с вами:*\n\n"
        msg += f"*{'№':<3} {'Наименование':<30} Статус        Сроки*\n"

        for i, task in enumerate(data, 1):
            title = task['title'][:10] + '...' if len(task['title']) > 30 else task['title']
            status = task['status']['name']

            def format_date(field):
                raw = task.get(field)
                try:
                    return datetime.fromisoformat(raw).strftime('%d.%m.%Y') if raw else '—'
                except:
                    return '—'

            created = format_date('created_at')
            updated = format_date('updated_at')
            due = format_date('due_date')

            period_str = f"{created} → {updated} → {due}"
            msg += f"{i:<3} {title:<30} {status:<12} {period_str}\n"

        await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Ошибка!: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("mytasks", task_handler))
app.run_polling()
