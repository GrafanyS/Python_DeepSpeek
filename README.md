# Создание Telegram-бота

Создание Telegram-бота для группового чата с функцией бана за нецензурные выражения можно реализовать с использованием библиотеки python-telegram-bot. Ниже приведен пример кода на Python, который демонстрирует, как это можно сделать.
.

## Шаги для создания бота:

1 Создайте бота в Telegram:

2 Откройте Telegram и найдите бота BotFather.

3 Создайте нового бота с помощью команды /newbot.

4 Получите токен вашего бота.

5 Установите необходимые библиотеки:

6 Установите библиотеку python-telegram-bot:

```bash
pip install python-telegram-bot
```

Напишите код бота:

```python
from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

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

# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Бот запущен и готов следить за чатом!')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
```

## Как это работает`:`

* BAD_WORDS: Список нецензурных выражений, которые бот будет искать в сообщениях.

* check_message: Функция, которая проверяет, содержит ли сообщение нецензурные выражения.

* handle_message: Обработчик сообщений. Если сообщение содержит нецензурное выражение, бот банит пользователя и удаляет сообщение.

* start: Обработчик команды /start, который отправляет сообщение о том, что бот запущен.

### Запуск бота`:`

Сохраните код в файл, например, bot.py.

Запустите бота с помощью команды:

```bash
python bot.py
```

### Добавление бота в группу`:`

Добавьте бота в группу и сделайте его администратором с правами на удаление сообщений и блокировку пользователей.

### Примечания`:`

Бот должен быть администратором в группе, чтобы иметь возможность банить пользователей и удалять сообщения.

Вы можете расширить список BAD_WORDS и добавить более сложную логику для фильтрации сообщений.

Этот бот будет автоматически банить пользователей, которые используют нецензурные выражения, и удалять их сообщения.

## добавить перевод голосовых сообщений в текст

Чтобы добавить функциональность перевода голосовых сообщений в текст, можно использовать библиотеку speech_recognition для распознавания речи. Также потребуется установить ffmpeg для обработки аудиофайлов.

Шаги для добавления перевода голосовых сообщений в текст:
Установите необходимые библиотеки:

Установите библиотеку speech_recognition:

```bash
pip install SpeechRecognition
```

Установите pydub для работы с аудиофайлами:

```bash
pip install pydub
```

Установите ffmpeg (если не установлен):

* Для Windows: скачайте с официального сайта и добавьте в PATH.

* Для Linux/macOS: используйте пакетный менеджер (например, apt или brew).

Обновите код бота:

```python
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
```

### Как это работает

Скачивание голосового сообщения:

Бот скачивает голосовое сообщение в формате .ogg.

* Конвертация в .wav:

* Используется библиотека pydub для конвертации .ogg в .wav, так как speech_recognition лучше работает с .wav.

### Распознавание текста`:`

Библиотека speech_recognition использует Google Web Speech API для перевода аудио в текст.

### Отправка текста в чат`:`

Распознанный текст отправляется обратно в чат.

Удаление временных файлов:

После обработки временные файлы удаляются.

### Запуск бота

Сохраните код в файл, например, bot.py.

Запустите бота с помощью команды:

```bash
python bot.py
```

### Примечания

Для работы с голосовыми сообщениями боту нужно иметь доступ к файлам в группе.

Распознавание речи зависит от качества аудио и может быть не всегда точным.

Вы можете использовать другие API для распознавания речи, например, Yandex SpeechKit или Microsoft Azure Speech Service, если требуется более высокая точность.

Теперь ваш бот может не только банить за нецензурные выражения, но и переводить голосовые сообщения в текст!
