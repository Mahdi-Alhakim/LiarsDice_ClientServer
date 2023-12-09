import socket
from threading import Thread
import time

from processing import Process
from user import User

class Server:
    def __init__(self):
        self.users = {}
        self.players = {}
        self.names = []
        self.deadPlyrs = []
        self.gameStarted, self.allRoll, self.finalR = False, False, False
        self.Tdice = 20
        self.round = 1
        self.roundStarter = 1
        self.turn = 0
        self.currBet = [0, 0]
        self.exit1 = False

        self.process = Process(self)

        self.conSetup()

    def conSetup(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((socket.gethostbyname(socket.gethostname()), 5050))
        self.s.listen(4)

        self.t = Thread(target=self.acceptLoop)
        self.t.start()
        self.t.join()
        self.s.close()

    def end(self):
        self.exit1 = True

    def acceptLoop(self):
        while True:
            client, address = self.s.accept()
            self.users[client] = [address]
            Thread(target=self.handle_client, args=(client,)).start()
            if self.exit1:
                time.sleep(0.6)
                for i in list(self.users.keys()):
                    del self.users[i][1]
                self.gameStarted = False
                self.names = []
                self.__init__()
                break

    def handle_client(self, client):
        name = client.recv(1024).decode("utf8")
        if not name:
            print("Client: '{}' ::DISCONNECTED".format(self.users[client][1].name))
            self.names.remove(self.users[client][1].name)
            del self.players[self.users[client][1].playerNum]
            del self.users[client]
            return

        if not(name in self.names) and len(self.names) < 4 and not self.gameStarted:
            place = -1
            for x in range(1,5):
                if self.players.get(x, -1) == -1:
                    self.players[x] = (client, name)
                    place = x
                    break
            self.users[client] += [User(name, place)]
            self.names += [name]
            client.send(str.encode("acc-:{}".format(str(place))))
            print("Client: '{}' ::ACCEPTED".format(self.users[client][1].name))
            if len(self.names) == 4:
                self.gameStarted = True
                for c in list(self.users.keys()):
                    txt = "GAMESTART:-{}_|-|{}_|-|{}_|-|{}".format(self.players[1][1], self.players[2][1], self.players[3][1], self.players[4][1])
                    c.send(str.encode(txt))
                print("|GAME HAS STARTED| -->>  [(4/4) players]")
        elif len(self.names) == 4 or self.gameStarted:
            client.send(str.encode("full"))
            del self.users[client]
            return
        else:
            client.send(str.encode("Uden"))
            del self.users[client]
            return


        #The Server's Gameloop for each client
        thisId = self.users[client][1].playerNum
        while True:
            data = client.recv(1024).decode("utf8")
            if (data == "EXIT" or not data) and not self.exit1:
                print("Client: '{}' ::DISCONNECTED".format(self.users[client][1].name))
                self.names.remove(self.users[client][1].name)
                self.deadPlyrs += [thisId]
                self.Tdice -= self.users[client][1].dice
                self.users[client][1].hand = []
                self.users[client][1].dscnct = True

                if len(self.deadPlyrs) >= 3: self.end()
                if thisId == self.turn:
                    self.allRoll = False
                    for i in list(self.users.keys()):
                        self.users[i][1].rolled = False
                    self.turn = self.process.calc_next_Turn()
                    self.roundStarter = self.turn

                    if self.Tdice == 2:
                        self.finalR = True
                        self.currBet = 0
                    else:
                        self.currBet = [0, 0]
                if not self.allRoll and not self.users[client][1].rolled:
                    data = "Rolled"


                for i in list(self.users.keys()):
                    if not self.users[i][1].dscnct:
                        i.send(str.encode("DISCON:-{}_]|".format(thisId)))
            if data.startswith(">recieveUpdate"):
                IdsString = ""
                dscnct = ""
                for i in list(self.users.keys()):
                    if i != thisId:
                        if not self.users[i][1].dscnct:
                            if self.users[i][1].rolled:
                                IdsString += str(self.users[i][1].playerNum)
                        else:
                            dscnct += str(self.users[i][1].playerNum)
                print(IdsString + "<><><><><<>><")
                client.send(str.encode("Update:{}-{}[/.]|".format(IdsString, dscnct)))
                data = data.replace(">recieveUpdate", "")
            if self.gameStarted:
                if not(self.allRoll) and data == "Rolled":
                    self.users[client][1].rolled = True
                    newH = self.process.create_Hand(self.users[client][1].dice)
                    strng = ""
                    for me in newH:
                        strng += str(me)
                    self.users[client][1].hand = newH
                    client.send(str.encode("YourNewHand:-{}-||=-".format(strng)))
                    cntr = 0
                    for i in list(self.users.keys()):
                        cntr += 1 if (self.users[i][1].rolled or self.users[i][1].playerNum in self.deadPlyrs) else 0
                        if not (i == client):
                            if not self.users[i][1].dscnct:
                                i.send(str.encode("HasRolled:-{}-".format(thisId)))
                    if cntr == 4:
                        self.allRoll = True
                        for i in list(self.users.keys()):
                            if not self.users[i][1].dscnct:
                                i.send(str.encode(">allRoll>"))
                        if self.round == 1:
                            for i in range(1, 5):
                                if i not in self.deadPlyrs:
                                    self.turn = i
                                    break
                print(self.turn, "<<<<<<<<<<<<<<<<<<<<<<")
                if self.allRoll and thisId == self.turn:
                    self.process.processGameComm(thisId, data)
                    time.sleep(0.6)
                    if thisId in self.deadPlyrs:
                        return
                if self.exit1: return
