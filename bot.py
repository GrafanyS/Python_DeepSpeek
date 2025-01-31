from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re
import os
import speech_recognition as sr
from pydub import AudioSegment

# Замените 'YOUR_TOKEN' на токен вашего бота
TOKEN = 'YOUR_TOKEN'

# Список нецензурных выражений (можно расширить)
BAD_WORDS = ['мат1', 'мат2', 'мат3']

# Функция для проверки сообщений на наличие нецензурных выражений
def check_message(message: str) -> bool:
    for word in BAD_WORDS:
        if re.search(r'\b' + re.escape(word) + r'\b', message, re.IGNORECASE):
            return True
    return False

# Функция для перевода голосового сообщения в текст
def voice_to_text(voice_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(voice_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")  # Распознавание на русском языке
        return text
    except sr.UnknownValueError:
        return "Не удалось распознать речь"
    except sr.RequestError:
        return "Ошибка сервиса распознавания речи"

# Обработчик текстовых сообщений
def handle_message(update: Update, context: CallbackContext):
    message_text = update.message.text
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if check_message(message_text):
        # Бан пользователя
        context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        context.bot.send_message(chat_id=chat_id, text=f"Пользователь {update.message.from_user.username} был забанен за использование нецензурных выражений.")

# Обработчик голосовых сообщений
def handle_voice(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    # Скачиваем голосовое сообщение
    voice_file = update.message.voice.get_file()
    voice_file.download("voice_message.ogg")

    # Конвертируем .ogg в .wav
    audio = AudioSegment.from_file("voice_message.ogg", format="ogg")
    audio.export("voice_message.wav", format="wav")

    # Переводим голосовое сообщение в текст
    text = voice_to_text("voice_message.wav")

    # Отправляем распознанный текст в чат
    context.bot.send_message(chat_id=chat_id, text=f"Распознанный текст: {text}")

    # Удаляем временные файлы
    os.remove("voice_message.ogg")
    os.remove("voice_message.wav")

# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Бот запущен и готов следить за чатом!')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.voice, handle_voice))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    