from datetime import datetime


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%m.%d.%Y")
    except ValueError:
        return None