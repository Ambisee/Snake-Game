# --- Modules --- #
import pygame
import os

pygame.init()

# --- Variables --- #
RC = 40
RCidx = RC - 1
WIDTH = 560
HEIGHT = 640
EDGE = WIDTH // RC

RED = (255, 0, 0)
P_ORANGE = (255, 213, 61)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
P_BLUE = (50, 108, 155)
WHITE = (255, 255, 255)

body_colors = [P_ORANGE, P_BLUE]

# --- Images --- #
headImg = pygame.transform.scale(pygame.image.load(os.path.join('Resources', 'Snake head.png')), (EDGE, EDGE))
headImgUp = headImg
headImgDown = pygame.transform.rotate(headImg, 180)
headImgLeft = pygame.transform.rotate(headImg, 90)
headImgRight = pygame.transform.rotate(headImg, -90)