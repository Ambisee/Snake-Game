# --- Modules --- #
import pygame

try:
    import config
except:
    from Modules_Configs import config

# --- Functions --- #
def drawEnd(window, font, score):
    label = font.render("Final Score = {}".format(score), True, (255, 255, 255))
    window.blit(label ,(window.get_width() // 2 - label.get_width() // 2, window.get_height() // 2 - label.get_height() // 2))

def resetGame(snake, food):
    snake.reset(20, 20)
    food.newLocation()