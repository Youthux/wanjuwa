from telegram.ext import Updater
from telegram import Update
from config import token
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, filters
from activity import *
from telegram.ext import ApplicationBuilder, CommandHandler

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: CallbackContext):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


async def update_token(update: Update, context: CallbackContext):
    logging.info('收到token: %s', context.args[0])
    context.bot_data['token'] = context.args[0]
    await context.bot.send_message(chat_id=update.effective_chat.id, text='更新成功')


async def activity(update: Update, context: CallbackContext):
    try:
        token = context.bot_data['token']
    except KeyError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='请先设置token')
        return
    try:
        userId = context.args[0]
    except IndexError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='请输入要查询的用户Id')
        return
    try:
        rows = context.args[1]
    except IndexError:
        rows = 100

    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='搜索最近{}场活动中，请稍后...'.format(rows))

        title = find_activity(token, userId, rows)
        for t in title:
           await context.bot.send_message(chat_id=update.effective_chat.id, text=t)
    except TokenInvalid as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='{},请重新输入token'.format(e.msg))
    except requests.exceptions.ConnectionError as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='连接超时，请重新查询')
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='查询失败'.format(e))


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    REQUEST_KWARGS = {
        'proxy_url': 'socks5h://127.0.0.1:1080/',
    }
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    update_handler = CommandHandler('token', update_token)
    application.add_handler(update_handler)

    activity_handler = CommandHandler('activity', activity)
    application.add_handler(activity_handler)

    application.run_polling()
