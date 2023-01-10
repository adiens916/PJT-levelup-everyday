import re
from datetime import date, datetime, time, timedelta


class RelativeDateTime:
    def __init__(self, reference_date: date, reference_time=time(0, 0)) -> None:
        self.__reference_date = reference_date
        self.__reference_time = reference_time

    def is_day_changed_relatively(self) -> bool:
        relative_date = self.get_relative_date(datetime.now(), self.__reference_time)
        return self.__reference_date != relative_date

    def is_day_on_due_relatively(self, interval=1) -> bool:
        relative_date = self.get_relative_date(datetime.now(), self.__reference_time)
        return self.__reference_date + timedelta(days=interval) == relative_date

    @staticmethod
    def get_relative_date(absolute_datetime: datetime, reference_time: time) -> date:
        hours = reference_time.hour
        minutes = reference_time.minute
        offset = timedelta(hours=hours, minutes=minutes)

        relative_datetime = absolute_datetime - offset
        if reference_time.hour < 12:
            return relative_datetime.date()
        else:
            return relative_datetime.date() + timedelta(days=1)


def is_iso_format_time(time: str) -> bool:
    iso_format = "([0-1][0-9]|2[0-3]):([0-5][0-9])"
    # Ex.) '03:30'

    matched = re.match(iso_format, time)
    return matched != None
