import sys
import threading
import time
import random
from PySide6.QtWidgets import *

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

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.pulling=False
        self.resize(800,800)
        # Create widgets
        self.edit = QLineEdit("Write my name here")
        self.button = QPushButton("Show Greetings")
        self.label= [QLabel(figure[sun]),QLabel(figure[sun]),QLabel(figure[sun])]
        self.ele=[sun,sun,sun]
        # Create layout and add widgets
        layout = QVBoxLayout()
        hl=QHBoxLayout()
        for l in self.label:
            hl.addWidget(l)
        layout.addLayout(hl)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)
        self.refresh_period=50

    # Greets the user
    def greetings(self):
        if not self.pulling:
            self.pulling=True
            threading.Thread(target = pulled_func,args=(random.sample(range(20,50),3),self)).start()

def pulled_func(scl,widget):
    #global money,win_text
    # if money<=0:
    #     win_text="you are broke!"
    #     return
    win_text=" "
    # money-=10
    for i,sc in enumerate(scl):
        bi=fig_list.index(widget.ele[i])
        for j in range(sc):
            bi=(bi+1)%len(fig_list)
            widget.ele[i]=fig_list[bi]
            widget.label[i].setText(figure[widget.ele[i]])
            time.sleep(widget.refresh_period/1000)
    if widget.ele[0]==widget.ele[1] and widget.ele[1]==widget.ele[2]:
        win_text="you win!"
        # money+=1000
    widget.pulling=False

if __name__ == '__main__':
    random.seed(int(time.time()))
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())