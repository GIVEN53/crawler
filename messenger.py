weekdays = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}


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
    message = f'📢 현재 시각: {weekday}요일, {hour}시 {min}분\n미팅 1분 전입니다.'

    return message
