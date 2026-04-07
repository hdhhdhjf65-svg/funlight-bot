import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, 
    InlineKeyboardButton, BotCommand, ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.session.aiohttp import AiohttpSession

# --- НАСТРОЙКИ ---
TOKEN = "8783709484:AAF1u8ROYoWmhsIFfW9-C7GLZ_27Xm4OgaM"
ADMIN_ID = 6765015248  

TG_CHANNEL_URL = "https://t.me/FunLight_13377" 
DISCORD_URL = "https://discord.gg/TnxkRqkdUC"
SERVER_IP = "funlightspace.gamepvp.ru"
FUNPAY_URL = "https://funpay.com/users/13256198/"

# Твои контакты
UKR_PAY_CONTACT = "@polihochkaa"
OTHER_PAY_CONTACT = "@TvoiDillivery"

# Настройка прокси (исправляет ошибку с image_ff9628.png)
session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

class SupportState(StatesGroup):
    waiting_for_issue = State()
    waiting_for_nickname = State()

# --- ПРАЙС-ЛИСТ ---
DONATES = {
    "Элита": 50, "Титан": 70, "Принц": 100, "Князь": 150, "Герцог": 200, "Спонсор": 400,
    "Разбан": 100, "Размут": 30, "Супер Донат Кейс": 100,
    "100к токенов": 30, "200к токенов": 60, "300к токенов": 100,
    "500к токенов": 150, "1.000.000 токенов": 300,
    "🥩 Дракону на покушать": 1, "🍗 Дракону на пк": 5, "🍖 Дракону на шмот": 10,
    "🧬 Дракону развитие": 15, "🔥 Дракону на мотивацию": 20, 
    "📈 Дракону на старания": 50, "👑 Дракон крутой чувак": 100
}

# --- МЕНЮ (Reply Keyboard) ---
def get_main_reply_kb():
    kb = [
        [KeyboardButton(text="🏠 /start"), KeyboardButton(text="🛡️ /help")],
        [KeyboardButton(text="📜 /rules"), KeyboardButton(text="🔗 /links")],
        [KeyboardButton(text="💎 /donate"), KeyboardButton(text="🐲 /Drakon")],
        [KeyboardButton(text="🛠️ /support")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# --- МАГАЗИН (Inline) ---
def main_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ ПРИВИЛЕГИИ ⭐", callback_data="none")],
        [InlineKeyboardButton(text="Элита-50", callback_data="buy_Элита"), InlineKeyboardButton(text="Титан-70", callback_data="buy_Титан")],
        [InlineKeyboardButton(text="Принц-100", callback_data="buy_Принц"), InlineKeyboardButton(text="Князь-150", callback_data="buy_Князь")],
        [InlineKeyboardButton(text="Герцог-200", callback_data="buy_Герцог"), InlineKeyboardButton(text="Спонсор-400", callback_data="buy_Спонсор")],
        
        [InlineKeyboardButton(text="📦 КЕЙСЫ И УСЛУГИ 🎁", callback_data="none")],
        [InlineKeyboardButton(text="Разбан-100", callback_data="buy_Разбан"), InlineKeyboardButton(text="Размут-30", callback_data="buy_Размут")],
        [InlineKeyboardButton(text="🎁 Супер Кейс-100", callback_data="buy_Супер Донат Кейс")],
        
        [InlineKeyboardButton(text="💰 ТОКЕНЫ 💰", callback_data="none")],
        [InlineKeyboardButton(text="100к-30", callback_data="buy_100к токенов"), InlineKeyboardButton(text="200к-60", callback_data="buy_200к токенов")],
        [InlineKeyboardButton(text="300к-100", callback_data="buy_300к токенов"), InlineKeyboardButton(text="500к-150", callback_data="buy_500к токенов")],
        [InlineKeyboardButton(text="💎 1.000.000-300", callback_data="buy_1.000.000 токенов")],
        
        [InlineKeyboardButton(text="💳 ОПЛАТА (ДРУГОЕ) 💳", callback_data="none")],
        [InlineKeyboardButton(text="🇺🇦 Оплата (УКР)", url=f"https://t.me/{UKR_PAY_CONTACT.replace('@','')}")],
        [InlineKeyboardButton(text="💠 Оплата (Другое)", url=f"https://t.me/{OTHER_PAY_CONTACT.replace('@','')}")],
        [InlineKeyboardButton(text="🌍 FunPay", url=FUNPAY_URL)],
        
        [InlineKeyboardButton(text="🛠️ Создать тикет", callback_data="support_ticket")]
    ])
    return kb

def drakon_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🥩 Покушать-1", callback_data="buy_🥩 Дракону на покушать")],
        [InlineKeyboardButton(text="🍗 На ПК-5", callback_data="buy_🍗 Дракону на пк")],
        [InlineKeyboardButton(text="🍖 На шмот-10", callback_data="buy_🍖 Дракону на шмот")],
        [InlineKeyboardButton(text="🧬 Развитие-15", callback_data="buy_🧬 Дракону развитие")],
        [InlineKeyboardButton(text="🔥 Мотивация-20", callback_data="buy_🔥 Дракону на мотивацию")],
        [InlineKeyboardButton(text="📈 Старания-50", callback_data="buy_📈 Дракону на старания")],
        [InlineKeyboardButton(text="👑 КРУТОЙ ЧУВАК-100", callback_data="buy_👑 Дракон крутой чувак")]
    ])
    return kb

# --- ОБРАБОТЧИКИ ---

@dp.message(Command("start"))
@dp.message(F.text == "🏠 /start")
async def cmd_start(message: types.Message):
    await message.answer(
        f"🤖 **FunLight Bot**\n📍 IP: `{SERVER_IP}`\n\nБот готов к работе! Магазин открыт ниже:",
        reply_markup=get_main_reply_kb(), parse_mode="Markdown"
    )
    await message.answer("🛒 **Магазин доната:**", reply_markup=main_menu_kb())

@dp.message(Command("help"))
@dp.message(F.text == "🛡️ /help")
async def cmd_help(message: types.Message):
    help_text = (
        "🤖 **Доступные команды:**\n\n"
        "🏠 `/start` — Главное меню и магазин\n"
        "🛡️ `/help` — Список всех команд\n"
        "📜 `/rules` — Правила проекта\n"
        "🔗 `/links` — Соцсети и IP сервера\n"
        "💎 `/donate` — Магазин привилегий\n"
        "🐲 `/Drakon` — Меню поддержки Дракона\n"
        "🛠️ `/support` — Связь с администрацией"
    )
    await message.answer(help_text, parse_mode="Markdown")

@dp.message(Command("rules"))
@dp.message(F.text == "📜 /rules")
async def cmd_rules(message: types.Message):
    rules_full = (
        "⚖️ **ПОЛНЫЙ СВОД ПРАВИЛ FUNLIGHT**\n\n"
        "1.1 Незнание правил не освобождает вас от ответственности;\n"
        "1.2 Начав играть на наших серверах, Вы автоматически подтверждаете своё согласие с данным сводом правил;\n"
        "1.3 Администратор вправе наказать игрока по причине, не указанной в настоящих правилах;\n"
        "1.4 Администрация не несет ответственности за временную или постоянную невозможность игры на сервере конкретным лицом или группой лиц;\n"
        "1.5 Администрация не несет ответственности за потерю игровых ценностей в следствии нарушения работоспособности сервера или его плагинов;\n"
        "1.6 Администрация не гарантирует работоспособность сервера, а также сохранность информации на нем и продолжение работы над ним;\n"
        "1.7 Администрация сервера не гарантирует надёжную работу в предоставлении услуг и сервисов, а также не несёт ответственность за ущерб, который может быть причинён пользователям вследствие сбоев в линиях связи, ошибочного использования предоставляемых услуг, дефектов программного обеспечения или других действий, которые могут привести к возникновению нежелательных ситуаций;\n"
        "1.8 Игроки обязаны соблюдать все правила;\n"
        "1.9 Администрация ведет логи всех действий игроков на сервере и всех сообщений чата;\n"
        "1.10 Администрация имеет право корректировать данный свод правил без уведомления игрока;"
    )
    await message.answer(rules_full, parse_mode="Markdown")

@dp.message(Command("donate"))
@dp.message(F.text == "💎 /donate")
async def cmd_donate(message: types.Message):
    await message.answer("🛒 **Магазин доната:**", reply_markup=main_menu_kb())

@dp.message(Command("Drakon"))
@dp.message(F.text == "🐲 /Drakon")
async def cmd_drakon(message: types.Message):
    await message.answer("🐲 **Меню Дракона:**", reply_markup=drakon_menu_kb())

@dp.message(Command("links"))
@dp.message(F.text == "🔗 /links")
async def cmd_links(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Канал", url=TG_CHANNEL_URL)],
        [InlineKeyboardButton(text="👾 Discord", url=DISCORD_URL)],
        [InlineKeyboardButton(text=f"📍 IP: {SERVER_IP}", callback_data="copy_ip")]
    ])
    await message.answer("🔗 **Наши ресурсы:**", reply_markup=kb)

@dp.callback_query(F.data == "copy_ip")
async def call_copy_ip(cb: types.CallbackQuery):
    await cb.answer(f"IP: {SERVER_IP} скопирован!", show_alert=True)

@dp.callback_query(F.data.startswith("buy_"))
async def send_invoice(callback: types.CallbackQuery):
    name = callback.data.split("_")[1]
    if name == "none": return
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=name,
        description=f"Покупка {name} на FunLight",
        payload=f"payload_{name}",
        currency="XTR",
        prices=[LabeledPrice(label=name, amount=DONATES[name])],
    )

@dp.pre_checkout_query()
async def process_pre_checkout(q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(q.id, ok=True)

@dp.message(F.successful_payment)
async def success_payment(message: types.Message, state: FSMContext):
    name = message.successful_payment.invoice_payload.replace("payload_", "")
    await state.update_data(bought_item=name)
    await message.answer(f"✅ Оплата {name} прошла! Введи свой НИК:")
    await state.set_state(SupportState.waiting_for_nickname)

@dp.message(SupportState.waiting_for_nickname)
async def process_nick(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item = data.get('bought_item')
    await message.answer(f"❤️ Спасибо! Админ выдаст `{item}` для `{message.text}`.")
    await bot.send_message(ADMIN_ID, f"💰 **ПОКУПКА:** `{message.text}` купил `{item}`")
    await state.clear()

@dp.message(Command("support"))
@dp.message(F.text == "🛠️ /support")
async def cmd_support_msg(message: types.Message, state: FSMContext):
    await message.answer("🛠️ Опиши проблему:")
    await state.set_state(SupportState.waiting_for_issue)

@dp.callback_query(F.data == "support_ticket")
async def call_support_btn(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.answer("🛠️ Опиши проблему:")
    await state.set_state(SupportState.waiting_for_issue)

@dp.message(SupportState.waiting_for_issue)
async def forward_to_admin(m: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"⚠️ **ТИКЕТ от {m.from_user.full_name}:**")
    await m.copy_to(ADMIN_ID)
    await m.answer("✅ Отправлено!")
    await state.clear()

async def main():
    # Регистрация команд в меню Telegram
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="donate", description="Магазин"),
        BotCommand(command="rules", description="Правила"),
        BotCommand(command="support", description="Поддержка")
    ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())