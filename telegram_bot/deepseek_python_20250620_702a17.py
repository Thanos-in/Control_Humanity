import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes,
)
from datetime import datetime

# Настройки бота
TOKEN = "8040016996:AAGRy-acyXz_Y3UwdJINC4oxsphE39BgeyE"
API_URL = "https://api.telegram.org/bot"

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальные переменные для хранения данных
user_data = {}

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [
            {"text": "Русский", "callback_data": "lang_ru"},
            {"text": "English", "callback_data": "lang_eng"},
            {"text": "O'zbekcha", "callback_data": "lang_uz"},
        ]
    ]
    reply_markup = {"inline_keyboard": keyboard}
    
    await update.message.reply_text(
        f"Привет, {user.first_name}! Выберите язык / Hello, {user.first_name}! Choose language / Salom, {user.first_name}! Tilni tanlang",
        reply_markup=reply_markup,
    )

# Обработчик callback_query для выбора языка
async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    callback_data = query.data
    
    # Определяем выбранный язык
    if callback_data == "lang_ru":
        language = "RU"
        text = "Для получения расчетного листа отправьте свой номер телефона с помощью кнопки"
        button_text = "Отправить свой номер"
    elif callback_data == "lang_eng":
        language = "ENG"
        text = "To receive your payslip, please send your phone number using the button"
        button_text = "Send my phone number"
    elif callback_data == "lang_uz":
        language = "UZ"
        text = "Иш хаки хисоботини олиш учун телефон рақамингизни юборинг"
        button_text = "Телефон рақамимни юбориш"
    else:
        return
    
    # Сохраняем язык пользователя (в реальном приложении нужно сохранять в БД)
    user_data[user_id] = {"language": language}
    
    # Создаем клавиатуру с кнопкой запроса номера телефона
    keyboard = [[KeyboardButton(button_text, request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=True
    )
    
    await query.edit_message_text(text=text)
    await context.bot.send_message(
        chat_id=user_id, text=text, reply_markup=reply_markup
    )

# Обработчик получения контакта
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    contact = update.message.contact
    
    # Проверяем, что контакт принадлежит отправителю
    if contact.user_id == user.id:
        phone_number = contact.phone_number
        user_id = user.id
        
        # Сохраняем номер телефона (в реальном приложении нужно сохранять в БД)
        if user_id in user_data:
            user_data[user_id]["phone_number"] = phone_number
        else:
            user_data[user_id] = {"phone_number": phone_number, "language": "RU"}
        
        # Получаем язык пользователя
        language = user_data.get(user_id, {}).get("language", "RU")
        
        # Текст сообщения в зависимости от языка
        if language == "RU":
            text = "Введите период расчета. ММ/ГГГГ - Пример: 01.2025"
        elif language == "ENG":
            text = "Enter the calculation period. MM/YYYY - Example: 01.2025"
        elif language == "UZ":
            text = "Хисоблаш даврини киритинг. ОЙ/ЙИЛ - Мисол учун: 01.2025"
        
        await update.message.reply_text(
            text, reply_markup=ReplyKeyboardRemove()
        )

# Обработчик текстовых сообщений (для периода расчета)
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    user_id = update.effective_user.id
    
    # Здесь можно добавить проверку формата периода (ММ.ГГГГ)
    # и логику для получения расчетного листа
    
    language = user_data.get(user_id, {}).get("language", "RU")
    
    if language == "RU":
        response = "Ваш расчетный лист за указанный период готовится..."
    elif language == "ENG":
        response = "Your payslip for the specified period is being prepared..."
    elif language == "UZ":
        response = "Сизнинг кўрсатилган давр учун иш ҳақи хисоботингиз тайёрланиб бўлди..."
    
    await update.message.reply_text(response)

def main() -> None:
    # Создаем приложение и передаем токен бота
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(language_selection))
    application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()