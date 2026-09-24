import os
import sys
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Configure timestamped stdout logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("telegram_bot")


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_info = f"{user.username} ({user.id})" if user else "Unknown User"
    logger.info("Received /start command from %s", user_info)
    if update.message:
        await update.message.reply_text("Hello! Bot is live and running on your custom dashboard!")


async def ping_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_info = f"{user.username} ({user.id})" if user else "Unknown User"
    logger.info("Received /ping command from %s", user_info)
    if update.message:
        await update.message.reply_text("Pong! System status is healthy.")


async def log_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_info = f"{user.username} ({user.id})" if user else "Unknown User"
    text = update.message.text if update.message else "<non-text>"
    logger.info("Received message from %s: %s", user_info, text)


def main() -> None:
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("BOT_TOKEN environment variable is missing. Exiting.")
        sys.exit(1)

    logger.info("Initializing Telegram Bot...")
    application = Application.builder().token(bot_token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("ping", ping_handler))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, log_message_handler))

    logger.info("Bot started successfully. Listening for incoming messages...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()