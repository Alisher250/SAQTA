import os
import telebot

BOT_TOKEN = "6904214341:AAGH1op60Yf8jdiwTYN2B8ZH7gOYZEFTdCI"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Hello! Can I buy it?")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    sender_id = message.from_user.id  # Get the sender's ID
    print(f"Received message from {sender_id}: {message.text}")  # Print message with sender's ID


bot.infinity_polling()