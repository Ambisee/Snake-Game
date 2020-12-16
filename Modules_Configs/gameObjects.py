# --- Modules --- #
from random import choice
import pygame

if __name__ == '__main__':
    from config import *
else:
    from Modules_Configs.config import *
# --- Classes --- #
class Cube:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.lastRow = row
        self.lastCol = col
        self.color = WHITE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.col * EDGE, self.row * EDGE, EDGE, EDGE))
    
    def drawImg(self, window, img):
        window.blit(img, (self.col * EDGE, self.row  * EDGE))

class Snake:
    def __init__(self, col, row):
        self.head = Cube(row, col)
        self.color_index = 0

        self.body = []
        self.body.append(self.head)
        self.body.extend([Cube(row, col-1), Cube(row, col-2)])
        self.body[1].color = body_colors[0]
        self.body[2].color = body_colors[1]
        self.start = False
        self.image = headImgRight

        self.x_vel = 1
        self.y_vel = 0

    def moveHead(self): # Not for main function
        self.head.lastCol = self.head.col
        self.head.lastRow = self.head.row

        self.head.col += self.x_vel
        self.head.row += self.y_vel

        if self.head.col < 0:
            self.head.col = RC - 1
        elif self.head.col >= RC:
            self.head.col = 0
        if self.head.row < 0:
            self.head.row = RC - 1
        elif self.head.row >= RC:
            self.head.row = 0

    def checkKey(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.x_vel != 1:
                self.x_vel = -1
                self.y_vel = 0
                self.start = True
                self.image = headImgLeft
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.x_vel != -1:
                self.x_vel = 1
                self.y_vel = 0
                self.start = True
                self.image = headImgRight
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.y_vel != 1:
                self.x_vel = 0
                self.y_vel = -1
                self.start = True
                self.image = headImgUp
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.y_vel != -1:
                self.x_vel = 0
                self.y_vel = 1
                self.start = True
                self.image = headImgDown

    def move(self):
        self.moveHead()
        for i in range(1, len(self.body)):
            self.body[i].lastRow = self.body[i].row
            self.body[i].lastCol = self.body[i].col
            self.body[i].row = self.body[i - 1].lastRow
            self.body[i].col = self.body[i - 1].lastCol
    
    def addBody(self):
        self.body.append(Cube(self.body[-1].lastRow, self.body[-1].lastCol))
        self.body[len(self.body) - 1].color = body_colors[self.color_index % 2]
        self.color_index += 1
    
    def checkCollision(self):
        for i in range(3,len(self.body)):
            if (self.head.row, self.head.col) == (self.body[i].row, self.body[i].col):
                return True

    def reset(self, row, col):
        self.head = Cube(row, col)
        self.color_index = 0

        self.body = []
        self.body.append(self.head)
        self.body.extend([Cube(row, col-1), Cube(row, col-2)])
        self.body[1].color = body_colors[0]
        self.body[2].color = body_colors[1]
        self.start = False
        self.image = headImgRight

        self.x_vel = 1
        self.y_vel = 0

    def draw(self, window):
        self.body[0].drawImg(window, self.image)
        for part in self.body[1:]:
            part.draw(window)

class Scoreboard:
    def __init__(self, font):
        self.width = WIDTH
        self.height = HEIGHT - (RC * EDGE)
        self.x = 0
        self.y = RC * EDGE
        self.color = WHITE
        self.font = font
        self.surface = pygame.Surface((self.width, self.height))
        self.score = 0
        self.label = font.render(f"Score = {self.score}", True, (0, 0, 0))

    def updateScore(self):
        self.score += 1
        self.label = self.font.render(f"Score = {self.score}", True, (0, 0, 0))
    
    def reset(self):
        self.score = 0
        self.label = self.font.render("Score = 0", True, (0, 0, 0))

    def draw(self, window):
        window.blit(self.surface, (self.x, self.y))
        self.surface.fill(WHITE)
        self.surface.blit(self.label, (self.width * 3 // 4 - self.label.get_width() // 2, self.height // 2 - self.label.get_height() // 2))

class Food:
    def __init__(self, snake):
        self.snake = snake
        self.cubes = self.updateGrid()
        self.row = None
        self.col = None
        self.newLocation()
    
    def updateGrid(self): # Not for main function
        self.cubes = [(i, j) for i in range(RC) for j in range(RC)]
        for parts in self.snake.body:
            self.cubes.remove((parts.row, parts.col))

    def newLocation(self):
        self.updateGrid()
        self.row, self.col = choice(self.cubes)
    
    def isEaten(self):
        if self.row == self.snake.head.row and self.col == self.snake.head.col:
            return True
        return False

    def draw(self, window):
        pygame.draw.rect(window, (255,255,255), (self.col * EDGE, self.row * EDGE, EDGE, EDGE))