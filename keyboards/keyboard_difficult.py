from aiogram import types

buttons = ["800", "900", "900", "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800", "1900",
           "2000",
           "2100", "2200", "2300", "2400", "2500", "2600", "2700", "2800", "2900", "3000", "3100", "3200", "3300",
           "3400", "3500"]

inline_buttons_diff = [types.InlineKeyboardButton(text=i, callback_data=f"diff_{i}") for i in buttons]
