class User:
    def __init__(self, name, playerNum):
        self.name = name
        self.playerNum = playerNum
        self.hand = []
        self.GUIhand, self.board = [], None
        self.rolled = False
        self.dice = 5