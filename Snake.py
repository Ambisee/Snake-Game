# --- Modules --- #
from win32api import GetSystemMetrics
from Modules_Configs.functions import *
from Modules_Configs.gameObjects import *
from Modules_Configs.config import *
from Modules_Configs.scoreObjects import *
from random import choice
import pygame
import time
import sys
import os

pygame.init()

# --- Main Function --- #
def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{GetSystemMetrics(0) // 2 - WIDTH // 2}, {GetSystemMetrics(1) // 2 - HEIGHT // 2}"
    clock = pygame.time.Clock()
    FPS = 20
    pause = 0
    start = False
    font = pygame.font.Font(os.path.abspath("Resources/SourceCodePro-Medium.ttf"), 32)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    sBoard = Scoreboard(font)
    player = Snake(20, 20)
    food = Food(player)

    while True:
        screen.fill((0, 0, 0))
        clock.tick(FPS / 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if food.isEaten():
            player.addBody()
            sBoard.updateScore()
            food.newLocation()

        if player.checkCollision():
            start = False
            resetGame(player, food)
            while pause < FPS:
                drawEnd(screen, font, sBoard.score)
                pygame.display.update()
                pause += 1
                time.sleep(0.1)

            # ---
            # Insert code to upload score and name
            # ---

            sBoard.reset()
            pause = 0
            continue

        player.checkKey()
        
        if player.start != False:
            player.move()

        food.draw(screen)
        player.draw(screen)
        sBoard.draw(screen)

        pygame.display.update()

# --- Execute --- #
if __name__ == "__main__":
    main()