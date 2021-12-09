import sys
import threading
import time
import random
from PySide6.QtWidgets import *
from PySide6.QtGui import *

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
        self.resize(500,500)
        # Create widgets
        self.edit = QLineEdit()
        self.button = QPushButton("PULL FOR LUCK!")
        self.label= [QLabel(figure[sun]),QLabel(figure[sun]),QLabel(figure[sun])]
        for l in self.label:
            l.setFont(QFont("Times", 50))
        self.ele=[sun,sun,sun]
        self.winmsg=QLabel("Hello!")
        self.dollarSign=QLabel("$")

        # Create layout and add widgets
        layout = QVBoxLayout()
        hl=QHBoxLayout()
        for l in self.label:
            hl.addWidget(l)
        layout.addLayout(hl)

        hl2=QHBoxLayout()
        hl2.addWidget(self.dollarSign)
        hl2.addWidget(self.edit)

        layout.addLayout(hl2)
        layout.addWidget(self.winmsg)
        layout.addWidget(self.button)

        # Set dialog layout
        self.setLayout(layout)

        # Add button signal to greetings slot
        self.button.clicked.connect(self.pulled)
        self.dollarSign.mousePressEvent = self.wealthMagic
        self.edit.textChanged.connect(self.textChanged)

        self.refresh_period=50
        self.setMoney(1000)

    def wealthMagic(self,ev):
        if not self.pulling:
            self.setMsg("You just got the wealth magic!")
            self.pulling=True
            di=random.randint(0,len(fig_list))
            rs=random.sample(range(3),3)
            cbi=[fig_list.index(self.ele[i]) for i in range(3)]
            cbi=[(di-x)%len(fig_list) for x in cbi]
            cbi=[a + b*len(fig_list) for a, b in zip(cbi, rs)]
            threading.Thread(target = self.pulled_func,args=(cbi,"You just got the wealth magic!")).start()

    def setMsg(self,msg):
        self.winmsg.setText(msg)

    def setMoney(self,n):
        self.money=n
        self.edit.setText(str(n))

    def textChanged(self):
        try:
            n=int(self.edit.text())
        except:
            return
        else:
            self.money=n

    def pulled(self):
        if not self.pulling:
            threading.Thread(target = self.pulled_func,args=(random.sample(range(20,50),3),"Hello!")).start()

    def scroll_to_next(self,index):
        bi=fig_list.index(self.ele[index])
        bi=(bi+1)%len(fig_list)
        self.ele[index]=fig_list[bi]
        self.label[index].setText(figure[self.ele[index]])

    def pulled_func(self,scl,msg):
        if self.money<=0:
            self.setMsg("you are broke!")
            return
        self.pulling=True
        self.setMsg(msg)
        self.setMoney(self.money-10)
        sum=0
        l=len(self.ele)
        for i,sc in enumerate(scl):
            for j in range(sc+l-sum%l):
                self.scroll_to_next(i)
                for k in range(i+1, len(self.ele)):
                    self.scroll_to_next(k)
                sum+=1
                time.sleep(self.refresh_period/1000)
        if self.ele[0]==self.ele[1] and self.ele[1]==self.ele[2]:
            self.setMsg("you win!")
            self.setMoney(self.money+1000)
        else:
            self.setMsg("Good luck next time!")
        self.pulling=False

if __name__ == '__main__':
    random.seed(int(time.time()))
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())