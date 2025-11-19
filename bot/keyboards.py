from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/addmeal'), KeyboardButton('/stats'))
    kb.add(KeyboardButton('/profile'), KeyboardButton('/setgoal'))
    return kb
