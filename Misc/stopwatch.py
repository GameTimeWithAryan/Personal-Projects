try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import time

# CONSTANTS
TIME_FORMAT = "{:.2f}"
DELAY_BETWEEN_UPDATE = 30


def switch_play_button():
    global play_index
    play_index = int(not bool(play_index))
    play_button.config(text=play_buttons[play_index][0])
    play_button.config(command=play_buttons[play_index][1])


def update_stopwatch(start_time, time_to_count):
    """ Update stopwatch until time runs out or stop button is pressed """
    current_time = time.time()
    time_difference = current_time - start_time

    # Play index 1 indicates stop button is on screen which means timer is running
    if time_difference < time_to_count and play_index == 1:
        # Updating Stopwatch Label
        backward_time = round(time_to_count - time_difference, 2)
        update_stopwatch_label(backward_time)

        # Calling update function after delay
        caller = lambda: update_stopwatch(start_time, time_to_count)
        root.after(DELAY_BETWEEN_UPDATE, caller)

    elif time_difference > time_to_count:
        stop()


def update_stopwatch_label(stopwatch_time):
    stopwatch_label.config(text=TIME_FORMAT.format(stopwatch_time))


def get_timer_input():
    """ Gets text from timer input box """
    try:
        c_time = int(timer_entry.get())
    except ValueError:
        timer_entry.delete(0, END)
        timer_entry.insert(0, "Please enter a valid number")
        c_time = 0
    return c_time


def start(time_to_count, start_time):
    caller = lambda: update_stopwatch(start_time, time_to_count)
    root.after(DELAY_BETWEEN_UPDATE, caller)
    switch_play_button()


def stop():
    switch_play_button()
    update_stopwatch_label(0)


# For handling buttons
# (Button Text, Function to call on button press)
play_buttons = [("Start Timer", lambda: start(get_timer_input(), time.time())), ("Stop Timer", stop)]
play_index = 0  # 0 for Start, 1 for Stop | to manage the state of button

root = Tk()
root.geometry("290x200")
root.title("Stopwatch")

# Input widgets
timer_entry_label = Label(text="Enter time in seconds: ")
timer_entry = Entry(root, justify=CENTER, width=30)
timer_entry.insert(0, "2")

# Button and stopwatch timer widgets
play_button = Button(root, text=play_buttons[play_index][0],
                     command=play_buttons[play_index][1])
stopwatch_label = Label(root, text="0.00", font=("Arial", 40))

# Displaying stuff
timer_entry_label.pack(pady=(15, 0))
timer_entry.pack()
play_button.pack(pady=10)
stopwatch_label.pack()

root.mainloop()
