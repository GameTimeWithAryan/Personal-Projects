from util import *
from datetime import date


def get_total_days(log_lines: list):
    """ Returns the difference between first log's date and last log's date
     i.e. gives the difference between range of dates for which logging occurred """
    if len(log_lines) == 0:
        msg = "No log line in log_lines to parse date from\nPlease run logger to first get some data in log.txt"
        raise Exception(msg)
    if len(log_lines) == 1:
        return 1

    start = get_date(log_lines[0])
    end = get_date(log_lines[-1])

    start_date = date(start[0], start[1], start[2])
    end_date = date(end[0], end[1], end[2])
    return (end_date - start_date).days + 1


def get_total_time(log_lines: list):
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
