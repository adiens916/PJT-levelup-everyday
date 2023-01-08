import re


class DateTimeCalculator:
    @staticmethod
    def is_iso_format(time: str):
        iso_format = "([0-1][0-9]|2[0-3]):([0-5][0-9])"
        # Ex.) '03:30'

        matched = re.match(iso_format, time)
        return matched
