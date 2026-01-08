import random
import string
from telegram.ext import Updater, CommandHandler

# ===== CONFIG =====
BOT_TOKEN = "8434663936:AAF7GDPG7TDCwdPvpT94eBGAkFfSoEe7tb8"
KEY_PREFIX = "Slider_"
RANDOM_LENGTH = 14
# ==================

def generate_random_key(length=14):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def newkey(update, context):
    random_part = generate_random_key(RANDOM_LENGTH)
    full_key = f"{KEY_PREFIX}{random_part}"

    update.message.reply_text(
        f"🔑 *NEW KEY GENERATED*\n\n`{full_key}`",
        parse_mode="Markdown"
    )

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("newkey", newkey))

    updater.start_polling()
    print("🤖 Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()