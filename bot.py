import platform
import random
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

#Установка токена бота
bot_token = '6547665217:AAEs6odbtzDUkEP57l9LZKiFWLTWWx7Tn9w'
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

#Вопросы для викторины
quiz_questions = [
    {
        "question": "Сколько планет в Солнечной системе?",
        "options": ["6", "7", "8", "9"],
        "correct_option": 2
    },
    {
        "question": "Какая самая большая планета в Солнечной системе?",
        "options": ["Меркурий", "Венера", "Земля", "Юпитер"],
        "correct_option": 3
    }
]

#Обработчик команды /start
def start(update, context):
    #Отправка приветственного сообщения
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет 👋 Я бот-помощник. Давай знакомиться!🙂 Как тебя зовут?")

# Обработчик получения имени пользователя
def get_name(update, context):
    #Получение имени пользователя из сообщения
    name = update.message.text
    #Сохранение имени в контексте пользователя
    context.user_data['name'] = name
    #Создание клавиатуры с кнопками
    reply_markup = create_keyboard_markup()
    #Отправка сообщения с просьбой выбрать действие
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{name}, чем могу помочь?🙂", reply_markup=reply_markup)

#Создание клавиатуры с кнопками
def create_keyboard_markup():
    keyboard = [
        [InlineKeyboardButton("Информация о машине 🤖", callback_data='info')],
        [InlineKeyboardButton("Пройти викторину ❓", callback_data='quiz')],
        [InlineKeyboardButton("Ссылка на GitHub моего создателя ➡️", url="https://github.com/BashkatovaAD")]
    ]
    return InlineKeyboardMarkup(keyboard)

#Обработчик кнопки "Информация о машине"
def info(update, context):
    #Получение информации о машине
    info_text = (
        "🔽 Информация о машине, на которой запущен бот-помощник:\n\n"
        f"Machine: {platform.machine()};\n"
        f"Version: {platform.version()};\n"
        f"Platform: {platform.platform()};\n"
        f"Uname: {platform.uname()};\n"
        f"System: {platform.system()}."
    )
    #Отправка информации о машине
    context.bot.send_message(chat_id=update.effective_chat.id, text=info_text)
    #Создание клавиатуры с кнопками
    reply_markup = create_keyboard_markup()
    #Отправка сообщения с просьбой выбрать действие
    context.bot.send_message(chat_id=update.effective_chat.id, text="Чем еще могу помочь? 🙂", reply_markup=reply_markup)

#Обработчик кнопки "Пройти викторину"
def quiz(update, context):
    #Выбор случайного вопроса из списка
    random_question = random.choice(quiz_questions)
    question_text = random_question["question"]
    options = random_question["options"]
    correct_option = random_question["correct_option"]

    #Сохраняем параметры options
    context.user_data['options'] = options
    #Создание клавиатуры с вариантами ответов
    reply_markup = create_quiz_keyboard_markup(options)

    context.user_data['correct_option'] = correct_option
    #Отправка вопроса с клавиатурой вариантов ответов
    context.bot.send_message(chat_id=update.effective_chat.id, text=question_text, reply_markup=reply_markup)

#Создание клавиатуры с вариантами ответов
def create_quiz_keyboard_markup(options):
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in options]
    return InlineKeyboardMarkup(keyboard)

def quiz_answer_callback(update, context):
    #Получение выбранного пользователем варианта ответа
    selected_option = update.callback_query.data
    #Получение правильного варианта ответа из контекста пользователя
    correct_option = context.user_data.get('correct_option')
    #Получение вариантов ответов из контекста пользователя
    options = context.user_data.get('options')
    
    #Проверка выбранного варианта ответа
    if selected_option == options[correct_option]:
        #Если выбран правильный вариант ответа
        context.bot.send_message(chat_id=update.effective_chat.id, text="УРА!👍 Это правильный ответ! 🎉")
    else:
        #Если выбран неправильный вариант ответа
        context.bot.send_message(chat_id=update.effective_chat.id, text="Эх, попробуй снова! 😔 Это неправильный ответ! 😔")
    
    #Создание клавиатуры с кнопками
    reply_markup = create_keyboard_markup()
    
    #Отправка сообщения с просьбой выбрать действие
    context.bot.send_message(chat_id=update.effective_chat.id, text="Чем еще могу помочь?", reply_markup=reply_markup)

#Создание обработчиков команд и сообщений с помощью классов-обработчиков
start_handler = CommandHandler('start', start)
name_handler = MessageHandler(Filters.text & ~Filters.command, get_name)
info_button_handler = CallbackQueryHandler(info, pattern='info')
quiz_button_handler = CallbackQueryHandler(quiz, pattern='quiz')
quiz_answer_handler = CallbackQueryHandler(quiz_answer_callback)

#Добавление обработчиков в диспетчер
dispatcher.add_handler(start_handler)
dispatcher.add_handler(name_handler)
dispatcher.add_handler(info_button_handler)
dispatcher.add_handler(quiz_button_handler)
dispatcher.add_handler(quiz_answer_handler)

#Запуск цикла получения обновлений от Telegram
updater.start_polling()


