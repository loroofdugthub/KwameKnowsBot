from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Bot Token
BOT_TOKEN = "7500779185:AAHSiuetI7kdLSomu-d9WZS1nQftZDJd9LA"

# Your MoMo number
MOMO_NUMBER = "+233240438094"

# Simple database to store who has paid (in memory)
ad_free_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in ad_free_users:
        await update.message.reply_text(
            f"Hi {user.first_name}! KwameKnowsBot gives you insights, jokes, and more!\n\n"
            "Ads are shown by default. To remove ads, pay to MTN MoMo number:\n"
            f"{MOMO_NUMBER}\n\n"
            "After payment, reply with 'Paid'."
        )
    else:
        await update.message.reply_text(f"Welcome back {user.first_name}! You’re ad-free. Ask me anything!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    if "paid" in text:
        ad_free_users.add(user_id)
        await update.message.reply_text("Payment confirmed! Ads removed. Thank you!")
        return

    if user_id in ad_free_users:
        await update.message.reply_text(f"Here’s your response with no ads: {text[::-1]}")
    else:
        await update.message.reply_text(
            f"Ad: KwameKnowsBot is brought to you by Wisdom Ltd!\n\nResponse: {text[::-1]}"
        )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
