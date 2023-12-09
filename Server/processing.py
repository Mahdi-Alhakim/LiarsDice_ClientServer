import random

class Process:
    def __init__(self, app):
        self.app = app

    def processGameComm(self, clientId, Rcmnd):
        if Rcmnd == ">#Liar":
            if clientId == self.app.roundStarter: return

            lst = []
            dieQnt = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
            Dsum = 0
            for x in range(1, 5):
                Handstir = ""
                for singleDie in self.app.users[self.app.players[x][0]][1].hand:
                    Handstir += str(singleDie)
                    Dsum += singleDie
                    if singleDie == 1:
                        for elmnt in range(1, 7):
                            dieQnt[elmnt] += 1
                    else:
                        dieQnt[singleDie] += 1
                lst += [Handstir]
            if not self.app.finalR: print(dieQnt[self.app.currBet[1]], "<<<< QNT of betted dice")
            for i in list(self.app.users.keys()):
                self.app.users[i][1].rolled = False
                if not self.app.users[i][1].dscnct:
                    if not self.app.finalR:
                        i.send(str.encode("LieClaim<{}-{}-{}-{}-{}-{}||-".format(
                            "w" if dieQnt[self.app.currBet[1]] < self.app.currBet[0] else "l", str(dieQnt[self.app.currBet[1]]),
                            lst[0], lst[1], lst[2], lst[3]
                        )))
                    else:
                        print(Dsum, self.app.currBet, Dsum < self.app.currBet, "w" if Dsum < self.app.currBet else "l")
                        i.send(str.encode("LieClaim<{}-{}-{}-{}-{}-{}||-".format(
                            "w" if Dsum < self.app.currBet else "l", str(Dsum),
                            lst[0], lst[1], lst[2], lst[3]
                        )))

            loserPlyr = 0
            if not self.app.finalR:
                if dieQnt[self.app.currBet[1]] < self.app.currBet[0]:
                    lastT = self.calc_last_Turn()
                    loserPlyr = lastT
                    self.app.users[self.app.players[lastT][0]][1].dice -= 1
                    if self.app.users[self.app.players[lastT][0]][1].dice == 0:
                        self.app.deadPlyrs += [lastT]
                else:
                    loserPlyr = clientId
                    self.app.users[self.app.players[clientId][0]][1].dice -= 1
                    if self.app.users[self.app.players[clientId][0]][1].dice == 0:
                        self.app.deadPlyrs += [clientId]
            else:
                self.app.end()
                return
            if len(self.app.deadPlyrs) == 3:
                self.app.end()
                return

            self.app.allRoll = False
            self.app.Tdice -= 1
            self.app.round += 1

            self.app.turn = loserPlyr
            self.app.turn = self.calc_next_Turn() if (loserPlyr in self.app.deadPlyrs) else loserPlyr
            self.app.roundStarter = self.app.turn

            if self.app.Tdice == 2:
                self.app.finalR = True
                self.app.currBet = 0
            else:
                self.app.currBet = [0, 0]

        if Rcmnd.startswith(">#NewBet:-"):
            Nbet = [int(x) if x != "" else x for x in Rcmnd.replace(">#NewBet:-", "").split("-")]
            if "" in Nbet: return
            print(Nbet)
            if self.validateNewBet(Nbet):
                for i in list(self.app.users.keys()):
                    if not self.app.users[i][1].dscnct:
                        i.send(str.encode("@newPlacedBet>:-{}-{}+=|]".format(str(Nbet[0]), str(Nbet[1]))))
                self.app.roundStarter = 0
                self.app.currBet = Nbet
                self.app.turn = self.calc_next_Turn()
            else:
                print("Not validated!")

        if Rcmnd.startswith(">:<fnl>:#NewBet:-") and self.app.finalR:
            Nbet = int(Rcmnd.replace(">:<fnl>:#NewBet:-", "").split("-")[0])
            if self.validateNewBet(Nbet):
                for i in list(self.app.users.keys()):
                    if not self.app.users[i][1].dscnct:
                        i.send(str.encode("@:<fnl>:newPlacedBet>:-{}+=|]".format(str(Nbet))))
                self.app.roundStarter = 0
                self.app.currBet = Nbet
                self.app.turn = self.calc_next_Turn()
            else:
                print("Not validated!")
    
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
    def create_Hand(self, qnt=5):
        hand = []
        for i in range(qnt):
            hand += [random.choice(list(range(1, 7)))]
        return hand
    def validateNewBet(self, newbet):
        if not self.app.finalR:
            if newbet[0] < self.app.currBet[0] or newbet[0] < 1 or newbet[0] > self.app.Tdice: return False
            if newbet[0] == self.app.currBet[0] and newbet[1] <= self.app.currBet[1]: return False
            if newbet[1] < 1 or newbet[1] > 6: return False
        elif newbet <= self.app.currBet or newbet < 1 or newbet > 12: return False
        return True