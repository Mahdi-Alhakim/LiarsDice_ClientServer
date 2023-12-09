class Die:
    def __init__(self, canv, x, y, size, num=0):
        self.c = canv
        self.x = x; self.y = y; self.size = size

        self.val = None

        self.text = None
        self.Die = self.c.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size, fill="white")

        if num:
            self.val = num
            self.revealNum(self.val)
    def revealNum(self, n, bettedDie=0):
        self.val = int(n)
        self.text = self.c.create_text(self.x+self.size/2, self.y+self.size/2, text=str(n), fill="red", font=("Persian", 23))
        if n == bettedDie or (bettedDie and n == 1):
            self.c.itemconfig(self.Die, fill="orange2")
    def shade(self, bettedDie=0):
        if self.val in [1, bettedDie] or not bettedDie: self.c.itemconfig(self.Die, fill="orange2")
    def unroll(self):
        self.c.delete(self.Die)
        if self.text: self.c.delete(self.text)