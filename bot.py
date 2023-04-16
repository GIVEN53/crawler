import loader
import discord
import crawler
from time import strftime
import mapper
import asyncio
from selenium.common.exceptions import UnexpectedAlertPresentException

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
REFRESH_SEC = 180

@bot.event
async def on_ready():
    # 봇 상태 정의
    game = discord.Game('크롤링')
    await bot.change_presence(activity=game, status=discord.Status.online)

    # 봇 구동 시 메시지 전송
    notice_channel = bot.get_channel(int(loader.get_env('notice_channel_id')))
    await notice_channel.send(f'⭐ Server start!\n{get_date_time()}\n🔔 Notice: Refresh cycle is {REFRESH_SEC}s. 🔔')

    # 크롤링 전 로그인
    driver = crawler.create_driver()
    crawler.login(driver)

    # 크롤링 결과 알림 전송
    alimi_channel = bot.get_channel(int(loader.get_env('alimi_channel_id')))
    await send_result(notice_channel, alimi_channel, driver, '0')


async def send_result(notice_channel, alimi_channel, driver, now_number):
    try:
        while True:
            result = crawler.crawl_target(driver)
            if result['number'] != now_number:
                now_number = result['number']
                message = mapper.mapping_new_info(result)
                await alimi_channel.send(message)
            await asyncio.sleep(REFRESH_SEC)
    except UnexpectedAlertPresentException :
        crawler.login(driver)
        await send_result(alimi_channel, driver, now_number)
    except asyncio.CancelledError or KeyboardInterrupt:
        await notice_channel.send(f'⛔ Server terminated.\n{get_date_time()}')


@bot.event
async def on_error(event, *args, **kwargs):
    await bot.close()


def get_date_time():
    return f'\tDate: {strftime("%Y.%m.%d (%a)")}\n\tTime: {strftime("%X")}'


if __name__ == '__main__':
    bot.run(loader.get_env('discord_token'))
