from tkinter import *
import tkinter.messagebox as tkm
import time, atexit

import random

from die import Die
from conn import Conn
from game_manager import GameManager
from process import Process


class App:
    def __init__(self, root, savedName):
        self.savedName = savedName
        self.root = root
        self.root.title("Liars Dice")
        self.root.geometry("400x250")
        self.root["bg"] = "light gray"

        self.conn = Conn(self)
        self.game_manager = GameManager(self)
        self.process = Process(self)

        self.setup()
    
    def setup(self):
        self.playerById = {}
        self.plyrOrd = [1, 2, 3, 4]
        self.deadPlyrs = []
        self.Tdice= 20
        self.round = 1
        self.roundStarter = 1
        self.turn = 0
        self.currBet = [0, 0]

        self.allowCnvEdit, self.cc_State = False, False
        self.finalR = False

        self.l = Label(self.root, text="Liars Dice", font="Times 35", bg="light gray"); self.l.pack(pady=20)
        self.sv = StringVar()
        self.sv.set(self.savedName)
        self.e = Entry(self.root, textvariable=self.sv)
        self.e.pack(side=LEFT)
        self.conbtn = Button(self.root, text="Connect", command=(lambda : self.conn.connect(self.sv.get())))
        self.conbtn.pack(side=LEFT)
        self.betNumHolders = []
        self.canvCntrl = []
        self.cnvBetTextExtra = []

        self.root.protocol("WM_DELETE_WINDOW", self.game_manager.on_closing)
        atexit.register(self.game_manager.on_closing)
        self.root.mainloop()

    def roll(self, e=None):
        self.rollWait = self.c.create_text(220, 200, text="Waiting for players to roll....")
        if self.User.playerNum in self.deadPlyrs: return
        self.c.delete(self.ROLLBTN)
        self.User.rolled = True
        self.c.unbind("<Button 1>")
        self.c.unbind("<Enter>")
        self.c.unbind("<Leave>")
        self.conn.send(str.encode("Rolled"))


    def cnvCntrl_1U(self, e): self.cnvCntrl1("1U")
    def cnvCntrl_1D(self, e): self.cnvCntrl1("1D")
    def cnvCntrl_2U(self, e): self.cnvCntrl1("2U")
    def cnvCntrl_2D(self, e): self.cnvCntrl1("2D")
    def cnvCntrl_State(self, enabled):
        if enabled:
            if not self.cc_State:
                self.cc_State = True
                n23 = random.choice(list(range(0, 1000)))
                print(self.canvCntrl)
                for i in self.canvCntrl:
                    self.c.itemconfig(i, state="normal")
                    TG = self.c.itemcget(i, "tags")

                    print(TG + "        <{}".format(str(n23)))
                    if TG == "1U": self.c.tag_bind(i, "<Button-1>", self.cnvCntrl_1U)
                    if TG == "1D": self.c.tag_bind(i, "<Button-1>", self.cnvCntrl_1D)
                    if TG == "2U": self.c.tag_bind(i, "<Button-1>", self.cnvCntrl_2U)
                    if TG == "2D": self.c.tag_bind(i, "<Button-1>", self.cnvCntrl_2D)
        else:
            if self.cc_State:
                self.cc_State = False
                for i in self.canvCntrl:
                    print("<<<<<< ")
                    self.c.tag_unbind(i, "<Button-1>")
                    self.c.itemconfig(i, state="hidden")
    def cnvCntrl1(self, Mytag):
        if self.allowCnvEdit:
            if self.c.itemcget(self.betVal, "text") == "":
                if not self.finalR:
                    if self.currBet == [0, 0]:
                        self.c.itemconfig(self.betVal, text="1")
                        self.c.itemconfig(self.betDie, text="2")
                    else:
                        self.c.itemconfig(self.betVal, text=str(self.currBet[0]))
                        self.c.itemconfig(self.betDie, text=str(self.currBet[1]))
                else:
                    if self.currBet == 0:
                        self.c.itemconfig(self.betVal, text="1")
                    else:
                        self.c.itemconfig(self.betVal, text=str(self.currBet))
            else:
                if Mytag == "1U":
                    if not self.finalR:
                        if int(self.c.itemcget(self.betVal, "text")) != self.Tdice:
                            self.c.itemconfig(self.betVal, text=str(int(self.c.itemcget(self.betVal, "text"))+1))
                    else:
                        if int(self.c.itemcget(self.betVal, "text")) != 12:
                            self.c.itemconfig(self.betVal, text=str(int(self.c.itemcget(self.betVal, "text")) + 1))
                if Mytag == "1D":
                    if not self.finalR:
                        if int(self.c.itemcget(self.betVal, "text")) not in [self.currBet[0], 1]:
                            self.c.itemconfig(self.betVal, text=str(int(self.c.itemcget(self.betVal, "text"))-1))
                            if int(self.c.itemcget(self.betVal, "text")) == self.currBet[0] and int(self.c.itemcget(self.betDie, "text")) < self.currBet[1]:
                                self.c.itemconfig(self.betDie, text=str(self.currBet[1]))
                    else:
                        if int(self.c.itemcget(self.betVal, "text")) not in [self.currBet, 1]:
                            self.c.itemconfig(self.betVal, text=str(int(self.c.itemcget(self.betVal, "text"))-1))

                if Mytag == "2U":
                    if int(self.c.itemcget(self.betDie, "text")) != 6: self.c.itemconfig(self.betDie, text=str(int(self.c.itemcget(self.betDie, "text"))+1))
                if Mytag == "2D":
                    if int(self.c.itemcget(self.betDie, "text")) != 2:
                        if int(self.c.itemcget(self.betVal, "text")) == self.currBet[0]:
                            if int(self.c.itemcget(self.betDie, "text")) != self.currBet[1]:
                                self.c.itemconfig(self.betDie, text=str(int(self.c.itemcget(self.betDie, "text"))-1))
                        else: self.c.itemconfig(self.betDie, text=str(int(self.c.itemcget(self.betDie, "text"))-1))
            if not self.finalR:
                if int(self.c.itemcget(self.betVal, "text")) == self.currBet[0] and int(self.c.itemcget(self.betDie, "text")) == self.currBet[1]:
                    self.betBtn["state"] = "disabled"
                else:
                    self.betBtn["state"] = "active"
            else:
                if int(self.c.itemcget(self.betVal, "text")) == self.currBet:
                    self.betBtn["state"] = "disabled"
                else:
                    self.betBtn["state"] = "active"


    def placeBet(self):
        if not self.finalR: self.conn.send(str.encode(">#NewBet:-{}-{}".format(str(self.c.itemcget(self.betVal, "text")), str(self.c.itemcget(self.betDie, "text")))))
        else: self.conn.send(str.encode(">:<fnl>:#NewBet:-{}-".format(str(self.c.itemcget(self.betVal, "text")))))
    def callALie(self): self.conn.send(str.encode(">#Liar"))

    def on_ent(self, e): self.c.itemconfig(self.ROLLBTN, fill="blue")
    def on_esc(self, e): self.c.itemconfig(self.ROLLBTN, fill="red")
    def draw_dice(self, side, DiceQ=0):
        hand = []
        if side == 1:
            x = 105
            for i in range(self.User.dice):
                die1 = Die(self.c, x, 401, 36, self.User.hand[i])
                hand += [die1]
                x += 51
        if side == 2:
            x = 138
            for i in range(DiceQ):
                die1 = Die(self.c, 13, x, 26)
                hand += [die1]
                x += 37
        if side == 3:
            x = 138
            for i in range(DiceQ):
                die1 = Die(self.c, x, 13, 26)
                hand += [die1]
                x += 37
        if side == 4:
            x = 138
            for i in range(DiceQ):
                die1 = Die(self.c, 412, x, 26)
                hand += [die1]
                x += 37
        return hand



    

    def drawGameFeatures(self):
        #Turn Label<
        self.betLbl = self.c.create_text(225, 110, text=":BET:", fill="Orange2", font=("application", 36))
        if not self.finalR:
            #Bet Selection display
            self.betNumHolders = []
            self.betNumHolders += [self.c.create_rectangle(150, 155, 210, 215, fill="white")]
            self.betVal = self.c.create_text(180,185,text="",fill="purple", font=("Times", 33))
            self.betNumHolders += [self.c.create_rectangle(240, 155, 300, 215, fill="white")]
            self.betDie = self.c.create_text(270, 185, text="", fill="blue", font=("Times", 33))
            # {}x{}s format display
            self.cnvBetTextExtra += [self.c.create_text(225, 185, text="x", fill="black", font=("Times", 25))]
            self.cnvBetTextExtra += [self.c.create_text(314, 195, text="'s", fill="black", font=("Times", 30))]

            #Canvas Controls
            for x in self.canvCntrl:
                self.c.delete(x)
            self.canvCntrl = []
            self.canvCntrl += [self.c.create_polygon(165, 150, 195, 150, 180, 130, fill="IndianRed", outline="black", tags="1U")]
            self.canvCntrl += [self.c.create_polygon(165, 220, 195, 220, 180, 240, fill="IndianRed", outline="black", tags="1D")]
            self.canvCntrl += [self.c.create_polygon(255, 150, 285, 150, 270, 130, fill="IndianRed", outline="black", tags="2U")]
            self.canvCntrl += [self.c.create_polygon(255, 220, 285, 220, 270, 240, fill="IndianRed", outline="black", tags="2D")]

            #Extra GUI for "Previous Bet" display
            temp1 = self.c.create_rectangle(165, 260, 285, 323, fill="orange3")
            temp2 = self.c.create_text(225, 314, text="^ PREVIOUS ^", fill="white", font=("Times", 16))
            #"Previous Bet" Display
            self.betNumHolders += [self.c.create_rectangle(170, 265, 210, 305, fill="gray")]
            self.preBetVal = self.c.create_text(190, 285, text="", fill="purple", font=("Times", 29))
            self.betNumHolders += [self.c.create_rectangle(230, 265, 270, 305, fill="gray")]
            self.preBetDie = self.c.create_text(250, 285, text="", fill="blue", font=("Times", 29))
            self.betNumHolders += [temp1, temp2]
            # {}x{}s format display
            self.cnvBetTextExtra += [self.c.create_text(220, 285, text="x", fill="black", font=("Times", 24))]
            self.cnvBetTextExtra += [self.c.create_text(278, 290, text="'s", fill="black", font=("Times", 24))]
        else:
            # Bet Selection display
            self.betNumHolders = []
            self.betNumHolders += [self.c.create_rectangle(195, 155, 255, 215, fill="white")]
            self.betVal = self.c.create_text(225, 185, text="", fill="blue", font=("Times", 33))

            # Canvas Controls
            for x in self.canvCntrl:
                self.c.delete(x)
            self.canvCntrl = []
            self.canvCntrl += [self.c.create_polygon(210, 150, 240, 150, 225, 130, fill="IndianRed", outline="black", tags="1U")]
            self.canvCntrl += [self.c.create_polygon(210, 220, 240, 220, 225, 240, fill="IndianRed", outline="black", tags="1D")]

            # Extra GUI for "Previous Bet" display
            temp1 = self.c.create_rectangle(165, 260, 285, 323, fill="orange3")
            temp2 = self.c.create_text(225, 314, text="^ PREVIOUS ^", fill="white", font=("Times", 16))
            # "Previous Bet" Display
            self.betNumHolders += [self.c.create_rectangle(205, 265, 245, 305, fill="gray")]
            self.preBetVal = self.c.create_text(225, 285, text="", fill="blue", font=("Times", 29))
            self.betNumHolders += [temp1, temp2]
