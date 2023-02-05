"""
Logger logs the time for which it was running
The log is updated every second
"""

from time import sleep
from datetime import datetime
from util import get_hour_min_sec


def format_time(time: int) -> str:
    """
    Takes time in seconds
    Return formatted time
    Time format: HH:MM:SS
    """
    hours, minutes, seconds = get_hour_min_sec(time)
    time_in_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return time_in_str


def logger():
    """The Logger"""
    time_spent = 0
    log_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Reading the file
    with open("log.txt", "r") as file:
        lines = file.readlines()

    # Setting Current Session
    lines.append("CURRENT SESSION")

    print("Logging has Started")
    # Updating file with new time_spent every loop
    while True:
        sleep(1)
        time_spent += 1
        print(f"Time Spent: {time_spent}")

        log_message = f"[{log_date}] {format_time(time_spent)}\n"
        lines[-1] = log_message  # Updating Current Session Log
        with open("log.txt", "w") as file:
            file.writelines(lines)


if __name__ == '__main__':
    logger()
