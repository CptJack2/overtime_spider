import pyautogui as pg
import  time
while True:
    x,y=pg.position()
    time.sleep(50 / 1000)
    print("x: {0}, y: {1}".format(x,y),end="\r")