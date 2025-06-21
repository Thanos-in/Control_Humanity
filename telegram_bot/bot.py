from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import requests
from datetime import datetime

BOT_TOKEN = '8040016996:AAGRy-acyXz_Y3UwdJINC4oxsphE39BgeyE'
BIND_URL = 'http://localhost:8000/api/auth/bind-telegram/'
TASKS_URL = 'http://localhost:8000/api/telegram-tasks/'

# /start — telefon raqamini so'raydi
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_btn = KeyboardButton(text="📱 Telefon raqamini yuborish", request_contact=True)
    kb = [[contact_btn]]
    reply_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Assalomu alaykum! Iltimos, telefon raqamingizni yuboring:",
        reply_markup=reply_markup
    )

# Kontakt qabul qilganda backendga bog'laydi
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    contact = update.message.contact

    # Faqat o'z kontaktingiz bo'lsa
    if contact.user_id != user.id:
        await update.message.reply_text("❌ Iltimos, o'zingizning raqamingizni yuboring.")
        return

    phone = contact.phone_number
    normalized_phone = f"+{phone.lstrip('+')}"
    telegram_id = user.id
    print(f"📞 Yuborilgan raqam: {normalized_phone}")
    print(f"👤 Telegram ID: {telegram_id}")
    try:
        resp = requests.post(BIND_URL, json={
            "phone": normalized_phone,
            "telegram_id": telegram_id
        }, timeout=5)
        if resp.status_code == 200:
            await update.message.reply_text(
                "✅ Telefon raqamingiz muvaffaqiyatli bog‘landi!\nEndi /mytasks komandasini yuboring.",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await update.message.reply_text(
                f"❌ Xatolik ({resp.status_code}): {resp.text}"
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Serverga ulanib bo‘lmadi: {e}")

# /mytasks — tasklarni olib beradi
async def task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        resp = requests.get(TASKS_URL, params={'telegram_id': chat_id}, timeout=5)
        data = resp.json()
        if resp.status_code != 200 or not data:
            await context.bot.send_message(chat_id=chat_id, text="✅ Sizga hozircha task yo‘q.")
            return

        msg = "📋 *Sizga tegishli tasklar:*\n\n"
        msg += "`№  Nomi                          Status       Muddati`\n"

        for i, task in enumerate(data, 1):
            title = task['title']
            if len(title) > 30:
                title = title[:27] + "..."
            status = task['status']['name']

            def fmt(f):
                raw = task.get(f)
                try:
                    return datetime.fromisoformat(raw).strftime('%d.%m.%Y') if raw else '—'
                except:
                    return '—'

            created = fmt('created_at')
            updated = fmt('updated_at')
            due     = fmt('due_date')
            period = f"{created}→{updated}→{due}"

            msg += f"{i:<3} {title:<30} {status:<12} {period}\n"

        await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ Xatolik: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    # Handler’lar
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(CommandHandler("mytasks", task_handler))
    # Polling
    app.run_polling()

if __name__ == "__main__":
    main()


#===========================================================>>>>


# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# import requests
# from datetime import datetime   

# BOT_TOKEN = '8040016996:AAGRy-acyXz_Y3UwdJINC4oxsphE39BgeyE'
# BACKEND_URL = 'http://localhost:8000/api/telegram-tasks/'

# async def task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id

#     try:
#         response = requests.get(BACKEND_URL, params={'telegram_id': chat_id})
#         data = response.json()

#         if response.status_code != 200 or not data:
#             await context.bot.send_message(chat_id=chat_id, text="✅ У вас пока нет задач.")
#             return

#         msg = "📋 *Задачи, связанные с вами:*\n\n"
#         msg += f"*{'№':<3} {'Наименование':<30} Статус        Сроки*\n"

#         for i, task in enumerate(data, 1):
#             title = task['title'][:10] + '...' if len(task['title']) > 30 else task['title']
#             status = task['status']['name']

#             def format_date(field):
#                 raw = task.get(field)
#                 try:
#                     return datetime.fromisoformat(raw).strftime('%d.%m.%Y') if raw else '—'
#                 except:
#                     return '—'

#             created = format_date('created_at')
#             updated = format_date('updated_at')
#             due = format_date('due_date')

#             period_str = f"{created} → {updated} → {due}"
#             msg += f"{i:<3} {title:<30} {status:<12} {period_str}\n"

#         await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')

#     except Exception as e:
#         await context.bot.send_message(chat_id=chat_id, text=f"Ошибка!: {str(e)}")

# app = ApplicationBuilder().token(BOT_TOKEN).build()
# app.add_handler(CommandHandler("mytasks", task_handler))
# app.run_polling()
