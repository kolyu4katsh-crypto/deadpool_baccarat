import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

TOKEN = "8316512949:AAHjer5xyDuE1M_OBoFVXVZ1_uvOxiNMEmM"
# Твоя картинка
PHOTO_URL = "https://raw.githubusercontent.com/kolyu4katsh-crypto/deadpool_baccarat/main/grok_image_1770572447691.jpg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище статистики (будет работать пока запущен бот)
stats = {"win": 0, "loss": 0}
SUITS = ["♠️", "♥️", "♦️", "♣️"]

QUOTES = [
    "Слушай сюда, сахарные трусики, ИИ подумал и решил...",
    "Если это не зайдет, я не виноват, это всё Фрэнсис!",
    "Моя интуиция подсказывает это (или это просто зуд в неположенном месте)...",
    "Ставь аккуратно, нам еще на чимичанги должно хватить!",
    "Вероятность успеха почти такая же, как то, что Росомаха меня обнимет.",
    "Карты не врут, в отличие от моего бывшего пластического хирурга!",
    "Ставь всё! Шучу, не будь как Логан, думай головой."
]

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="⚔️ ТЫКНУТЬ В РАНДОМ ⚔️"))
    
    welcome = (
        "<b>🔴 КТО ЭТО ТУТ У НАС? СВЕЖЕЕ МЯСО!</b>\n"
        "────────────────────\n"
        "Я — <b>Baccarat Deadpool AI</b>.\n\n"
        "<i>P.S. Костюм не стираный, так что не прижимайся.</i>"
    )
    # Картинка при старте
    await message.answer_photo(
        photo=PHOTO_URL, 
        caption=welcome, 
        parse_mode="HTML", 
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@dp.message(F.text == "⚔️ ТЫКНУТЬ В РАНДОМ ⚔️")
async def send_prediction(message: types.Message):
    suit = random.choice(SUITS)
    conf = random.randint(10, 99)
    quote = random.choice(QUOTES)
    
    # Эффект загрузки (как в оригинале)
    status_msg = await message.answer("📽 <i>Заряжаю пистолеты и считаю карты...</i>", parse_mode="HTML")
    await asyncio.sleep(1.5)
    await status_msg.delete()
    
    res_text = (
        f"<b>🔴 {quote}</b>\n"
        "────────────────────\n"
        f"<b>КАРТА:</b> {suit}\n"
        f"<b>ДОГОН:</b> 1 игра\n"
        "────────────────────\n"
        f"<b>УВЕРЕННОСТЬ:</b> {conf}% 🌶\n"
        f"<b>УСПЕХИ:</b> ✅ {stats['win']} | ❌ {stats['loss']}"
    )
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Я БОГАТ! ✅", callback_data="stat_win")
    kb.button(text="ВСЁ ПЛОХО... ❌", callback_data="stat_loss")
    
    # Картинка вместе с прогнозом
    await message.answer_photo(
        photo=PHOTO_URL,
        caption=res_text,
        parse_mode="HTML",
        reply_markup=kb.as_markup()
    )

@dp.callback_query(F.data.startswith("stat_"))
async def update_stats(callback: types.CallbackQuery):
    # Обновляем цифры
    if callback.data == "stat_win":
        stats["win"] += 1
        msg = "Красавчик! 🦄"
    else:
        stats["loss"] += 1
        msg = "💩 Бывает..."

    # Вырезаем старую цитату из текста, чтобы обновить только статистику
    current_caption = callback.message.caption.split("УСПЕХИ:")[0]
    new_caption = f"{current_caption}УСПЕХИ: ✅ {stats['win']} | ❌ {stats['loss']}"

    # Редактируем старое сообщение (меняем текст статки и убираем кнопки)
    await callback.message.edit_caption(
        caption=new_caption,
        parse_mode="HTML",
        reply_markup=None
    )
    await callback.answer(msg)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
