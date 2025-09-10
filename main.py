import requests
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command

# --- Конфиги ---
TELEGRAM_TOKEN = "723599629:AAHY-BnqxjcfqVCBPlLzShzHzx0yuTh17O4"
DIFY_API_KEY = "app-5wIRMmbNQl4E0aoaKLf2YgHd"
DIFY_BASE_URL = "https://api.dify.ai/v1"

# --- Инициализация ---
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Хранилище для диалогов
user_conversations = {}

def ask_dify(query: str, user_id: str = "telegram_user") -> str:
    url = f"{DIFY_BASE_URL}/chat-messages"
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "user": user_id
    }

    # добавляем conversation_id только если он есть
    if user_id in user_conversations:
        payload["conversation_id"] = user_conversations[user_id]

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # сохраняем conversation_id, если он пришёл
        if "conversation_id" in data:
            user_conversations[user_id] = data["conversation_id"]

        return data.get("answer", "❌ Нет ответа от Dify")
    else:
        return f"⚠️ Ошибка Dify: {response.text}"


# Хэндлер команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет 👋 Я бот, работаю только для Абдуллаха. Напиши что-нибудь!")


# Хэндлер любых сообщений
@router.message()
async def handle_message(message: Message):
    user_text = message.text
    reply = ask_dify(user_text, str(message.from_user.id))
    await message.answer(reply)


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
