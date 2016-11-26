from src.lib.core.reader import Reader
from datetime import datetime, timedelta

reader = Reader('../fixtures/sample-nasa-access-log.log')

date = "frfrfr"


def parse_datetime(string_datetime):
    datetime_result = datetime.strptime(string_datetime[0:20], '%d/%b/%Y:%X')

    # The string date has the following format 01/Jul/1995:00:00:09 -400 so so the basic date is 20 characters long
    # and the timezone is the 22th character, so at index 21
    if string_datetime[21] == '+':

        # The we just take the value of the timezone, that we divide by one hundred
        datetime_result += timedelta(hours=int(string_datetime[22:26]) / 100)

    elif string_datetime[21] == '-':

        datetime_result -= timedelta(hours=int(string_datetime[22:26]) / 100)

    return datetime_result

print(parse_datetime(date))
