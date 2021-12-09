import curses
import threading
import time
import random

random.seed(int(time.time()))

sun="sun"
star="star"
spade="spade"
heart="heart"
diamond="diamond"
club="club"
note="note"
nazi="nazi"
coin="coin"
face="face"

fig_list=[
    sun,
    star,
    spade,
    heart,
    diamond,
    club,
    note,
    nazi,
    coin,
    face,
]

figure={
    sun:"☼",
    star:"☆",
    spade:"♠",
    heart:"♥",
    diamond:"♦",
    club:"♣",
    note:"♪",
    nazi:"卐",
    coin:"◎",
    face:"☺",
}

refresh_period=50#milli sec

stdscr = curses.initscr()
curses.cbreak()
curses.noecho()

current_fig=[sun,sun,sun]
win_text=" "
money=10

def random_fig():
    global current_fig
    rlist=random.sample(range(0,len(fig_list)),3)
    current_fig=[fig_list[i] for i in rlist]

def show_fig():
    figs=[figure[f] for f in current_fig]
    for i,f in enumerate(figs):
        stdscr.addstr(10,10+i*3,f)

exit_sig=False

def pulled_func(scl):
    global money,win_text
    if money<=0:
        win_text="you are broke!"
        return
    win_text=" "
    money-=10
    for i,sc in enumerate(scl):
        bi=fig_list.index(current_fig[i])
        for j in range(sc):
            bi=(bi+1)%len(fig_list)
            current_fig[i]=fig_list[bi]
            time.sleep(refresh_period/1000)
    if current_fig[0]==current_fig[1] and current_fig[1]==current_fig[2]:
        win_text="you win!"
        money+=1000

def func_thread():
    global exit_sig, current_fig
    while 1:
        key=stdscr.getkey()
        if key=="q":
            exit_sig=True
            break
        elif key=="p":
            pulled_func(scl=random.sample(range(20,50),3))
        elif key=="w":
            di=random.randint(0,len(fig_list))
            rs=random.sample(range(3),3)
            cbi=[fig_list.index(current_fig[i]) for i in range(3)]
            cbi=[(di-x)%len(fig_list) for x in cbi]
            cbi=[a + b*len(fig_list) for a, b in zip(cbi, rs)]
            pulled_func(cbi)

ft = threading.Thread(target = func_thread)
ft.start()

def show_text():
    stdscr.addstr(12,10,win_text)
    stdscr.addstr(13,10,"${0}".format(money))

def render_thread():
    while 1:
        if exit_sig:break
        stdscr.clear()
        show_fig()
        show_text()
        stdscr.refresh()
        time.sleep(refresh_period/1000)
rt = threading.Thread(target = render_thread)
rt.start()

ft.join()
rt.join()

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()