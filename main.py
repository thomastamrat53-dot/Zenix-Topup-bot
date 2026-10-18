import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.request import HTTPXRequest

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = "8938472378:AAG89zM6UzIglSsktfI88FTp1Al3iNLpPXY"
SUPPORT_CHANNEL = "https://t.me/zenixtopup1"
SUPPORT_USERNAME = "https://t.me/TOPMAX1505"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🛒 **ZENIX TOPUP**\n\n"
        "⚡ **24/7 AUTOMATED TOP-UP SERVICE** 🟢\n\n"
        "💎 **WELCOME TO ZENIX TOP-UP BOT** ✨\n\n"
        "👇 **PLEASE CHOOSE AN OPTION BELOW:**"
    )
    
    keyboard = [
        [InlineKeyboardButton("🕹️ Items (Games)", callback_data="items_menu")],
        [InlineKeyboardButton("💰 My Balance", callback_data="my_balance")],
        [InlineKeyboardButton("🧾 My Orders", callback_data="my_orders")],
        [InlineKeyboardButton("📢 Our Channel", url=SUPPORT_CHANNEL)],
        [InlineKeyboardButton("🎧 Contact Support", url=SUPPORT_USERNAME)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        try:
            await update.callback_query.message.edit_text(
                text=welcome_text, 
                reply_markup=reply_markup, 
                parse_mode="Markdown"
            )
        except Exception:
            pass
    else:
        await update.message.reply_text(
            text=welcome_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    back_keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
    back_markup = InlineKeyboardMarkup(back_keyboard)

    async def edit_msg(text, markup):
        try:
            await query.message.edit_text(text=text, reply_markup=markup, parse_mode="Markdown")
        except Exception:
            pass

    if query.data == "items_menu":
        games_keyboard = [
            [InlineKeyboardButton("🔥 Free Fire Top-up", callback_data="free_fire")],
            [InlineKeyboardButton("⚡ PUBG UC Top-up", callback_data="pubg_uc")],
            [InlineKeyboardButton("🎯 Call of Duty (CP) Top-up", callback_data="call_of_duty")],
            [InlineKeyboardButton("💎 Blood Strike Top-up", callback_data="blood_strike")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
        ]
        await edit_msg("🎮 **AVAILABLE GAMES (ITEMS)**\n\n👇 ጨዋታ ይምረጡ:", InlineKeyboardMarkup(games_keyboard))

    elif query.data in ["free_fire", "pubg_uc", "call_of_duty", "blood_strike"]:
        context.user_data["selected_game"] = query.data
        game_name = query.data.upper().replace('_', ' ')
        await edit_msg(
            f"🎯 **{game_name} TOP-UP**\n\n🆔 Please enter your 8-12 digit Player ID / የጌም 🆔 ቁጥርዎን ይላኩ:",
            back_markup
        )

    elif query.data == "my_balance":
        dashboard_text = (
            "💳 **USER DASHBOARD - BALANCE**\n\n"
            f"👤 **User:** {query.from_user.first_name}\n"
            f"🆔 **Telegram ID:** `{query.from_user.id}`\n"
            "💰 **Current Balance:** `0.00 ETB` 🇪🇹"
        )
        await edit_msg(dashboard_text, back_markup)

    elif query.data == "my_orders":
        orders_text = (
            "🧾 **YOUR ORDERS HISTORY**\n\n"
            "ℹ️ እስካሁን ያደረጉት ትዕዛዝ የለም።"
        )
        await edit_msg(orders_text, back_markup)

    elif query.data == "back_to_menu":
        await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response_text = (
        f"✅ **Player ID Received:** `{user_text}`\n\n"
        "⏳ **Please complete your payment within 5 minutes!**\n"
        "⏱ **የክፍያ ጊዜ ገደብ:** 5 ደቂቃ (5 Minutes remaining)\n\n"
        "🚀 **Processing your automatic top-up request...**"
    )
    await update.message.reply_text(response_text, parse_mode="Markdown")

if __name__ == "__main__":
    request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    app = ApplicationBuilder().token(BOT_TOKEN).request(request).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("ቦቱ በሰላም 24/7 እየሰራ ነው...")
    app.run_polling(drop_pending_updates=True)
