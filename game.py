from __future__ import annotations
import os
import select
import sys
from typing import Any, List
import pygame
from pygame.sprite import AbstractGroup
from settings import Constant
from objects import Object, Player

class Game:
    LOGIC = "l"
    GRAPHICS = "g"
    EVENTS = "e"
    def __init__(self, screen:pygame.Surface) -> None:
        self.fps_clock = pygame.time.Clock()
        self.screen = screen
        self.char = Player(os.path.join(*Constant.TILEMAP['c']))
        self.char.set_position(*self.screen.get_rect().center)
        self._set_camera()
        self.camera = Camera(self.screen.get_rect())
        self.game_object_group = Game.create_game_world(1, self.camera)
        # self.game_object_group.add(self.char)
        self.current_phase = "ch-0"
        self.phases = {
            "ch": {
                "0": {Game.LOGIC: self.chapter0, Game.GRAPHICS: self.view_chapter0, Game.EVENTS: self.chapter0_events},
                "1": {Game.LOGIC: self.chapter0, Game.GRAPHICS: self.view_chapter0, Game.EVENTS: self.chapter0_events}
            },
            "cut":{
                "0":{}
            }

        }


    def _set_camera(self):
        self.camera = self.screen.get_rect().copy()
        self.camera.center = self.char.rect.center


    def chapter0(self):
        # self.char.move()
        self.char.update(sprites=self.game_object_group.camera_captured_sprites())
        # self.camera.center = self.char.rect.center
        self.camera.follow_target(self.char.rect)


    def view_chapter0(self):
        self.game_object_group.draw(self.screen)
        self.char.show(self.screen, self.camera)

    
    def chapter0_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                self.char.handle_keydown(event.key)
            
            if event.type == pygame.KEYUP:
                self.char.handle_keyup(event.key)
        




    def gameplay(self):
        while True:
            self.screen.fill((0,0,0))
            ph, ph_no = self.current_phase.split("-")
            self.phases[ph][ph_no][Game.EVENTS]()
            self.phases[ph][ph_no][Game.LOGIC]()
            self.phases[ph][ph_no][Game.GRAPHICS]()
            pygame.display.flip()
            self.fps_clock.tick(Constant.FPS)
    
    def handle_graphic(self):
        self.game_object_group.draw(self.screen)
        self.char.show(self.screen, self.camera)
    

    def handle_logic(self):
        # self.char.move()
        self.char.update(spritegroup=self.game_object_group)
        # self.camera.center = self.char.rect.center
        # col_rect = pygame.sprite.spritecollideany(self.char, self.game_object_group)
        # self.char.movement_impact(col_rect)
        self.camera.follow_target(self.char.rect)
    
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
                    game_objects_group.add(o)
                    nx += 1
                ny += 1
        
        # return game_world_objects
        return game_objects_group
                    

                


class CameraGroup(pygame.sprite.Group):
    def __init__(self, *sprites: Any | AbstractGroup, camera:Camera) -> None:
        super().__init__(*sprites)
        self.camera = camera
    
    def draw(self, surface: pygame.Surface, bgsurf: pygame.Surface | None = None, special_flags: int = 0) -> List[pygame.Rect]:
        sprites = self.camera_captured_sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits(
                        (spr.image, self.camera.relative_rect(spr.rect), None, special_flags) for spr in sprites
                    ),
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(
                    spr.image, self.camera.relative_rect(spr.rect), None, special_flags
                )
        self.lostsprites = []
        dirty = self.lostsprites
        return dirty

    def camera_captured_sprites(self):
        sprites = self.sprites()
        flagged_sprites = []
        for spr in sprites:
            if self.camera.captured_objects(spr.rect):
                flagged_sprites.append(spr)
        return flagged_sprites
    
    # def relative_rect(self, rect:pygame.Rect):
    #     rel_rect = rect.copy()
    #     rel_rect.x = rect.x - self.camera.x
    #     rel_rect.y = rect.y - self.camera.y
    #     return rel_rect




class Camera:
    def __init__(self, screen_rect:pygame.Rect) -> None:
        self.rect = screen_rect.copy()

    def relative_rect(self, rect:pygame.Rect):
        rel_rect = rect.copy()
        rel_rect.x = rect.x - self.rect.x
        rel_rect.y = rect.y - self.rect.y
        return rel_rect
    
    def captured_objects(self, object_rect:pygame.Rect):
        return self.rect.colliderect(object_rect)
    
    def follow_target(self, target: pygame.Rect):
        self.rect.center = target.center