import sys
import pyautogui as pg
import time

while True:
    x,y=pg.position()
    time.sleep(50 / 1000)
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)
    print("x: {0}, y: {1}".format(x,y))