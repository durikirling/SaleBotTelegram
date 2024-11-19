import time

def get_duration(duration) -> str:
    ''' разбиение длительности в человеко-понятные единицы/разряды (из секунд с долями до крупнейшего возможного значения) '''
    if duration > 60:
        duration /= 60
        if duration > 60:
            duration /= 60 
            duration = str(int(duration)) + " ч. " + str(int((duration - int(duration))*60)) + " мин."
        else: 
            duration = str(int(duration)) + " мин. " + str(int((duration - int(duration))*60)) + " сек."
    else: duration = str(int(duration)) + " сек."
    return duration

def get_formated_date(data) -> str:
    return time.strftime("%H:%M:%S - %d.%m.%Y", data)