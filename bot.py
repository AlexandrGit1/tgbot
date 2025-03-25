from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
import requests

# Чтение токенов
try:
    tg_bot_token = open("token.txt").read().strip()
    openrouter_api_key = open("key.txt").read().strip()
except:
    print("Ошибка при чтении файлов с токенами")
    exit()

bot = Bot(token=tg_bot_token)
dp = Dispatcher()
router = Router()

def zapros(prompt):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemini-2.5-pro-exp-03-25:free",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        
        # Проверяем ответ
        data = response.json()
        if "choices" not in data:
            print("Ошибка: в ответе нет ключа 'choices'")
            print("Полный ответ API:", data)
            return "Произошла ошибка, попробуйте позже"
            
        return data["choices"][0]["message"]["content"]
        
    except Exception as e:
        print("Ошибка при запросе:", e)
        return "Не удалось обработать запрос"

@router.message(Command("start"))
async def start_command(message: Message):
    await message.reply("Привет! Напиши мне что-нибудь, и я отвечу.")

@router.message(Command("help"))
async def help_command(message: Message):
    await message.reply("Просто напиши сообщение - я отвечу!")

@router.message()
async def handle_message(message: Message):
    if not message.text:
        await message.reply("Отправьте текстовое сообщение")
        return

    await bot.send_chat_action(message.chat.id, "typing")
    bot_response = zapros(message.text)
    await message.reply(bot_response)

dp.include_router(router)

if __name__ == "__main__":
    dp.run_polling(bot)
