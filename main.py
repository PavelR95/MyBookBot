import os
import asyncio

from dotenv import load_dotenv
from aiohttp import web
from TgBot.tg_bot import TgBot
from data_base import DataBae


async def run_plugins(app):
    # Run Telegram Bot
    data_base = app['data_base']
    await data_base.connection()
    tgbot = app['tgbot']
    await tgbot.start()
    pass


async def tg_bot(request):
    print('NEW MESSAGE')
    tgbot = request.app['tgbot']
    data = await request.json()
    asyncio.create_task(tgbot.message(data))

    return web.Response(status=200)


def start_server():
    app = web.Application()
    # Add config env
    load_dotenv()
    app['webhook'] = os.getenv('webhook')
    app['token'] = os.getenv('tg_token')
    app['domain'] = os.getenv('domain')
    app['url_tg_api'] = os.getenv('url_tg_api') + app['token']

    # Run plugins
    app['tgbot'] = TgBot(app)
    app['data_base'] = DataBae(app)
    app.on_startup.append(run_plugins)

    # Add routers
    app.add_routes([web.post(app['webhook'], tg_bot)])

    # Run Server
    web.run_app(app, port=7070)


if __name__ == "__main__":
    start_server()
