from emoji import emojize
from loguru import logger

from src.utils.constant import keyboards
from src.utils.filters import IsAdmin
from utils.bot import bot


class Bot(object):
    """
    This class is a template for building a telegram bot.
    """

    def __init__(self, bot):
        logger.info("Bot Started ...")
        # Create Bot
        self.bot = bot
        # Add custom filter
        self.bot.add_custom_filter(IsAdmin())
        # Register Handlers
        self.handlers()
        # Run the bot
        logger.info("Bot is running ...")
        self.bot.infinity_polling()

    def handlers(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            """
            A welcome message is sent to the user
            who has just hit the bot start button.
            """
            logger.info(f"Sending message to user = {message.from_user.id}")
            self.bot.reply_to(message, f"Hello {message.chat.first_name}!")

        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(message.chat.id, 'You are admin!')

        @self.bot.message_handler(func=lambda m: True)
        def echo_all(message):
            """
            The user message is automatically returned.
            the appropriate keyboard is then sent the user.
            """
            logger.info(f"Sending message to user = {message.from_user.id}")
            self.send_message(
                message.chat.id,
                message.text,
                reply_markup=keyboards.main,
            )

    def send_message(self, chat_id, text, reply_markup=None, is_emoji=True):
        if is_emoji:
            text = emojize(text)
        self.bot.send_message(chat_id, text, reply_markup)
# Set your telegram bot token as environment variable `TELEGRAM_BOT_TOKEN`
# export TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>


if __name__ == "__main__":
    bot = Bot(bot)
    logger.info("Done!")
