# likes the answer on this link: https://www.toppr.com/ask/question/which-substances-are-always-produced-in-an
# -acidbase-neutralization-reaction/

import pyperclip
import pyautogui
import time

toppr_answer_link = "https://www.toppr.com/ask/question/which-substances-are-always-produced-in-an-acidbase" \
                    "-neutralization-reaction/"
likes = int(input("How many likes would you like to give to the toppr answer - "))
pyautogui.hotkey("win", "2")
time.sleep(1)
pyperclip.copy(toppr_answer_link)

for i in range(likes):
    pyautogui.hotkey("ctrl", "shift", "n")
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(5)
    pyautogui.scroll(-1400)
    pyautogui.leftClick(1280, 915)
    pyautogui.hotkey("ctrl", "w")
