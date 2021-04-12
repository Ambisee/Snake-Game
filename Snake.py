# --- Modules --- #
from win32api import GetSystemMetrics
from Modules_Configs.functions import *
from Modules_Configs.gameObjects import *
from Modules_Configs.config import *
from Modules_Configs.scoreObjects import *
import pygame
import time
import sys
import os

pygame.init()

# --- Main Function --- #
def main():
    # Initial Settings
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{GetSystemMetrics(0) // 2 - WIDTH // 2}, {GetSystemMetrics(1) // 2 - HEIGHT // 2}"
    clock = pygame.time.Clock()
    FPS = 20
    pause = 0
    start = False
    font = pygame.font.Font(os.path.abspath("Resources/SourceCodePro-Medium.ttf"), 32)

    # Initializing and Setting up the game objects
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    sBoard = Scoreboard(font)
    sButton = ScoreButton()
    player = Snake(20, 20)
    food = Food(player)

    while True:
        # Background fill and game tick
        screen.fill((0, 0, 0))
        clock.tick(FPS / 2)

        # Check for Window Close action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check if food is eaten
        if food.isEaten():
            player.addBody()
            sBoard.updateScore()
            food.newLocation()

        # Check if snake's head collides with its body
        if player.checkCollision():
            start = False
            resetGame(player, food)
            while pause < FPS:
                drawEnd(screen, font, sBoard.score)
                pygame.display.update()
                pause += 1
                time.sleep(0.1)

            # Open up ScoreSaver object to save the score under the user's name
            tempScore = sBoard.score
            ScoreSaver(tempScore)

            # Resets the game
            sBoard.reset()
            pause = 0
            continue

        # Change the snake's direction according to the pressed key
        player.checkKey()
        
        # Starts moving the snake if "start" variable of the player is True
        if player.start:
            player.move()
        # Score button checks for clicks instead if game is not running
        else:
            sButton.checkClick()

        # Draw the objects on the window
        food.draw(screen)
        player.draw(screen)
        sBoard.draw(screen)
        sButton.draw(screen)

        # Updates the window
        pygame.display.update()

# --- Execute --- #
if __name__ == "__main__":
    main()