from emoji import emojize
from loguru import logger

from src.utils.constant import keyboards, keys, states
from src.utils.filters import IsAdmin
from src.utils.db import db
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
            logger.info(
                f"Sending Welcome Message to user = {message.from_user.id}"
            )
            self.send_message(
                message.chat.id,
                f"Hello <strong>{message.chat.first_name}</strong>!",
                reply_markup=keyboards.main
            )
            db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': message.json},
                upsert=True
            )
            self.update_status(message.chat.id, states.main)

        @self.bot.message_handler(regexp=keys.random_connect)
        def connect_to_stranger(message):
            logger.info(f"Connecting {message.from_user.id} to Random Stranger...")
            self.send_message(
                message.chat.id,
                ':people_hugging: Connecting to Random Stranger...',
                reply_markup=keyboards.exit
            )
            self.update_status(message.chat.id, states.random_connect)
            other_user = db.users.find_one(
                {
                    'chat.id': {'$ne': message.chat.id},
                    'states': states.random_connect
                }
            )
            if not other_user:
                return
            print(other_user)
            self.update_status(other_user['chat']['id'], states.connected)
            self.update_status(message.chat.id, states.connected)
            self.update_db(other_user['chat']['id'], 'connected_to', message.chat.id)
            self.update_db(message.chat.id, 'connected_to', other_user['chat']['id'])
            self.send_message(
                message.chat.id,
                f"You are connected to user {other_user['chat']['id']}",
                reply_markup=keyboards.exit
            )
            self.send_message(
                other_user['chat']['id'],
                f"You are connected to user {message.chat.id}",
                reply_markup=keyboards.exit
            )

        @self.bot.message_handler(regexp=keys.exit)
        def discard_connection(message):
            logger.info("Discarding the connection...")
            self.send_message(
                message.chat.id,
                ':cross_mark: Discarding the connection......',
                reply_markup=keyboards.main,
            )
            user = db.users.find_one(
                {'chat.id': message.chat.id}
            )
            if user['states'] == states.connected:
                self.update_status(user['connected_to'], states.main)
                self.update_db(user['connected_to'], 'connected_to', None)
            self.update_status(message.chat.id, states.main)
            self.update_db(message.chat.id, 'connected_to', None)

        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(message.chat.id, 'You are admin!')

        @self.bot.message_handler(func=lambda m: True)
        def echo(message):
            """
            The user message is automatically returned.
            the appropriate keyboard is then sent the user.
            """
            user = db.users.find_one(
                {'chat.id': message.chat.id}
            )
            if user['states'] == states.connected:
                logger.info(f"Sending message to user = {user['connected_to']}")
                self.send_message(
                    user['connected_to'],
                    message.text,
                    reply_markup=keyboards.exit,
                )

    def send_message(self, chat_id, text, reply_markup=None, is_emoji=True):
        if is_emoji:
            text = emojize(text)
        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

    def update_status(self, chat_id, state):
        db.users.update_one(
                {'chat.id': chat_id},
                {'$set': {'states': state}},
                upsert=True
            )

    def update_db(self, chat_id, key, value):
        db.users.update_one(
                {'chat.id': chat_id},
                {'$set': {key: value}},
                upsert=True
            )
# Set your telegram bot token as environment variable `TELEGRAM_BOT_TOKEN`
# export TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>


if __name__ == "__main__":
    bot = Bot(bot)
    logger.info("Done!")
