import datetime


def get_att_event_time_tokens(att_event_time):
    "Output: att_year, att_month, att_day, att_hour, att_min, att_sec, att_ms, att_timestamp, att_date, att_datetime"
    att_event_time = att_event_time.replace('+00:00', '')
    dt = datetime.datetime.strptime(att_event_time, '%Y-%m-%d %H:%M:%S.%f')
    att_year = dt.year
    att_month = dt.month
    att_day = dt.day
    att_hour = dt.hour
    att_min = dt.minute
    att_sec = dt.second
    att_ms = dt.microsecond
    att_timestamp = int(dt.timestamp() * 1000)
    att_date = str(dt.date())
    att_datetime = int(dt.timestamp())

    return att_year, att_month, att_day, att_hour, att_min, att_sec, att_ms, att_timestamp, att_date, att_datetime


# tests
dates = []
dates.append('2018-12-10 10:48:12.943036+00:00')
# dates.append('2018-11-27 11:26:21.109571+00:00')

for date in dates:
    print('{},{}'.format(date, get_att_event_time_tokens(date)))
