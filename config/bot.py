from telebot.types import BotCommand
from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

from config.settings import API_TOKEN

bot = TeleBot(API_TOKEN, state_storage=StateMemoryStorage())
bot.add_custom_filter(custom_filter=custom_filters.StateFilter(bot))

bot.set_my_commands(commands=[
    BotCommand(command="start", description="Botni qayta yuklash")
])
