from datetime import datetime


def time_to_datetime(time_obj):
    return datetime.combine(datetime.today(), time_obj)
