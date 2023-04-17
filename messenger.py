from bot import REFRESH_SEC
from datetime import datetime


weekdays = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}


def start_server():
    return f'⭐ Server start!\n{__get_date_time()}\n🔔 Notice: Refresh cycle is {REFRESH_SEC}s. 🔔'


def terminate_server():
    return f'⛔ Server terminated.\n{__get_date_time()}'


def __get_date_time():
    return f'\tDate: {datetime.now().strftime("%Y.%m.%d (%a)")}\n\tTime: {datetime.now().strftime("%X")}'


def get_new_info(crawl_result: dict):
    message = '---------------------------------------\n'
    for key, value in crawl_result.items():
        if key == 'number':
            continue
        message += f'{key}: {value}\n'
    message += '---------------------------------------'
    return message


def get_meeting_info(weekday_num, hour, min):
    weekday = weekdays[weekday_num]
    message = f'📢 현재 시각: {weekday}요일, {hour}시 {min}분\n\t미팅 1분 전입니다.'

    return message
