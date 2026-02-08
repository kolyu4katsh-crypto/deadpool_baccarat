import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

TOKEN = "8316512949:AAHjer5xyDuE1M_OBoFVXVZ1_uvOxiNMEmM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище статистики
stats = {"win": 0, "loss": 0}
SUITS = ["♠️", "♥️", "♦️", "♣️"]

# Фразочки в стиле Уэйда Уилсона
QUOTES = [
    "Слушай сюда, сахарные трусики, ИИ подумал и решил...",
    "Если это не зайдет, я не виноват, это всё Фрэнсис!",
    "Моя интуиция подсказывает это (или это просто зуд в неположенном месте)...",
    "Ставь аккуратно, нам еще на чимичанги должно хватить!",
    "Вероятность успеха почти такая же, как то, что Росомаха меня обнимет."
]

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="⚔️ ТЫКНУТЬ В РАНДОМ ⚔️"))
    
    welcome = (
        "<b>🔴 КТО ЭТО ТУТ У НАС? СВЕЖЕЕ МЯСО!</b>\n"
        "────────────────────\n"
        "Я — <b>Baccarat Deadpool AI</b>, и я здесь, чтобы либо сделать тебя богатым, "
        "либо просто поржать, пока ты всё сливаешь. \n\n"
        "<i>P.S. Костюм не стираный, так что не прижимайся.</i>"
    )
    await message.answer(welcome, parse_mode="HTML", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "⚔️ ТЫКНУТЬ В РАНДОМ ⚔️")
async def send_prediction(message: types.Message):
    suit = random.choice(SUITS)
    conf = random.randint(10, 99)
    quote = random.choice(QUOTES)
    
    # Эффект "думающего" Дэдпула
    status_msg = await message.answer("📽 <i>Заряжаю пистолеты и считаю карты...</i>")
    await asyncio.sleep(1.5)
    
    res_text = (
        f"<b>🔴 {quote}</b>\n"
        "────────────────────\n"
        f"<b>КАРТА:</b> {suit}\n"
        f"<b>ДОГОН:</b> 1 игра (или до смерти)\n"
        "────────────────────\n"
        f"<b>УВЕРЕННОСТЬ:</b> {conf}% 🌶\n"
        f"<b>УСПЕХИ:</b> ✅ {stats['win']} | ❌ {stats['loss']}"
    )
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Я БОГАТ! ✅", callback_data="stat_win")
    kb.button(text="ВСЁ ПЛОХО... ❌", callback_data="stat_loss")
    
    await status_msg.edit_text(res_text, parse_mode="HTML", reply_markup=kb.as_markup())

@dp.callback_query(F.data.startswith("stat_"))
async def update_stats(callback: types.CallbackQuery):
    if callback.data == "stat_win":
        stats["win"] += 1
        msg = "Красавчик! Купи мне единорога! 🦄"
    else:
        stats["loss"] += 1
        msg = "Ну всё, теперь мы оба бомжи. Пойду чистить туалеты... 💩"
    
    await callback.answer(msg)
    await callback.message.edit_reply_markup(reply_markup=None)
    # Обновляем сообщение, чтобы показать финальную статку
    await callback.message.answer(f"📊 <b>Дэдпул-стата:</b> {stats['win']} зашло / {stats['loss']} мимо.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
