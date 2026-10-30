import os
import logging
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.request import HTTPXRequest

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- RENDER HEALTH CHECK SERVER ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Zenix Top-Up Bot is alive and running 24/7!")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"Health check server listening on port {port}")
    server.serve_forever()
# ----------------------------------

BOT_TOKEN = "8938472378:AAEQV-Kaxjz-x6pvSWti-EynSrrM72Jpg8s"
SUPPORT_CHANNEL = "https://t.me/zenixtopup1"
SUPPORT_USERNAME = "https://t.me/Zenixsupport12"

WELCOME_PHOTO_URL = "https://i.ibb.co/L50nLpD/IMG-20261017-163743-753.jpg" 
FF_PHOTO_URL = "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=1000"
PUBG_PHOTO_URL = "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?q=80&w=1000"
COD_PHOTO_URL = "https://images.unsplash.com/photo-1511512578047-dfb367046420?q=80&w=1000"

CBE_ACCOUNT = "1000123456789 (Zenix TopUp)"
TELEBIRR_ACCOUNT = "0912345678 (Zenix TopUp)"

FF_PACKAGES = {
    "ff_100": {"name": "100 Diamonds", "price": "230 ETB"},
    "ff_310": {"name": "310 Diamonds", "price": "640 ETB"},
    "ff_520": {"name": "520 Diamonds", "price": "970 ETB"},
    "ff_1060": {"name": "1060 Diamonds", "price": "1,910 ETB"},
    "ff_2180": {"name": "2180 Diamonds", "price": "3,900 ETB"},
}

PUBG_PACKAGES = {
    "pubg_30": {"name": "30 UC", "price": "105 ETB"},
    "pubg_60": {"name": "60 UC", "price": "180 ETB"},
    "pubg_300": {"name": "300+25 UC", "price": "780 ETB"},
    "pubg_600": {"name": "600+60 UC", "price": "1,530 ETB"},
    "pubg_1500": {"name": "1500+300 UC", "price": "3,780 ETB"},
}

COD_PACKAGES = {
    "cod_160": {"name": "160 CP", "price": "180 ETB"},
    "cod_460": {"name": "460 CP", "price": "520 ETB"},
    "cod_960": {"name": "960 CP", "price": "1,010 ETB"},
    "cod_2600": {"name": "2600 CP", "price": "3,950 ETB"},
}

def get_free_fire_nickname(player_id: str) -> str:
    try:
        url = f"https://api.garena.com/freefire/id/{player_id}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return data.get("nickname", "Zenix Player")
    except Exception:
        pass
    return "Zenix Player"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🛒 **ZENIX TOPUP**\n\n"
        "⚡ **24/7 AUTOMATED TOP-UP SERVICE** 🟢\n\n"
        "💎 **WELCOME TO ZENIX TOP-UP BOT** ✨\n\n"
        "👇 **PLEASE CHOOSE AN OPTION BELOW:**"
    )
    
    keyboard = [
        [InlineKeyboardButton("🕹️ Items (Games)", callback_data="items_menu")],
        [InlineKeyboardButton("💳 My Balance", callback_data="my_balance")],
        [InlineKeyboardButton("🧾 My Orders", callback_data="my_orders")],
        [InlineKeyboardButton("📢 Our Channel", url=SUPPORT_CHANNEL)],
        [InlineKeyboardButton("🎧 Contact Support", url=SUPPORT_USERNAME)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_photo(
            photo=WELCOME_PHOTO_URL,
            caption=welcome_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif update.callback_query:
        try:
            await update.callback_query.message.delete()
        except Exception:
            pass
        await context.bot.send_photo(
            chat_id=update.callback_query.message.chat_id,
            photo=WELCOME_PHOTO_URL,
            caption=welcome_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    back_keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
    back_markup = InlineKeyboardMarkup(back_keyboard)

    if query.data == "items_menu":
        games_keyboard = [
            [InlineKeyboardButton("🔥 Free Fire Top-up", callback_data="game_free_fire")],
            [InlineKeyboardButton("⚡ PUBG UC Top-up", callback_data="game_pubg")],
            [InlineKeyboardButton("🎯 Call of Duty (CP) Top-up", callback_data="game_cod")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
        ]
        try:
            await query.message.delete()
        except Exception:
            pass
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="🎮 **AVAILABLE GAMES**\n\n👇 ይምረጡ:",
            reply_markup=InlineKeyboardMarkup(games_keyboard),
            parse_mode="Markdown"
        )

    elif query.data == "game_free_fire":
        buttons = [[InlineKeyboardButton(f"{v['name']} - {v['price']}", callback_data=f"pkg_{k}")] for k, v in FF_PACKAGES.items()]
        buttons.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")])
        try:
            await query.message.delete()
        except Exception:
            pass
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=FF_PHOTO_URL,
            caption="🔥 **FREE FIRE PACKAGES**\n\n👇 የዲያመንድ መጠን ይምረጡ:",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown"
        )

    elif query.data == "game_pubg":
        buttons = [[InlineKeyboardButton(f"{v['name']} - {v['price']}", callback_data=f"pkg_{k}")] for k, v in PUBG_PACKAGES.items()]
        buttons.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")])
        try:
            await query.message.delete()
        except Exception:
            pass
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=PUBG_PHOTO_URL,
            caption="⚡ **PUBG UC PACKAGES**\n\n👇 የ UC መጠን ይምረጡ:",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown"
        )

    elif query.data == "game_cod":
        buttons = [[InlineKeyboardButton(f"{v['name']} - {v['price']}", callback_data=f"pkg_{k}")] for k, v in COD_PACKAGES.items()]
        buttons.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")])
        try:
            await query.message.delete()
        except Exception:
            pass
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=COD_PHOTO_URL,
            caption="🎯 **CALL OF DUTY (
