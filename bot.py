# -*- coding: utf-8 -*-
# Pikabu chat bot
import logging
import random
import re

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import config
import db
import models


class Bot(object):
    def __init__(self):
        # Enable logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        self.TIME_TO_REPOST = dict()
        self.fochi_replyes = ["Ко ко ко", "Воу воу, палехчи паринь", "Смотрите все! Fochi бушует!",
                              "Слушайте его, он херни не скажет", "Круто сказанул, ыыыыы"]

        # boobs_channels = ['@superboobs', '@boobsChannel', '@boobsblog', '@BestTits']
        self.boobs_channels = ['@superboobs', '@BestTits', '@boobsblog']
        self.boobs_regexp = re.compile('(сис(ек|ьки|ечки|и|яндры))|(ти(тьки|течки|тюли|ти|тяндры))', re.IGNORECASE)

        self.ass_channels = ['@bigasianasses', '@BestAss']
        self.ass_regexp = re.compile('(поп(ка|ец))|(жоп(ка|ища|уля))', re.IGNORECASE)

        # init main logic
        self.bot_db = db.sql_database()
        models.create_tables(self.bot_db.get_engine())
        self.session = self.bot_db.get_session()

        self.updater = Updater(config.TOKEN)
        self.dp = self.updater.dispatcher
        self.dp.addHandler(CommandHandler("start", self.start))
        self.dp.addHandler(CommandHandler("users", self.users))
        self.dp.addHandler(CommandHandler("help", self.help))
        self.dp.addHandler(MessageHandler([Filters.text], self.echo))
        self.dp.addErrorHandler(self.error)

    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    def start(self, bot, update):
        bot.sendMessage(update.message.chat_id,
                        text='Здарова, бандиты! Меня зовут Бороздобородый, я буду вас развлекать.')

    def users(self, bot, update):
        if update.message.from_user.id == config.ADMIN_ID:
            session = self.bot_db.get_session()
            users = session.query(models.User).limit(20).all()
            if users is None:
                bot.sendMessage(update.message.chat_id,
                                text='Пока что нет пользователей в базе.')
            else:
                bot.sendMessage(update.message.chat_id,
                                text='\n'.join(map(str, users)))

    def help(self, bot, update):
        bot.sendMessage(update.message.chat_id, text='Help!')

    def echo(self, bot, update):
        user = self.__put_user_to_database(update)

        if self.boobs_regexp.match(update.message.text) is not None:
            bot.forwardMessage(chat_id=update.message.chat_id,
                               from_chat_id=self.boobs_channels[random.randint(0, len(self.boobs_channels) - 1)],
                               message_id=random.randint(1, 1000))
        if self.ass_regexp.match(update.message.text) is not None:
            bot.forwardMessage(chat_id=update.message.chat_id,
                               from_chat_id=self.ass_channels[random.randint(0, len(self.ass_channels) - 1)],
                               message_id=random.randint(1, 1000))
        elif update.message.from_user.username == "fochi_ip":
            if self.TIME_TO_REPOST.get(update.message.chat_id, 0) == 0:
                bot.sendMessage(update.message.chat_id,
                                text=self.fochi_replyes[random.randint(0, len(self.fochi_replyes) - 1)],
                                reply_to_message_id=update.message.message_id)
                self.TIME_TO_REPOST[update.message.chat_id] = random.randint(10, 50)
            else:
                self.TIME_TO_REPOST[update.message.chat_id] -= 1

    def error(self, bot, update, error):
        self.logger.warn('Ошибочка "%s"' % (error))

    def __put_user_to_database(self, update):
        user = models.User(update.message.from_user.id, update.message.from_user.username,
                           update.message.from_user.first_name, update.message.from_user.last_name,
                           update.message.from_user.type)
        self.session.merge(user)
        self.session.commit()

        return user


def main():
    bot = Bot()
    bot.updater.start_polling()
    bot.updater.idle()


if __name__ == '__main__':
    main()
