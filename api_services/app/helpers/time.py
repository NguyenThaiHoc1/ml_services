import datetime
import pytz


def now_utc():
    utc_now = datetime.datetime.utcnow()
    utc_now = utc_now.replace(tzinfo=pytz.utc)
    return utc_now


def str_dd_mm_yyyy(time: datetime = now_utc(), space="-"):
    return time.strftime("%d-%m-%Y")
