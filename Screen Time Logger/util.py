# Log Line example: [31-1-2030 18:30:50] 00:00:30

def get_hour_min_sec(seconds: int):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


def get_time(log_line: str):
    """ Returns time from a line of log.txt, in a list of ints
    :returns [hour, min, sec] """
    return list(map(int, log_line.split(" ")[-1].split(":")))


def get_date(log_line: str):
    """ Returns date from a line of log.txt, in a list of strings
    :returns ['year', 'month', 'day'] """
    return log_line.split(" ")[0][1:].split("-")[::-1]


def time_to_str(seconds: int) -> str:
    """ Change seconds into human-readable format """
    time_in_str = ""
    hours, minutes, seconds = get_hour_min_sec(seconds)

    if hours != 0:
        time_in_str += f"{hours} Hrs, "
    if minutes != 0:
        time_in_str += f"{minutes} Min, "
    if seconds != 0:
        time_in_str += f"{seconds} Sec"
    return time_in_str
