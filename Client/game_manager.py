from tkinter import *
import tkinter.messagebox as tkm

from threading import Thread

import time

class GameManager:
    def __init__(self, app):
        self.app = app

    def on_closing(self):
        self.app.conn.on_closing()
        self.app.root.destroy()
    
    def calc_next_Turn(self):
        val = self.app.turn
        for i in range(4):
            val = (val + 1) % 4 if ((val + 1) % 4) else 4
            if val not in self.app.deadPlyrs:
                return val
        return "<winner>"
    def calc_last_Turn(self):
        val = self.app.turn
        for i in range(4):
            val = (val - 1) if (val - 1) else 4
            if val not in self.app.deadPlyrs:
                return val
        return "<winner>"

    def newRound(self, loserPlyr):
        self.app.round += 1
        self.app.Tdice -= 1
        self.app.l["text"] = "ROUND:[{}]".format(self.app.round) + " - Final" if (self.app.Tdice == 2) else ""
        if self.app.Tdice == 2: self.app.finalR = True
        for x in self.app.betNumHolders + self.app.cnvBetTextExtra + [self.app.betLbl, self.app.betVal, self.app.betDie, self.app.preBetDie, self.app.preBetVal]:
            self.app.c.delete(x)
        self.app.cnvBetTextExtra = []
        self.app.currBet = [0, 0] if not self.app.finalR else 0
        if not self.app.User.playerNum in self.app.deadPlyrs:
            self.app.ROLLBTN = self.app.c.create_text(220, 230, text="ROLL DICE", font=("Times", 35), fill="red")
            self.app.c.bind("<Button-1>", self.app.roll); self.app.c.bind("<Enter>", self.app.on_ent); self.app.c.bind("<Leave>", self.app.on_esc)
        else:
            self.app.roll()

        if loserPlyr != 0:
            self.app.turn = loserPlyr
            self.app.turn = self.calc_next_Turn() if (loserPlyr in self.app.deadPlyrs) else loserPlyr
        self.app.roundStarter = self.app.turn

        for i in range(1,5):
            if i in self.app.deadPlyrs: self.app.c.itemconfig(self.app.playerById[i].board, fill="gray44")
            elif i == self.app.User.playerNum:
                self.app.c.itemconfig(self.app.playerById[i].board, fill="green")
            else: self.app.c.itemconfig(self.app.playerById[i].board, fill="dark green")
    
    def newTurn(self):
        if self.app.turn != self.app.roundStarter:
            self.app.roundStarter = 0
        if self.app.turn == self.app.User.playerNum:
            self.app.c.itemconfigure(self.app.betLbl, text=":BET:")
            if self.app.currBet != [0, 0] and self.app.currBet != 0 and self.app.User.playerNum != self.app.roundStarter:
                self.app.liarBtn["state"] = "active"
            self.app.allowCnvEdit = True
            self.app.cnvCntrl_State(1)
        else:
            self.app.c.itemconfigure(self.app.betLbl, text="[{}]'s Turn".format(str(self.app.turn)))
            self.app.allowCnvEdit = False
            self.app.cnvCntrl_State(0)
            self.app.liarBtn["state"] = "disabled"
            self.app.betBtn["state"] = "disabled"

        for i in range(1,5):
            if i == self.app.turn:
                self.app.c.itemconfig(self.app.playerById[i].board, fill=("light green" if i != self.app.User.playerNum else "green"))
            elif i in self.app.deadPlyrs: self.app.c.itemconfig(self.app.playerById[i].board, fill="gray44")
            else: self.app.c.itemconfig(self.app.playerById[i].board, fill="dark green")

    def gameover(self):
        self.app.conn.gameover()

        self.app.cnvCntrl_State(0)
        self.app.c.delete('all')
        winner = [item for item in [1, 2, 3, 4] if item not in self.app.deadPlyrs][0]
        self.app.c["bg"] = "green3" if winner == self.app.User.playerNum else "red3"
        self.app.c.create_text(255, 255, text="YOU WIN!" if winner == self.app.User.playerNum else "<{}> WINS!".format(self.app.playerById[winner].name), fill="white", font=("Persian", 28))

    def entergame(self):
        self.app.conbtn["state"],self.app.e["state"]  = "disabled","disabled"
        self.app.l["font"], self.app.l["text"] = "Times 18", "PLAYER {}\n>{}<".format(str(self.app.User.playerNum), self.app.User.name)
        self.app.conbtn.pack_forget(); self.app.e.pack_forget()

        self.app.connectingLabel = Label(self.app.root, text="Waiting for Server..", fg="red"); self.app.connectingLabel.pack()

        Thread(target=self.app.process.clientGameThread).start()

    def joinGame(self):
        tkm.showinfo("Success", "WELCOME TO GAME!")

        self.app.root.geometry("450x600")
        self.app.connectingLabel.pack_forget()
        self.app.l["text"] = "ROUND:[{}]".format(self.app.round)

        self.app.c = Canvas(self.app.root, width=450, height=450, bg="light blue"); self.app.c.pack()

        self.app.User.board = self.app.c.create_rectangle(90, 396, 360, 442, fill="green"); self.app.c.create_text(225, 386, text="|{}|: <{}>".format(self.app.User.playerNum,self.app.User.name), fill="red", font=("Persian", 15))
        self.app.playerById[self.app.plyrOrd[0]].board = self.app.c.create_rectangle(8, 127, 44, 323, fill="dark green"); self.app.c.create_text(55, 333, text="|{}|: <{}>".format(self.app.plyrOrd[0],self.app.playerById[self.app.plyrOrd[0]].name), fill="red")
        self.app.playerById[self.app.plyrOrd[1]].board = self.app.c.create_rectangle(127, 8, 323, 44, fill="dark green"); self.app.c.create_text(225, 55, text="|{}|: <{}>".format(self.app.plyrOrd[1],self.app.playerById[self.app.plyrOrd[1]].name), fill="red")
        self.app.playerById[self.app.plyrOrd[2]].board = self.app.c.create_rectangle(407, 127, 443, 323, fill="dark green"); self.app.c.create_text(396, 333, text="|{}|: <{}>".format(self.app.plyrOrd[2],self.app.playerById[self.app.plyrOrd[2]].name), fill="red")

        self.app.ROLLBTN = self.app.c.create_text(220, 230, text="ROLL DICE", font=("Times", 35), fill="red")
        self.app.c.bind("<Button-1>", self.app.roll); self.app.c.bind("<Enter>", self.app.on_ent); self.app.c.bind("<Leave>", self.app.on_esc)
        self.app.liarBtn = Button(self.app.root, width=20, text="LIAR!", font="Persian 25", command=self.app.callALie, state="disabled")
        self.app.betBtn = Button(self.app.root, width=20, text="Bet", font="Persian 25", command=self.app.placeBet, state="disabled")
        self.app.betBtn.pack(); self.app.liarBtn.pack()