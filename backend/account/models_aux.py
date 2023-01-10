import re
from datetime import date, datetime, time, timedelta


class DateTimeCalculator:
    def __init__(self, date: date, time=time(0, 0)) -> None:
        self.__date = date
        self.__time = time
        self.datetime = datetime.combine(self.__date, self.__time)

    def is_day_passed(self) -> bool:
        return self.datetime <= datetime.now()

    @staticmethod
    def is_day_changed_relatively(reference_date: date, reference_time: time) -> bool:
        relative_date = __class__.get_relative_date(datetime.now(), reference_time)
        return reference_date != relative_date

    @staticmethod
    def is_day_on_due_relatively(reference_date: date, interval=1):
        pass

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

    @staticmethod
    def is_iso_format(time: str) -> bool:
        iso_format = "([0-1][0-9]|2[0-3]):([0-5][0-9])"
        # Ex.) '03:30'

        matched = re.match(iso_format, time)
        return matched != None
