from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
import requests

# Токены
tg_bot_token = "7543673168:AAFzOnN2eQPJrRGdzrJF-LZ31ewfNZBzhuI"
openrouter_api_key = "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"

# Инициализация бота и диспетчера
bot = Bot(token=tg_bot_token)
dp = Dispatcher()

# Создаем роутер для обработчиков
router = Router()

# Функция для отправки запросов к OpenRouter (Gemini Pro 2.0 Experimental)
def zapros(prompt):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemini-pro",  # Указываем модель Gemini Pro 2.0 Experimental
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return response.json()["choices"][0]["message"]["content"]

# Обработчик команды /start
@router.message(Command("start"))
async def start_command(message: Message):
    await message.reply("Привет, я крутой бот! Напиши мне что-нибудь, и я отвечу.")

# Обработчик команды /help
@router.message(Command("help"))
async def help_command(message: Message):
    await message.reply("Просто напиши мне сообщение, а я дам ответ!")

# Обработчик текстовых сообщений
@router.message()
async def handle_message(message: Message):
    user_message = message.text  # Получаем текст сообщения от пользователя

    # Отправка запроса к LLM
    bot_response = zapros(user_message)
    await message.reply(bot_response)

# Подключаем роутер к диспетчеру
dp.include_router(router)

# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot)
