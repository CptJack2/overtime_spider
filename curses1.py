import curses
import time

stdscr = curses.initscr()
stdscr = curses.initscr()

# stdscr.addstr(5,10,'abv',curses.A_REVERSE)
#
# while 1:
#     c = stdscr.getch()
#
# for i in range(100,110):
#     time.sleep(1)
#     stdscr.addstr(10,10,chr(i)*10)
#     stdscr.refresh()

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()