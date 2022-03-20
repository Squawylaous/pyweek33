import pygame
from pygame.locals import *
from pygame import Vector2 as vector

pygame.init()

background = Color(0, 0, 0)
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
screen_rect = screen.get_rect()
screen.fill(background)


# class for entities that can move and stuff
class entity:
    def __init__(self):
        pass


# class for walls, will be packaged into a maze
class wall:
    def __init__(self):
        pass
