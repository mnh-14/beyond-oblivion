import os
import sys
import pygame
from settings import Constant
from objects import Object, Player

class Game:
    def __init__(self, screen:pygame.Surface) -> None:
        self.fps_clock = pygame.time.Clock()
        self.screen = screen
        self.char = Player(os.path.join(*Constant.TILEMAP['c']))
        self.game_objects = Game.create_game_world(1)
        self.game_objects.append(self.char)
        self._set_camera()


    # def gamelogic(self):
    #     while True:
    def _set_camera(self):
        self.camera = self.screen.get_rect().copy()
        self.camera.center = self.char.rect.center

    def gameplay(self):
        while True:
            self.screen.fill((0,0,0))
            self.handle_graphic()
            self.handle_event()
            self.handle_logic()
            pygame.display.flip()
            self.fps_clock.tick(Constant.FPS)
    
    def handle_graphic(self):
        for o in self.game_objects:
            o.show(self.screen, self.camera)
    

    def handle_logic(self):
        self.char.move()
        self.camera.center = self.char.rect.center
    
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                self.char.handle_keydown(event.key)
            
            if event.type == pygame.KEYUP:
                self.char.handle_keyup(event.key)
    

    @staticmethod
    def create_game_world(world_no:int):
        game_world_objects: list[Object] = []
        with open(os.path.join(*Constant.GAME_WORLD[1]), 'r') as game_text:
            nx,ny=0,0
            for line in game_text:
                nx=0
                for ch in line.strip():
                    if ch=='0':
                        nx += 1
                        continue
                    o = Object(str(os.path.join(*Constant.TILEMAP[ch])))
                    o.set_position(nx*Constant.BOX[0], ny*Constant.BOX[1])
                    game_world_objects.append(o)
                    nx += 1
                ny += 1
        
        return game_world_objects
                    

                
