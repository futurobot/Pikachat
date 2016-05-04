# -*- coding: utf-8 -*-
# Pikabu chat bot
import logging

import config
import random
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

TIME_TO_REPOST = dict()
fochi_replyes = ["Ко ко ко", "Воу воу, палехчи паринь", "Смотрите все! Fochi бушует!",
                 "Слушайте его, он херни не скажет", "Круто сказанул, ыыыыы"]

# boobs_channels = ['@superboobs', '@boobsChannel', '@boobsblog', '@BestTits']
boobs_channels = ['@superboobs', '@BestTits', '@boobsblog']
boobs_regexp = re.compile('(сис(ек|ьки|ечки|и|яндры))|(ти(тьки|течки|тюли|ти))')


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Здарова, бандиты! Меня зовут Бороздобородый, я буду вас развлекать.')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    if boobs_regexp.match(update.message.text) is not None:
        bot.forwardMessage(chat_id=update.message.chat_id,
                           from_chat_id=boobs_channels[random.randint(0, len(boobs_channels) - 1)],
                           message_id=random.randint(1, 1000))
    elif update.message.from_user.username == "fochi_ip":
        if TIME_TO_REPOST.get(update.message.chat_id, 0) == 0:
            bot.sendMessage(update.message.chat_id, text=fochi_replyes[random.randint(0, len(fochi_replyes) - 1)],
                            reply_to_message_id=update.message.message_id)
            TIME_TO_REPOST[update.message.chat_id] = random.randint(10, 50)
        else:
            TIME_TO_REPOST[update.message.chat_id] -= 1


def error(bot, update, error):
    logger.warn('Ошибочка "%s"' % (error))


def main():
    updater = Updater(config.TOKEN)
    dp = updater.dispatcher
    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))
    dp.addHandler(MessageHandler([Filters.text], echo))
    dp.addErrorHandler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
