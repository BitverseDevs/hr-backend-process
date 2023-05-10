import datetime

def number_of_days_before(dates):
    today = datetime.date.today()

    if today.month > date.month or today.day > date.day:
        date = date.replace(year=today.year + 1)
    else:
        date = date.replace(year=today.year)

    days = date - today

    return days + datetime.time(days=1) if today.year/4 == 0 else days.days