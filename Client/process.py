from tkinter import *
import tkinter.messagebox as tkm

from user import User

import time

class Process:
    def __init__(self, app):
        self.app = app
    def clientGameThread(self):
        recvStart = self.app.conn.recieve()
        if recvStart.startswith("GAMESTART:-"):
            playerNl = recvStart.replace("GAMESTART:-", "").split("_|-|")
            myI = -1
            for plyrN in range(1, 5):
                nme = playerNl[plyrN-1]
                if nme == self.app.User.name:
                    myI = plyrN
                    continue
                newU = User(nme, plyrN)
                self.app.playerById[plyrN] = newU
            self.app.plyrOrd = [1, 2, 3, 4]
            if myI in [2, 3]:
                self.app.plyrOrd = self.app.plyrOrd[myI:] + self.app.plyrOrd[:myI-1]
            if myI == 1: self.app.plyrOrd = [2, 3, 4]
            if myI == 4: self.app.plyrOrd = [1, 2, 3]
            print(self.app.plyrOrd)
            print("IM JOING THE GAME")
            self.app.connectingLabel["text"] = "Connecting to Game..."
            time.sleep(1)
            self.app.game_manager.joinGame()

            data = ""
            while True:
                if data == "": data = self.app.conn.recieve()
                print(data)
                if data.startswith("DISCON:-"):
                    newTurnNum = self.app.turn
                    while True:
                        dscnt_Plyr = int(data.replace("DISCON:-", "").split("_]|")[0])
                        self.app.deadPlyrs += [dscnt_Plyr]
                        if len(self.app.deadPlyrs) == 3:
                            newTurnNum = "GameOver"
                            break
                        self.app.Tdice -= self.app.playerById[dscnt_Plyr].dice
                        self.app.playerById[dscnt_Plyr].dice = 0

                        self.app.c.itemconfig(self.app.playerById[dscnt_Plyr].board, fill="gray44")
                        for x in self.app.playerById[dscnt_Plyr].GUIhand:
                            x.unroll()
                            del x
                        self.app.playerById[dscnt_Plyr].GUIhand = []

                        if self.app.turn == dscnt_Plyr:
                            self.app.turn = self.app.game_manager.calc_next_Turn()
                            print(self.app.turn)



                        if data > 12: data = data[12:]
                        else: data = ""
                        if not data.startswith("DISCON:-"): break
                    if newTurnNum == "GameOver":
                        self.app.game_manager.gameover()
                        break
                    if self.app.turn != newTurnNum:
                        self.app.cnvCntrl_State(0)
                        for x in self.app.canvCntrl:
                            self.app.c.delete(x)
                        self.app.game_manager.newRound(0)

                if data.startswith("YourNewHand:-"):
                    self.app.User.hand = []
                    stR = data.replace("YourNewHand:-", "")
                    for ChR in stR:
                        try:
                            self.app.User.hand += [int(ChR)]
                        except:
                            break
                    self.app.User.GUIhand = self.app.draw_dice(1)
                    data=data.split("-||=-")[1]

                if data.startswith("HasRolled:-"):
                    id1 = int(data.replace("HasRolled:-", "")[0])
                    self.app.playerById[id1].rolled = True
                    self.app.playerById[id1].GUIhand = self.app.draw_dice(self.app.plyrOrd.index(id1)+2, self.app.playerById[id1].dice)
                    if len(data) > 13: data=data[13:]
                    else: data = ""

                if data.startswith("@newPlacedBet>:-"):
                    self.app.currBet = [int(thng) for thng in data.replace("@newPlacedBet>:-", "").split("+=|]")[0].split("-")]
                    self.app.c.itemconfig(self.app.betNumHolders[0], fill="green")
                    self.app.c.itemconfig(self.app.betNumHolders[1], fill="green")
                    self.app.c.itemconfig(self.app.betVal, text=str(self.app.currBet[0]))
                    self.app.c.itemconfig(self.app.betDie, text=str(self.app.currBet[1]))
                    time.sleep(2)
                    self.app.c.itemconfig(self.app.betNumHolders[0], fill="white")
                    self.app.c.itemconfig(self.app.betNumHolders[1], fill="white")
                    #display self.app.currBet
                    self.app.c.itemconfig(self.app.preBetVal, text=str(self.app.currBet[0]))
                    self.app.c.itemconfig(self.app.preBetDie, text=str(self.app.currBet[1]))

                    self.app.c.itemconfig(self.app.betVal, text="")
                    self.app.c.itemconfig(self.app.betDie, text="")
                    self.app.turn = self.app.game_manager.calc_next_Turn()
                    self.app.game_manager.newTurn()
                    data = data.split("+=|]")[1]
                if data.startswith("@:<fnl>:newPlacedBet>:-"):
                    self.app.currBet = data.replace("@:<fnl>:newPlacedBet>:-", "").split("+=|]")[0]
                    self.app.c.itemconfig(self.app.betNumHolders[0], fill="green")
                    self.app.c.itemconfig(self.app.betVal, text=str(self.app.currBet))
                    time.sleep(2)
                    self.app.c.itemconfig(self.app.betNumHolders[0], fill="white")
                    # display self.app.currBet
                    self.app.c.itemconfig(self.app.preBetVal, text=str(self.app.currBet))

                    self.app.c.itemconfig(self.app.betVal, text="")
                    self.app.turn = self.app.game_manager.calc_next_Turn()
                    self.app.game_manager.newTurn()
                    data = data.split("+=|]")[1]

                if data.startswith("LieClaim<"):
                    self.app.allowCnvEdit = False
                    lst = data.replace("LieClaim<", "").split("||-")[0].split("-")
                    if lst[0] == "": lst = lst[1:]
                    stat, claim = lst[0],lst[1]; lst = lst[2:]
                    for i in self.app.plyrOrd:
                        smthn = self.app.playerById[i].GUIhand
                        plyrHnd = lst[i-1]
                        for x in range(self.app.playerById[i].dice):
                            print(plyrHnd[x], "  ", x, smthn)
                            smthn[x].revealNum(plyrHnd[x])
                    """_____________________________________________
                    tkm.showinfo(
                        "({}) Played".format(str(self.app.turn)),
                        ("Called player {} a 'Liar' for the bet of atleast {} - {}s and there were actually {} - {}s\n" + ("player {} righteously called player {} a liar" if stat=="w" else "player {} falsely called player {} a liar")).format(
                            str(self.app.game_manager.calc_last_Turn()), str(self.app.currBet[0]), str(self.app.currBet[1]), claim, str(self.app.currBet[1]), str(self.app.turn), str(self.app.game_manager.calc_last_Turn())
                        )
                    )"""


                    ############
                    self.app.cnvCntrl_State(0)
                    for x in self.app.canvCntrl:
                        self.app.c.delete(x)

                    self.app.c.itemconfig(self.app.playerById[self.app.game_manager.calc_last_Turn()].board, fill="orange2")
                    if not self.app.finalR: self.app.c.itemconfig(self.app.betLbl, text="LIAR?[{}x{}s]?".format(str(self.app.currBet[0]), str(self.app.currBet[1])))
                    else: self.app.c.itemconfig(self.app.betLbl, text="LIAR?[+{}+]?".format(str(self.app.currBet)))
                    self.app.c.itemconfig(self.app.betNumHolders[0], fill="orange2")
                    if not self.app.finalR: self.app.c.itemconfig(self.app.betNumHolders[1], fill="orange2")
                    self.app.c.itemconfig(self.app.betVal, text="0")
                    if not self.app.finalR: self.app.c.itemconfig(self.app.betDie, text=str(self.app.currBet[1]))
                    time.sleep(1.5)
                    thng101 = 0
                    """ ........................"""  #<<<<<<<<<<<
                    for x in range(4):
                        Xturn = (self.app.turn+x)%4 if (self.app.turn+x)%4 else 4
                        if Xturn in self.app.deadPlyrs:
                            continue
                        lst = list(self.app.playerById[Xturn].GUIhand)
                        if Xturn != self.app.User.playerNum:
                            if self.app.plyrOrd.index(Xturn) == 0:
                                lst.reverse()
                        else:
                            lst.reverse()
                        for sngleDie in lst:
                            if self.app.finalR:
                                sngleDie.shade()
                                thng101 += sngleDie.val
                            else:
                                sngleDie.shade(self.app.currBet[1])
                                if sngleDie.val in [1, self.app.currBet[1]]:
                                    thng101 += 1
                            self.app.c.itemconfig(self.app.betVal, text=str(thng101))
                            time.sleep(0.2)
                    time.sleep(1)



                    loser = 0
                    if stat == "w":
                        self.app.c.itemconfig(self.app.betNumHolders[0], fill="red")
                        if not self.app.finalR: self.app.c.itemconfig(self.app.betNumHolders[1], fill="red")
                        self.app.c.itemconfig(self.app.betLbl, text="LIE!!", fill="red")
                        self.app.c.itemconfig(self.app.playerById[self.app.game_manager.calc_last_Turn()].board, fill="red")
                        self.app.c.itemconfig(self.app.playerById[self.app.turn].board, fill="green")
                        loser = self.app.game_manager.calc_last_Turn()
                    else:
                        self.app.c.itemconfig(self.app.betLbl, text="NO LIE")
                        self.app.c.itemconfig(self.app.playerById[self.app.turn].board, fill="red")
                        self.app.c.itemconfig(self.app.playerById[self.app.game_manager.calc_last_Turn()].board, fill="green")
                        loser = self.app.turn

                    time.sleep(1)
                    for i in range(2):
                        self.app.c.itemconfig(self.app.playerById[loser].board, fill="black")
                        time.sleep(0.1)
                        self.app.c.itemconfig(self.app.playerById[loser].board, fill="red")
                        time.sleep(0.1)
                    lostDie = self.app.playerById[loser].GUIhand[-1]
                    for i in range(2):
                        self.app.c.itemconfig(lostDie.Die, fill="red", outline="red")
                        time.sleep(0.2)
                        self.app.c.itemconfig(lostDie.Die, fill="white", outline="black")
                        time.sleep(0.2)
                    time.sleep(0.4)
                    self.app.c.itemconfig(lostDie.Die, fill="red", outline="red")


                    self.app.playerById[loser].dice -= 1
                    if self.app.playerById[loser].dice == 0:
                        self.app.deadPlyrs += [loser]
                        if self.app.finalR:
                            self.app.game_manager.gameover()
                            break
                        if loser == self.app.User.playerNum:
                            self.app.betBtn.pack_forget(); self.app.liarBtn.pack_forget()
                            Label(text="------------------------------SPECTATING------------------------------", bg="light gray", font="Times 20").pack()

                    time.sleep(1)

                    for i in range(1,5):
                        self.app.playerById[i].hand = []
                        for x in self.app.playerById[i].GUIhand:
                            x.unroll()
                            del x
                        self.app.playerById[i].GUIhand = []
                    ############

                    self.app.game_manager.newRound(loser)
                    data = data.split("||-")[1]
                    self.app.conn.send(str.encode(">recieveUpdate"))
                    bulean = True
                    while bulean:
                        IdsString = self.app.conn.recieve()
                        print(IdsString)
                        if "Update:" in IdsString:
                            for i in IdsString.split("Update:")[1].split("[/.]|")[0].split("-")[0]:
                                print(":::::]]]]] " + i)
                                if int(i) != self.app.User.playerNum:
                                    print("::: "+i)
                                    self.app.playerById[int(i)].rolled = True
                                    self.app.playerById[int(i)].GUIhand = self.app.draw_dice(self.app.plyrOrd.index(int(i)) + 2,
                                                                                     self.app.playerById[int(i)].dice)
                            print("+++==---++>>> "+ IdsString.split("Update:")[1].split("[/.]|")[0].split("-")[1])
                            for i in IdsString.split("Update:")[1].split("[/.]|")[0].split("-")[1]:
                                if int(i) not in self.app.deadPlyrs: data += "DISCON:-{}_]|".format(i)
                            bulean = False


                if data == ">allRoll>":
                    self.app.c.delete(self.app.rollWait)
                    if self.app.round == 1:
                        for i in range(1, 5):
                            if i not in self.app.deadPlyrs:
                                self.app.turn = i
                                break
                    self.app.drawGameFeatures()
                    self.app.game_manager.newTurn()
                    if len(data) > 9: data = data[9:]
                    else: data = ""