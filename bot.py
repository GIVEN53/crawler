import loader
import discord
import crawler
from datetime import datetime
import messenger
from selenium.common.exceptions import UnexpectedAlertPresentException
from discord.ext import tasks
import meeting

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
REFRESH_SEC = 180
now_number = '0'


@bot.event
async def on_ready():
    global notice_channel, alimi_channel, meeting_channel, driver

    # 봇 상태 정의
    game = discord.Game('크롤링')
    await bot.change_presence(activity=game, status=discord.Status.online)

    # 봇 구동 시 메시지 전송
    notice_channel = bot.get_channel(int(loader.get_env('notice_channel_id')))
    alimi_channel = bot.get_channel(int(loader.get_env('alimi_channel_id')))
    meeting_channel = bot.get_channel(int(loader.get_env('meeting_channel_id')))

    await notice_channel.send(messenger.start_server())

    driver = crawler.create_driver()
    crawler.login(driver)
    send_result.start()
    send_meeting_time.start()


# 크롤링 결과 알림 전송
@tasks.loop(seconds=REFRESH_SEC)
async def send_result():
    global now_number

    try:
        result = crawler.crawl_target(driver)
        if result['number'] != now_number:
            now_number = result['number']
            message = messenger.get_new_info(result)
            await alimi_channel.send(message)
    except UnexpectedAlertPresentException:
        crawler.login(driver)
        await send_result()


@send_result.after_loop
async def close():
    await notice_channel.send(messenger.terminate_server())
    await bot.close()


@tasks.loop(minutes=1)
async def send_meeting_time():
    now = datetime.now()

    if meeting.is_meeting_time(now.weekday(), now.hour, now.minute):
        message = messenger.get_meeting_info(now.weekday(), now.hour, now.minute)
        await meeting_channel.send(message)


if __name__ == '__main__':
    bot.run(loader.get_env('discord_token'))
