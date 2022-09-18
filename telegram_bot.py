from ast import Call
from sympy import im
from telegram.ext import Updater
from telegram import Update
from config import token
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from activity import *

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

REQUEST_KWARGS={
    'proxy_url': 'socks5h://127.0.0.1:1080/',
}

updater = Updater(token=token, use_context=True, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    
def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
        
def update_token(update: Update, context: CallbackContext):
    logging.info('收到token: %s', context.args[0])
    context.bot_data['token'] = context.args[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text='更新成功')   
    
def activity(update: Update, context: CallbackContext):
    try:
        token = context.bot_data['token']
    except KeyError:
        context.bot.send_message(chat_id=update.effective_chat.id, text='请先设置token')
        return
    userId = context.args[0]
    if not userId:
        context.bot.send_message(chat_id=update.effective_chat.id, text='请输入要查询的用户Id')
        
    try:
        title = find_activity(token, userId)
        context.bot.send_message(chat_id=update.effective_chat.id, text='{}报名了活动：{}'.format(userId, title))
    except NotFound as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=e.msg)
    except TokenInvalid as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text='{},请重新输入token'.format(e.msg))
        
        
    
    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

update_handler = CommandHandler('token', update_token)
dispatcher.add_handler(update_handler)

activity_handler = CommandHandler('activity', activity)
dispatcher.add_handler(activity_handler)

updater.start_polling()