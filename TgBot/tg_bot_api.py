import aiohttp
import json
import asyncio


class TgBotApi:
    pass

    def __init__(self, app):
        self.app = app
        self.url_tg_api = app['url_tg_api']
        self.webhook_url = app['domain'] + app['webhook']
        pass

    async def check_bot(self):
        print('CHECK BOT')
        url = self.url_tg_api + '/getMe'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print('resp status: ' + str(resp.status))
                    print('Connection status: ' + str(data['ok']))
                    return data['result']
            print('Error connection:', resp.status)
        pass

    async def check_webhook(self):
        print('CHECK WEBHOOK TG BOT')
        url = self.url_tg_api + '/getWebhookInfo'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print('resp status: ' + str(resp.status))
                    print('Connection status: ' + str(data['ok']))
                    return data['result']
            print('Error connection:', resp.status)
        pass

    async def set_url_webhook(self):
        print('SET URL WEBHOOK')
        url = self.url_tg_api + '/setWebhook' + '?url=' + self.webhook_url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    print('URL: OK', '\n')
                else:
                    print('Error:', resp.status, '\n')
        pass

    async def send_message(self, answer):
        print('SEND MESSAGE')
        url = self.url_tg_api + '/sendMessage'
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(answer), headers=headers) as resp:
                pass
