import pygame

from game import Game
from settings import Constant


pygame.init()
screen = pygame.display.set_mode(Constant.SCREEN_RES)
pygame.display.set_caption(Constant.GAME_NAME)



if __name__=="__main__":
    game = Game(screen)
    game.gameplay()