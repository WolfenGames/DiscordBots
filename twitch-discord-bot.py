import discord
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from datetime import date, datetime

from twitch_client import TwitchClient

load_dotenv()

TWITCH_TOKEN = os.getenv('TWITCH_AUTH_TOKEN')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
USERS = os.getenv('USERS_TO_MONITOR').split(',')

USER_LOGGED = {}

class DiscordBot:
    def __init__(self, twitch_client, USER_LOGGED=USER_LOGGED):
        load_dotenv()
        self.twitch_client = twitch_client
        self.client = discord.Client()
        self.TOKEN = os.getenv("TWITCH_NOTIFIER_KEY")
        self.USER_LOGGED = USER_LOGGED

        try:
            self.client.loop.create_task(self.task())
            self.client.loop.run_until_complete(self.client.start(self.TOKEN))
        except SystemExit:
            pass
            # handle_exit()
        except KeyboardInterrupt:
            # handle_exit()
            self.client.loop.close()
            print("Program ended.")

    async def task(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.check_user_online, "cron", minute="*")
        scheduler.start()

    async def check_user_online(self):
        await self.client.wait_until_ready()
        guild = self.client.guilds[0]
        channel = discord.utils.get(
            self.client.get_all_channels(),
            name=os.getenv("CHANNEL_TO_POST")
        )
        role = discord.utils.get(
            guild.roles,
            name=os.getenv("ROLE_TO_MENTION")
        )

        for user in USERS:
            fetched = self.twitch_client.get_is_streaming(user)
            if any(fetched):
                user_info = fetched[0]
                msg = f"Hey {role.mention}\n\
{user_info['user_name']} is streaming {user_info['game_name']}\n\
Check them out here: https://twitch.tv/{user_info['user_name']}\n\
\n\
{user_info['title']}"

                started_at = user_info['started_at']
                if self.USER_LOGGED[f"{user_info['user_login']}"] != started_at:
                    self.USER_LOGGED[f"{user_info['user_login']}"] = started_at
                    await channel.send(msg)

_twitch_client = TwitchClient(TWITCH_TOKEN, TWITCH_CLIENT_ID)
_twitch_client.set_headers()

users_info = _twitch_client.get_users(USERS)

for user in users_info:
    now = datetime.utcnow()
    datething = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    USER_LOGGED[user['login']] = datething

_discord = DiscordBot(_twitch_client, USER_LOGGED)
