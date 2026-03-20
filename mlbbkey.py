import random
import string
import os
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# ===== WEBKEEP ALIVE =====
app_web = Flask(__name__)
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

@app_web.route("/")
def home():
    return "Bot is online!"

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    Thread(target=lambda: app_web.run(host="0.0.0.0", port=port)).start()

# 🔐 Get token from ENV
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")

# 🔑 Generate random key
def generate_key():
    chars = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(chars) for _ in range(11))
    return f"Slider_{random_part}"

# 👋 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello welcome to our key generator!\n\nType /generate to generate key"
    )

# 🔑 Generate command with duration buttons
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Inline buttons for durations
    keyboard = [
        [
            InlineKeyboardButton("1d", callback_data="1d"),
            InlineKeyboardButton("3d", callback_data="3d"),
            InlineKeyboardButton("7d", callback_data="7d"),
            InlineKeyboardButton("30d", callback_data="30d"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Select the key duration:",
        reply_markup=reply_markup
    )

# 🛠 Callback for button presses
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge button press

    duration = query.data
    # Generate 11 random characters AFTER duration
    chars = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(chars) for _ in range(11))
    final_key = f"Slider_{duration}{random_part}"

    await query.edit_message_text(
        text=f"🔑 Your Generated Key:\n`{final_key}`",
        parse_mode="Markdown"
    )

# 🚀 Main app
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    keep_alive()
    main()
