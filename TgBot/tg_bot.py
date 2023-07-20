from TgBot.tg_bot_api import TgBotApi
from TgBot.tg_user_api import TgUserApi


class TgBot:

    def __init__(self, app):
        self.app = app
        self.tg_bot_api = TgBotApi(app)
        pass

    async def start(self):
        res = await self.tg_bot_api.check_bot()
        # INFO
        print('BOT ID: ' + str(res['id']) + '\n'
              + 'BOT NAME: ' + str(res['first_name']) + '\n'
              + 'USER: ' + str(res['username']) + '\n'
              )
        await self.tg_bot_api.set_url_webhook()
        res = await self.tg_bot_api.check_webhook()
        if res:
            print('WEBHOOK INFO')
            print('URL: ' + str(res['url']) + '\n'
                  + 'IP CONNECTION: ' + str(res['ip_address']) + '\n'
                  )
        pass

    async def message(self, data):
        message = data['message']

        user = TgUserApi(
            self.app,
            message['from']['id'],
            message['from']['first_name'],
            message['text']
        )
        text = await user.command()
        answer = {
            'chat_id': message['chat']['id'],
            'text': text
        }
        await self.tg_bot_api.send_message(answer)
        pass
