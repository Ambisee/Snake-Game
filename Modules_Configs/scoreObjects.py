# --- Modules --- #
from tkinter import *

# --- Classes --- #
class ScoreWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title("Snake - Scores")
        self.window.resizable(height=False, width=False)
        self.window.protocol("WM_DELETE_WINDOW", self.window.quit)