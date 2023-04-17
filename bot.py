import loader
import discord
import crawler
from time import strftime
import mapper
from selenium.common.exceptions import UnexpectedAlertPresentException
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
REFRESH_SEC = 180
now_number = '0'


@bot.event
async def on_ready():
    global notice_channel, alimi_channel, driver

    # 봇 상태 정의
    game = discord.Game('크롤링')
    await bot.change_presence(activity=game, status=discord.Status.online)

    # 봇 구동 시 메시지 전송
    notice_channel = bot.get_channel(int(loader.get_env('notice_channel_id')))
    alimi_channel = bot.get_channel(int(loader.get_env('alimi_channel_id')))
    await notice_channel.send(f'⭐ Server start!\n{get_date_time()}\n🔔 Notice: Refresh cycle is {REFRESH_SEC}s. 🔔')

    driver = crawler.create_driver()
    crawler.login(driver)
    send_result.start()


# 크롤링 결과 알림 전송
@tasks.loop(seconds=REFRESH_SEC)
async def send_result():
    global now_number

    try:
        result = crawler.crawl_target(driver)
        if result['number'] != now_number:
            now_number = result['number']
            message = mapper.mapping_new_info(result)
            await alimi_channel.send(message)
    except UnexpectedAlertPresentException:
        crawler.login(driver)
        await send_result()


@send_result.after_loop
async def close():
    await notice_channel.send(f'⛔ Server terminated.\n{get_date_time()}')
    await bot.close()


def get_date_time():
    return f'\tDate: {strftime("%Y.%m.%d (%a)")}\n\tTime: {strftime("%X")}'


if __name__ == '__main__':
    bot.run(loader.get_env('discord_token'))
