import loader
import discord
import crawler
import messenger
from discord.ext import tasks
import requests

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
REFRESH_SEC = 120
now_number = "0"


@bot.event
async def on_ready():
    global notice_channel, alimi_channel

    # 봇 상태 정의
    game = discord.Game("크롤링")
    await bot.change_presence(activity=game, status=discord.Status.online)

    # 봇 구동 시 메시지 전송
    notice_channel = bot.get_channel(int(loader.get_env("notice_channel_id")))
    alimi_channel = bot.get_channel(int(loader.get_env("alimi_channel_id")))

    await notice_channel.send(messenger.start_server())

    session = requests.Session()
    crawler.login(session)
    send_result.start(session)


# 크롤링 결과 알림 전송
@tasks.loop(seconds=REFRESH_SEC)
async def send_result(session):
    global now_number

    try:
        result = crawler.crawl_target(session)
        if result["number"] != now_number:
            now_number = result["number"]
            message = messenger.get_new_info(result)
            await alimi_channel.send(message)
    except requests.exceptions.RequestException or IndexError:
        crawler.login(session)
        await send_result(session)


@send_result.after_loop
async def close():
    await notice_channel.send(messenger.terminate_server())
    await bot.close()


if __name__ == "__main__":
    bot.run(loader.get_env("discord_token"))
