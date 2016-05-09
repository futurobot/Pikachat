# -*- coding: utf-8 -*-
# Pikabu chat bot
import logging

import config
import db
import models
import random
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


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

        self.updater = Updater(config.TOKEN)
        self.dp = self.updater.dispatcher
        self.dp.addHandler(CommandHandler("start", self.start))
        self.dp.addHandler(CommandHandler("users", self.users))
        self.dp.addHandler(CommandHandler("groups", self.groups))
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
            try:
                users = session.query(models.User).limit(20)
                if users is None:
                    bot.sendMessage(update.message.chat_id,
                                    text='Пока что нет пользователей в базе.')
                else:
                    response = ''
                    counter = 0
                    for user in users:
                        if counter > 0:
                            response += '\n'
                        response += "%s. %s(%s) Рейтинг: %s Группы: %s" % (
                            counter + 1, user.username, user.id, user.rating,
                            ','.join(['%s' % chat.id for chat in user.participate_in_chats]))
                        counter += 1
                    bot.sendMessage(update.message.chat_id,
                                    text=response)
            finally:
                session.close()

    def groups(self, bot, update):
        if update.message.from_user.id == config.ADMIN_ID:
            session = self.bot_db.get_session()
            try:
                groups = session.query(models.Chat).limit(20).all()
                if len(groups) == 0:
                    bot.sendMessage(update.message.chat_id,
                                    text='Пока что нет групп в базе.')
                else:
                    response = ''
                    counter = 0
                    for group in groups:
                        if counter > 0:
                            response += '\n'
                        response += "%s. %s(%s) Участники: %s" % (
                            counter + 1, group.title, group.id,
                            ','.join(['%s' % user.id for user in group.users_in_chat]))
                        counter += 1
                    bot.sendMessage(update.message.chat_id,
                                    text=response)
            finally:
                session.close()

    def help(self, bot, update):
        bot.sendMessage(update.message.chat_id, text='Help!')

    def echo(self, bot, update):
        chat, user = self._put_message_to_database(update)

        if user is not None:
            # handle possible rating stuff
            pass

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

    def _put_message_to_database(self, update):
        session = self.bot_db.get_session()
        try:
            chat = session.query(models.Chat).filter_by(id=update.message.chat_id).first()
            if chat is None:
                chat = models.Chat(update.message.chat.id, update.message.chat.type, update.message.chat.title,
                                   update.message.chat.first_name, update.message.chat.last_name,
                                   update.message.chat.username)
                session.add(chat)
            else:
                chat.id = update.message.chat.id
                chat.type = update.message.chat.type
                chat.title = update.message.chat.title
                chat.first_name = update.message.chat.first_name
                chat.last_name = update.message.chat.last_name
                chat.username = update.message.chat.username
                session.merge(chat)

            user = session.query(models.User).filter_by(id=update.message.from_user.id).first()
            if user is None:
                user = models.User(update.message.from_user.id, update.message.from_user.username,
                                   update.message.from_user.first_name, update.message.from_user.last_name,
                                   update.message.from_user.type)
                session.add(user)
            else:
                user.id = update.message.from_user.id
                user.username = update.message.from_user.username
                user.first_name = update.message.from_user.first_name
                user.last_name = update.message.from_user.last_name
                user.type = update.message.from_user.type
                session.merge(user)

            if chat not in user.participate_in_chats:
                user.participate_in_chats.append(chat)
            if user not in chat.users_in_chat:
                chat.users_in_chat.append(user)

            session.commit()
            return chat, user
        except Exception as e:
            print(str(e))
            session.rollback()
        finally:
            session.close()


def main():
    bot = Bot()
    bot.updater.start_polling()
    bot.updater.idle()


if __name__ == '__main__':
    main()
