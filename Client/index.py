from app import App
from tkinter import Tk

savedName = "Enter Name.."

if __name__ == "__main__":
    root = Tk()
    theApp = App(root, savedName)