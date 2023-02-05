from util import *


def get_total_days(log_lines: list) -> int:
    """ Returns total numbers of days for which data was logged """
    if len(log_lines) == 0:
        msg = "No log line in log_lines to parse date from\nRun logger to first get some data in log.txt"
        raise Exception(msg)

    dates = set()  # set() to add unique dates, i.e. get actual no. of days for which log exists
    for line in log_lines:
        date = " ".join(get_date(line))  # Converting into string for adding into set
        dates.add(date)
    return len(dates)


def get_total_time(log_lines: list) -> int:
    """ Returns total time stored in log, in seconds """
    total = 0
    for line in log_lines:
        hours, minutes, seconds = get_time(line)
        total += hours * 3600 + minutes * 60 + seconds
    return total


def parser():
    with open("log.txt", "r") as file:
        lines = file.readlines()

    total_time = get_total_time(lines)
    total_days = get_total_days(lines)
    average = total_time // total_days

    print(f"{time_to_str(average)} on average per day")
    print(f"Calculated on data of: {total_days} days")


if __name__ == "__main__":
    parser()
