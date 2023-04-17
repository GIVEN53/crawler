meetings = [[0, 16, 0]]


def is_meeting_time(weekday_num, hour, min):
    for meeting in meetings:
        if meeting[2] == 0:
            if (weekday_num == meeting[0]) and (hour == meeting[1] - 1) and (min == 59):
                return True
        else:
            if (weekday_num == meeting[0]) and (hour == meeting[1]) and (min == meeting[2] - 1):
                return True
    return False
