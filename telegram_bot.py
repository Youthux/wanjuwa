from telegram import Update
from config import Config
from telegram.ext import ApplicationBuilder,CommandHandler, MessageHandler, filters, PicklePersistence,CallbackContext
from activity import *

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
    context.bot_data['token_expired'] = False
    await context.bot.send_message(chat_id=update.effective_chat.id, text='更新成功')


async def activity(update: Update, context: CallbackContext):
    try:
        token = context.bot_data.get('token')
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

async def heart(context: CallbackContext):
    admin_id = Config.get('admin_id')
    if context.bot_data.get('token_expired') == True:
        return
    try:
        token = context.bot_data.get('token')
        
        heart_beat(token)
    except KeyError:
        context.bot_data['token_expired'] = True
        await context.bot.send_message(
            chat_id=admin_id, text='请先设置token')
    except TokenInvalid:
        context.bot_data['token_expired'] = True
        await context.bot.send_message(
            chat_id=admin_id, text='token失效, 请重新设置token')


if __name__ == '__main__':
    
    bot_token = Config.get('bot_token')
    proxy_url = Config.get('proxy_url')
    
    persistence = PicklePersistence(filepath='bot.pickle')
    applicationBuilder = ApplicationBuilder().token(bot_token).persistence(persistence)
    if proxy_url:
        applicationBuilder = applicationBuilder.proxy_url(proxy_url).get_updates_proxy_url(proxy_url)
    application = applicationBuilder.build()
    
    application.job_queue.run_repeating(callback=heart, interval=300, first=0)
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    update_handler = CommandHandler('token', update_token)
    application.add_handler(update_handler)

    activity_handler = CommandHandler('activity', activity)
    application.add_handler(activity_handler)

    application.run_polling()
