import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Твой токен
TOKEN = "8316512949:AAHjer5xyDuE1M_OBoFVXVZ1_uvOxiNMEmM"
# Ссылка на твоего Дэдпула за столом
PHOTO_URL = "https://raw.githubusercontent.com/kolyu4katsh-crypto/deadpool_baccarat/main/1000014268.jpg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

stats = {"win": 0, "loss": 0}
SUITS = ["♠️", "♥️", "♦️", "♣️"]

QUOTES = [
    "Слушай сюда, сахарные трусики, ИИ подумал и решил...",
    "Если это не зайдет, я не виноват, это всё Фрэнсис!",
    "Моя интуиция подсказывает это...",
    "Ставь аккуратно, нам еще на чимичанги должно хватить!",
    "Вероятность успеха почти как мой шанс подружиться с Логаном."
]

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="⚔️ ПОЛУЧИТЬ ПРОГНОЗ ⚔️"))
    welcome = "<b>🔴 КТО ЭТО ТУТ У НАС?</b>\n\nЯ — <b>Baccarat Deadpool AI</b>.\nБуду подглядывать в карты за тебя!"
    await message.answer_photo(photo=PHOTO_URL, caption=welcome, parse_mode="HTML", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "⚔️ ПОЛУЧИТЬ ПРОГНОЗ ⚔️")
async def send_prediction(message: types.Message):
    suit = random.choice(SUITS)
    conf = random.randint(10, 99)
    quote = random.choice(QUOTES)
    
    res_text = (
        f"<b>🔴 {quote}</b>\n"
        "────────────────────\n"
        f"<b>РЕЗУЛЬТАТ:</b> {suit}\n"
        f"<b>УВЕРЕННОСТЬ:</b> {conf}% 🌶\n"
        f"<b>УСПЕХИ:</b> ✅ {stats['win']} | ❌ {stats['loss']}"
    )
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Я БОГАТ! ✅", callback_data="stat_win")
    kb.button(text="ВСЁ ПЛОХО... ❌", callback_data="stat_loss")
    
    await message.answer_photo(photo=PHOTO_URL, caption=res_text, parse_mode="HTML", reply_markup=kb.as_markup())

@dp.callback_query(F.data.startswith("stat_"))
async def update_stats(callback: types.CallbackQuery):
    if callback.data == "stat_win":
        stats["win"] += 1
        msg = "Красавчик! 🦄"
    else:
        stats["loss"] += 1
        msg = "💩 Бывает..."
    await callback.answer(msg)
    await callback.message.answer(f"📊 <b>Стата:</b> {stats['win']} / {stats['loss']}", parse_mode="HTML")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
