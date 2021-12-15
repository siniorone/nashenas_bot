from emoji import demojize, emojize
from telebot import types


def create_keyboard(*keys, row_width=2, resize_keyboard=True):
    """
    This function is in charge of producing new markup keyboards.
    """
    markup = types.ReplyKeyboardMarkup(
        row_width=row_width,
        resize_keyboard=resize_keyboard
    )
    keys = map(emojize, keys)
    buttons = map(types.KeyboardButton, keys)
    markup.add(*buttons)
    return markup