import socket
from user import User

class Conn:
    def __init__(self, app):
        self.app = app
        self.connected = False
        self.s = None

    def connect(self, currEntry):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((socket.gethostbyname(socket.gethostname()), 5050))
        self.s.send(str.encode(currEntry))
        acptnce = self.s.recv(1024).decode("utf8")
        if acptnce.startswith("acc-:"):
            self.connected = True
            self.app.User = User(currEntry, int(acptnce.replace("acc-:", "")))
            self.app.playerById[self.app.User.playerNum] = self.app.User
            self.app.savedName = currEntry
            self.app.game_manager.entergame()

        elif acptnce == "full":
            tkm.showerror("Denied", "Lobby is Full")
            self.s.close()
        elif acptnce == "Uden":
            tkm.showerror("Denied", "Username is taken")
            self.s.close()
    
    def send(self, m):
        self.s.send(m)
    def recieve(self):
        return self.s.recv(1024).decode("utf8")

    def on_closing(self):
        if self.connected:
            self.s.send(str.encode("EXIT"))
            self.s.close()
        
    def gameover(self):
        try:
            self.connected = False
            self.s.close()
        except: pass