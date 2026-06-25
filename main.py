import sys
import re
import json
import telebot
from telebot import types
import os

# --- ТРЕБОВАНИЕ: Аргументы командной строки через sys.argv ---
DEBUG_MODE = False

# Проверяем, передал ли пользователь флаг --debug при запуске в консоли
if "--debug" in sys.argv:
    DEBUG_MODE = True
    print("[DEBUG] Бот запущен в режиме отладки! Все логи будут выводиться сюда.")

token = os.environ.get('BOT_TOKEN', '')
bot = telebot.TeleBot(token)

# Загружаем тексты из файла config.json
try:
    with open("config.json", "r", encoding="utf-8") as f:
        CONTENT = json.load(f)
except Exception as e:
    print(f"Ошибка при чтении config.json: {e}")
    sys.exit(1)


# Функция для создания меню с кнопками
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('👤 О себе'), types.KeyboardButton('🎯 Моя цель'))
    markup.add(types.KeyboardButton('🚀 Как я пришел в IT'), types.KeyboardButton('🧠 Мой ментор'))
    markup.add(types.KeyboardButton('📈 Точка А → Точка Б'), types.KeyboardButton('🎸 Хобби'))
    markup.add(types.KeyboardButton('💻 Мои работы'), types.KeyboardButton('🔗 GitHub'))
    return markup


# Ответ на команду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if DEBUG_MODE:
        print(f"[DEBUG] Пользователь {message.chat.id} ввел команду /start")

    bot.send_message(
        message.chat.id,
        'Привет! Это моё бот-портфолио. Выберите интересующий вас раздел на кнопках ниже 👇',
        reply_markup=get_main_keyboard()
    )


# Команда /help
@bot.message_handler(commands=['menu'])
def help_command(message):
    if DEBUG_MODE:
        print(f"[DEBUG] Пользователь {message.chat.id} ввел команду menu")

    help_text = (
        "📖 *Справка по боту-портфолио*\n\n"
        "Для навигации используйте кнопки внизу экрана 👇\n\n"
        "📜 *Доступные команды:* \n"
        "/start — Главное меню\n"
        "/menu — Справка\n"
        "Секретный код для ментора: `код-2077`\n"
        "Попробуйте написать один из данных слов: спотифай|spotify|музыка"
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown", reply_markup=get_main_keyboard())


# --- ТРЕБОВАНИЕ: Использование регулярных выражений (re) ---
# Этот хэндлер поймает ЛЮБОЙ текст вида "код-XXXX" (где XXXX — любые цифры)
# --- ТРЕБОВАНИЕ: Использование регулярных выражений (re) ---
# ИСПРАВЛЕНО: сначала проверяем, что текст есть, а затем применяем регулярку к нижнему регистру текста
@bot.message_handler(func=lambda message: message.text is not None and re.match(r"^код-\d+$", message.text.lower()))
def handle_secret_code(message):
    if DEBUG_MODE:
        print(f"[DEBUG] Сработала регулярка re.match на текст: {message.text}")

    # С помощью регулярки вытаскиваем только цифры из текста
    code_number = re.search(r"\d+", message.text).group()

    # ИСПРАВЛЕНО: Объединили весь текст в одну красивую строку
    response_text = (
        f"🎉 *Пасхалка активирована!*\n"
        f"Телеграм-бот успешно распознал ваш код: `{code_number}`.\n\n"
        f"Перейдите по этой ссылке: [Ссылка](https://open.spotify.com/track/7mykoq6R3BArsSpNDjFQTm?si=fadff05ddd16496b)"
    )

    bot.send_message(
        message.chat.id,
        response_text,
        parse_mode="Markdown"
    )


# --- ЕЩЕ ОДНО ТРЕБОВАНИЕ: Регулярка для Спотифай ---
# Ловит слова "спотифай", "spotify", "музыка", "музыку" в любом регистре
@bot.message_handler(
    func=lambda message: message.text is not None and re.search(r"(спотифай|spotify|музыка)", message.text.lower()))
def handle_spotify_request(message):
    if DEBUG_MODE:
        print(f"[DEBUG] Обнаружена ключевое слово связанное с музыкой: {message.text}")

    spotify_text = (
        "🎵 *Мой плейлист в Spotify*\n\n"
        "Здесь собраны мои самые любимые песни в Spotify:\n"
        "🔗 [Открыть любимый плейлист](https://open.spotify.com/playlist/5Y6DMhDxDYxOKtSabgV6UT?si=_daZQWKEQE2scNrX5sLQ6A)"
    )
    # Вместо https://open.spotify.com/ можешь вставить реальную ссылку на свой плейлист или трек

    bot.send_message(
        message.chat.id,
        spotify_text,
        parse_mode="Markdown",
        disable_web_page_preview=False  # Это чтобы подгружалось красивое превью ссылки
    )

# Обработка нажатий на обычные кнопки меню (ВСЕГДА В САМОМ НИЗУ)
# Обработка нажатий на обычные кнопки меню (ВСЕГДА В САМОМ НИЗУ)
@bot.message_handler(content_types=['text'])
def message_reply(message):
    if DEBUG_MODE:
        print(f"[DEBUG] Пользователь нажал кнопку: {message.text}")

    if message.text == '👤 О себе':
        bot.send_message(message.chat.id, CONTENT['about'], parse_mode='Markdown')
    elif message.text == '🎯 Моя цель':
        bot.send_message(message.chat.id, CONTENT['goal'], parse_mode='Markdown')
    elif message.text == '🚀 Как я пришел в IT':
        bot.send_message(message.chat.id, CONTENT['history'], parse_mode='Markdown')
    elif message.text == '🧠 Мой ментор':
        bot.send_message(message.chat.id, CONTENT['mentor'], parse_mode='Markdown')
    elif message.text == '📈 Точка А → Точка Б':
        bot.send_message(message.chat.id, CONTENT['progress'], parse_mode='Markdown')
    elif message.text == '🎸 Хобби':
        bot.send_message(message.chat.id, CONTENT['hobbies'], parse_mode='Markdown')
    elif message.text == '💻 Мои работы':
        bot.send_message(message.chat.id, CONTENT['works'], parse_mode='Markdown')
    elif message.text == '🔗 GitHub':
        bot.send_message(message.chat.id, CONTENT['github'], parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, используйте кнопки меню или введите /help.')


# Запуск бота
# Запуск бота с защитой от падений
if __name__ == "__main__":
    import time

    print("Бот успешно запущен и готов к работе...")

    while True:
        try:
            # none_stop=True заставляет бота опрашивать сервер без остановки
            # timeout=60 задает время ожидания ответа от сервера
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            # Если упал интернет или легла телега — бот не выключится, а покажет ошибку
            print(f"[ERROR] Бот временно упал из-за ошибки: {e}")
            print("Перезапуск бота через 5 секунд...")
            time.sleep(5)
