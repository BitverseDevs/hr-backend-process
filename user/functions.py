import datetime

def number_of_days_before(dates):
    today = datetime.date.today()

    if today.month > dates.month:
        dates = dates.replace(year=today.year + 1)
    else:
        dates = dates.replace(year=today.year)

    days = dates - today

    return days + datetime.time(days=1) if today.year/4 == 0 else days.days