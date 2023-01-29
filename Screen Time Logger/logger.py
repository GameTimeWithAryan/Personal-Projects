"""
Logger logs the time difference between the starting of the program and ending
The log is updated every second

This program is supposed to be run at computer startup time and end when computer shuts down
to log the screen time of user
"""

from time import sleep
from datetime import datetime
from util import get_hour_min_sec


def get_time_diff(start_time):
    """ Return Log styled time showing difference between current time and start_time"""
    time_difference = datetime.now() - start_time
    hours, minutes, seconds = get_hour_min_sec(time_difference.seconds)

    # Log time format: HH:MM:SS
    time_in_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return time_in_str


def logger():
    """The Logger"""
    start_date = datetime.now()
    log_date = start_date.strftime("%d-%m-%Y %H:%M:%S")

    # Reading the file
    with open("log.txt", "r") as file:
        lines = file.readlines()

    # Setting Current Session
    lines.append("CURRENT SESSION")

    print("Logging has Started")
    # Updating file with new Screen Time every second
    while True:
        sleep(1)
        """ get_time_diff(start_date) will give difference between start time of program i.e. start time of computer 
        and current time i.e. time for which the computer is in use """
        log_message = f"[{log_date}] {get_time_diff(start_date)}\n"
        lines[-1] = log_message  # Updating Current Session Log

        with open("log.txt", "w") as file:
            file.writelines(lines)


if __name__ == '__main__':
    logger()
