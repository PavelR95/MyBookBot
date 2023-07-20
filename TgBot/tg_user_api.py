class TgUserApi:

    def __init__(self, app, user_id, name, text):
        self.app = app
        self.user_id = user_id
        self.name = name
        self.text = text
        self.last_command = None
        self.data_base = app['data_base']
        self.commands = {
            '/start': self.start,
            '/help': self.help,
            '/create_reminder': self.create_reminder,
            '/show_reminder': self.show_reminder
        }

    async def start(self):
        text = 'Приветствую, ' + self.name + '!' + '\n' + 'Введите /help для просмотра доступных команд.'
        return text

    @staticmethod
    async def help():
        text = (
                'Доступны следующие команды:' + '\n'
                + '/help - просмотр доступных команд.' + '\n'
                + '/create_reminder' + '\n'
                + '/show_reminder' + '\n'
        )
        return text

    async def create_reminder(self):
        if self.text == '/create_reminder':
            await self.data_base.update_last_command(self.user_id, '/create_reminder')
            return 'Введите дату в формате д.м.г (хх.хх.хх) и текст задачи' + '\n' \
                + 'Пример: 01.01.01 Проверить задачи в MyBooKBot' + '\n' \
                + 'для возврата введите /return'
        if self.text == '/return':
            await self.data_base.update_last_command(self.user_id, None)
            return await self.help()

        reminder = (self.user_id, self.text[0:8], self.text[9:])
        await self.data_base.add_reminder(reminder)
        await self.data_base.update_last_command(self.user_id, None)
        return 'Напоминание создано'

    async def show_reminder(self):
        data = await self.data_base.get_reminder(self.user_id)
        print(data)
        pass

    async def get_user(self):
        data = await self.data_base.get_user(self.user_id)
        if data:
            print('get user ok')
            return data
        user = (self.user_id, self.name, None)
        print('add new user')
        await self.data_base.add_user(user)
        return data

    async def command(self):
        data = await self.get_user()
        if data:
            print(data)
            self.last_command = data[2]
            if self.last_command is not None:
                command = self.commands.get(self.last_command, None)
                return await command()
        command = self.commands.get(self.text, None)
        if command:
            return await command()
        return 'No command'
