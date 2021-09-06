import os

from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

bot = TeleBot(API_TOKEN)
