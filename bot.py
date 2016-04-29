#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pikabu chat bot
import logging

import random
import config
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

TIME_TO_REPOST = dict()
fochi_replyes = ["Ко ко ко", "Воу воу, палехчи паринь", "Смотрите все! Fochi бушует!", "Слушайте его, он херни не скажет", "Круто сказанул, ыыыыы"]

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Здарова, бандиты! Меня зовут Бороздобородый, я буду вас развлекать.')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    username = update.message.from_user.username
    last_name = update.message.chat.last_name
    if username == "fochi_ip":
        if TIME_TO_REPOST.get(update.message.chat_id, 0) == 0:
            bot.sendMessage(update.message.chat_id, text=fochi_replyes[random.randint(0, len(fochi_replyes) - 1)], reply_to_message_id=update.message.message_id)
            TIME_TO_REPOST[update.message.chat_id] = random.randint(10, 50)
        else:
            TIME_TO_REPOST[update.message.chat_id] -= 1
    # elif username == "futurobot_tg":
    #     bot.sendMessage(update.message.chat_id, text=update.message.to_dict())
    #     if TIME_TO_REPOST.get(update.message.chat_id, 0) == 0:
    #         bot.sendMessage(update.message.chat_id, text=fochi_replyes[random.randint(0, len(fochi_replyes) - 1)], reply_to_message_id=update.message.message_id)
    #         TIME_TO_REPOST[update.message.chat_id] = random.randint(10, 50)
    #     else:
    #         TIME_TO_REPOST[update.message.chat_id] -= 1


def error(bot, update, error):
    logger.warn('Ошибочка "%s"' % (error))


def main():
    updater = Updater(config.TOKEN)
    dp = updater.dispatcher
    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))
    dp.addHandler(MessageHandler(filters.TEXT, echo))
    dp.addErrorHandler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
