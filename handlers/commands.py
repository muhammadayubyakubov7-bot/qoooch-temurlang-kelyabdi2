from telebot.types import Message

from config.bot import bot
import buttons as btn


@bot.message_handler(commands=["start"])
def handler_commands(message: Message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        f"Assalomu aleykum {message.from_user.first_name} 👋\n"
        f"Ro'yhatdan o'tish tugmasini bosing",
        reply_markup=btn.start_btn()
    )
