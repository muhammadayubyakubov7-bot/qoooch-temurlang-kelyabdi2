from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_btn():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="✍️ Ro'yhatdan o'tish", callback_data="register_btn")
    )
    return markup
