import os
import sys
from typing import Any, List
import pygame
from pygame.sprite import AbstractGroup
from settings import Constant
from objects import Object, Player

class Game:
    def __init__(self, screen:pygame.Surface) -> None:
        self.fps_clock = pygame.time.Clock()
        self.screen = screen
        self.char = Player(os.path.join(*Constant.TILEMAP['c']))
        self._set_camera()
        # self.game_objects = Game.create_game_world(1)
        # self.game_objects.append(self.char)
        self.game_object_group = Game.create_game_world(1, self.camera)
        self.game_object_group.add(self.char)


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
        # for o in self.game_objects:
        #     o.show(self.screen, self.camera)
        self.game_object_group.draw(self.screen)
    

    def handle_logic(self):
        # self.char.move()
        self.char.update()
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
    def create_game_world(world_no:int, camera:pygame.rect.Rect):
        game_world_objects: list[Object] = []
        game_objects_group = CameraGroup(camera=camera)
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
                    game_objects_group.add(o)
                    nx += 1
                ny += 1
        
        # return game_world_objects
        return game_objects_group
                    

                


class CameraGroup(pygame.sprite.Group):
    def __init__(self, *sprites: Any | AbstractGroup, camera:pygame.Rect) -> None:
        super().__init__(*sprites)
        self.camera = camera
    
    def draw(self, surface: pygame.Surface, bgsurf: pygame.Surface | None = None, special_flags: int = 0) -> List[pygame.Rect]:
        sprites = self.camera_captured_sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits(
                        (spr.image, self.relative_rect(spr.rect), None, special_flags) for spr in sprites
                    ),
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(
                    spr.image, self.relative_rect(spr.rect), None, special_flags
                )
        self.lostsprites = []
        dirty = self.lostsprites
        return dirty

    def camera_captured_sprites(self):
        sprites = self.sprites()
        flagged_sprites = []
        for spr in sprites:
            if self.camera.colliderect(spr.rect):
                flagged_sprites.append(spr)
        return flagged_sprites
    
    def relative_rect(self, rect:pygame.Rect):
        rel_rect = rect.copy()
        rel_rect.x = rect.x - self.camera.x
        rel_rect.y = rect.y - self.camera.y
        return rel_rect
