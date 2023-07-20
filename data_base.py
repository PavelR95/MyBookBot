import aiosqlite


class DataBae:

    def __init__(self, app):
        self.app = app
        self.name_db = 'users.db'
        pass

    async def connect(self):
        con = await aiosqlite.connect(self.name_db)
        return con

    async def connection(self):
        con = await self.connect()
        await con.execute(
            'CREATE TABLE IF NOT EXISTS users '
            '(user_id text PRIMARY KEY, user_name text, last_command text)'
        )
        await con.commit()
        await con.execute(
            'CREATE TABLE IF NOT EXISTS reminder '
            '(id_reminder int PRIMARY KEY, user_id text, date text, reminder text)'
        )
        await con.commit()
        await con.close()

    async def get_user(self, user_id):
        con = await self.connect()
        cur = await con.execute("SELECT * FROM users WHERE user_id=:user_id", {'user_id': user_id})
        data = await cur.fetchone()
        await cur.close()
        await con.close()
        return data

    async def add_user(self, user):
        con = await self.connect()
        await con.execute('INSERT INTO users VALUES (?, ?, ?)', user)
        await con.commit()
        await con.close()

    async def update_last_command(self, user_id, last_command):
        con = await self.connect()
        await con.execute("UPDATE users set last_command = ? where user_id = ?", (last_command, user_id))
        await con.commit()
        await con.close()

    async def add_reminder(self, reminder):
        con = await self.connect()
        cur = await con.execute("SELECT MAX(id_reminder) FROM reminder")
        data = await cur.fetchone()
        await cur.close()
        if data[0] is None:
            value = (1, reminder[0], reminder[1], reminder[2])
        else:
            value = (data[0]+1, reminder[0], reminder[1], reminder[2])
        await con.execute('INSERT INTO reminder VALUES (?, ?, ?, ?)', value)
        await con.commit()
        await con.close()

    async def get_reminder(self, user_id):
        con = await self.connect()
        cursor = await con.execute("SELECT * FROM reminder WHERE user_id=:user_id", {'user_id': user_id})
        data = await cursor.fetchall()
        await cursor.close()
        await con.close()
        return data
