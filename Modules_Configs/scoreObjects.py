# --- Modules --- #
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import pygame
import sys

if __name__ == "__main__":
    from config import *
else:
    from Modules_Configs.config import *


# --- Classes --- #
class ScoreWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('Snake Game - Scoreboard')
        self.resizable(height=False, width=False)
        self.protocol("WM_WINDOW_DELETE", self.destroy)

        self.topFrame = Frame(self)
        self.middleFrame = Frame(self)
        self.bottomFrame = Frame(self)

        self.topFrame.pack()
        self.middleFrame.pack()
        self.bottomFrame.pack()

        self.titleLabel = Label(self.topFrame, text="Score Board", font=('System', 20))
        self.sList = ScoreList(self.middleFrame)
        self.delButton = Button(self.bottomFrame, text="Delete Score", font=("Courier", 13), command=self.deleteScore)
        self.returnButton = Button(self.bottomFrame, text='Return', font=("Courier", 13), command=self.destroy)
        
        self.titleLabel.pack()
        self.delButton.pack(side=RIGHT, padx=7, pady=10)
        self.sList.pack(padx=10, pady=5)
        self.returnButton.pack(side=RIGHT, padx=7, pady=10)

        self.update()
        self.focus_force()
        self.geometry(f"+{self.winfo_screenwidth() // 2 - self.winfo_reqwidth() // 2}+{self.winfo_screenheight() // 2 - self.winfo_reqheight() // 2}")

        self.printScore()

    def printScore(self):
        with open("Resources/Scores.txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                inputVals = line.split(',')
                self.sList.insert('', 'end', len(self.sList.get_children()), values=tuple(inputVals))

    def nothingness(self):
        pass

    def deleteScore(self):
        if not self.sList.selection():
            return

        self.bind("<FocusOut>", lambda e: self.nothingness)
        deleteValues = self.sList.item(self.sList.selection())['values']
        confirmation = messagebox.askokcancel("Confirmation", "Are you sure you want to delete this score ?")
        if confirmation == True:
            with open("Resources/Scores.txt", 'r') as f:
                lines = f.readlines()
        
            with open("Resources/Scores.txt", 'w') as f:
                for line in lines:
                    line = line.replace('\n', '')
                    value = line.split(',')
                    value[1] = int(value[1])
                    if value != deleteValues:
                        f.write(f'{value[0]},{str(value[1])}\n')
            
            self.sList.delete(*self.sList.get_children())
            self.printScore()
            self.bind("<FocusOut>", self.focusOutDestroy)
    
    def focusOutDestroy(self, event):
        super().destroy()
        del self

    def printValues(self):
        print(self.sList.item(self.sList.selection()))
        print(self.sList.get_children())

class ScoreList(ttk.Treeview):
    def __init__(self, master):
        super().__init__(master, selectmode='browse', show='headings')
        
        self.setColumns()
        self.setHeadings()

    def setColumns(self):
        self['columns'] = ('1', '2')
        self.column("1", width=150, stretch=NO)
        self.column("2", width=150, stretch=NO)
    
    def setHeadings(self):
        self.heading('1', text="Name")
        self.heading('2', text="Score")

class ScoreSaver(ScoreWindow):
    def __init__(self, score):
        super().__init__()
        self.withdraw()

        self.topWindow = Toplevel(self)
        self.topWindow.title("Insert Name")
        self.topWindow.protocol("WM_DELETE_WINDOW", self.topQuit)
        self.topWindow.deiconify()

        self.topLabel = Label(self.topWindow, text="Insert your name to save your score :", font=("System", 20))
        self.nameRetriever = Entry(self.topWindow, width=60, border=3)
        self.topButton = Button(self.topWindow, text="Submit",font=("Courier", 14), command=self.postScore)

        self.topLabel.pack()
        self.nameRetriever.pack(pady=10)
        self.topButton.pack(pady=5)

        self.score = score  

        self.topWindow.update()
        self.topWindow.geometry("+{}+{}".format(self.topWindow.winfo_screenwidth() // 2 - self.topWindow.winfo_reqwidth() // 2, self.topWindow.winfo_screenheight() // 2 - self.topWindow.winfo_reqheight() // 2))
        self.mainloop()

    def topQuit(self):
        self.topWindow.destroy()
        self.update()
        self.deiconify()

    def postScore(self):
        if self.nameRetriever.get() != "":
            name = self.nameRetriever.get()
            score = self.score

            with open('Resources/Scores.txt', 'a') as f:
                f.write(f"{name},{score}\n")
            
        self.printScore()
        self.topQuit()

class ScoreButton:
    def __init__(self):
        self.y = HEIGHT + (WIDTH - HEIGHT) // 2
        self.x = 15
        self.width = 120
        self.height = 70
        self.border = 5
        self.borderRect = pygame.Rect(self.x, self.y - self.height // 2, self.width , self.height)
        self.borderSurface = pygame.Surface((self.width, self.height))
        self.mainSurface = pygame.Surface((self.width - 2 * self.border, self.height - 2 * self.border))
        
        self.color = [pygame.Color('grey'), pygame.Color('white')]
        self.colorIndex = 0

        self.borderSurface.fill((0,0,0))
        self.mainSurface.fill(self.color[self.colorIndex])
        self.text = pygame.font.SysFont('Courier', 17).render('ScoreBoard', True, BLACK)
        
    def draw(self, window):
        self.mainSurface.fill(self.color[self.colorIndex])
        window.blit(self.borderSurface, (self.borderRect))
        self.mainSurface.blit(self.text, (self.mainSurface.get_width() // 2 - self.text.get_width() // 2, self.mainSurface.get_height() // 2 - self.text.get_height() // 2))
        self.borderSurface.blit(self.mainSurface, (5, 5))
    
    def checkClick(self):
        clicked = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        if x in range(self.borderRect.left, self.borderRect.right) and y in range(self.borderRect.top, self.borderRect.bottom):
            self.colorIndex = 1
            if 1 in clicked:
                initScoreWindow()
        else:
            self.colorIndex = 0

def initScoreWindow():
    y = ScoreWindow()
    y.bind("<FocusOut>", y.focusOutDestroy)
    y.mainloop()

if __name__ == '__main__':
    initScoreWindow()