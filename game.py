from __future__ import annotations
import os
import sys
from typing import Any, List
import pygame
from pygame.sprite import AbstractGroup
from chapters.chapter3 import Chapter3
from settings import Constant
from objects import Object, Player
from chapters.chapter0 import Chapter0

class Game:
    REFER = {
        "t": Object,
        "c": Player
    }
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
        self.game_dimension = ()
        # self.game_object_group.add(self.char)
        self.chapter0 = Chapter0()
        self.chapter0.initiate_chapter(self)
        self.current_phase = "ch-0"
        self.cphase = [self.chapter0]
        self._set_chapters()


    def _set_camera(self):
        return
        self.camera = self.screen.get_rect().copy()
        self.camera.center = self.char.rect.center
    
    def _set_chapters(self):
        chapter3 = Chapter3()
        chapter3.initiate_chapter(self)
        self.cphase.append(chapter3)
        self.current_phase = "ch-1"



    def gameplay2(self):
        while True:
            self.screen.fill((130, 130, 170))
            ph, ph_no = self.current_phase.split("-")
            self.cphase[int(ph_no)].handle_logic()
            self.cphase[int(ph_no)].handle_event()
            self.cphase[int(ph_no)].handle_graphics()
            pygame.display.flip()
            self.fps_clock.tick(Constant.FPS)


    def gameplay(self):
        return
        while True:
            self.screen.fill((130, 130, 170))
            ph, ph_no = self.current_phase.split("-")
            self.phases[ph][ph_no][Game.EVENTS]()
            self.phases[ph][ph_no][Game.LOGIC]()
            self.phases[ph][ph_no][Game.GRAPHICS]()
            pygame.display.flip()
            self.fps_clock.tick(Constant.FPS)
    
    def handle_graphic(self):
        return
        self.game_object_group.draw(self.screen)
        self.char.show(self.screen, self.camera)
    

    def handle_logic(self):
        return
        # self.char.move()
        self.char.update(spritegroup=self.game_object_group)
        # self.camera.center = self.char.rect.center
        # col_rect = pygame.sprite.spritecollideany(self.char, self.game_object_group)
        # self.char.movement_impact(col_rect)
        self.camera.follow_target(self.char.rect)
    
    def handle_event(self):
        return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                self.char.handle_keydown(event.key)
            
            if event.type == pygame.KEYUP:
                self.char.handle_keyup(event.key)
    

    @staticmethod
    def create_game_world(world_no:int, camera:pygame.rect.Rect):
        location = Constant.GAME_WORLD[world_no]
        game_objects_group = CameraGroup(camera=camera)
        with open(os.path.join(*location), 'r') as game_text:
            nx,ny=0,0
            for line in game_text:
                nx=0
                for ch in line.strip():
                    if ch=='0' or ch==" ":
                        nx += 1
                        continue
                    o = Object(str(os.path.join(*Constant.TILEMAP[ch])))
                    o.set_position(nx*Constant.BOX[0], ny*Constant.BOX[1])
                    # o.set_center_pos(nx*Constant.BOX[0]+Constant.BOX[0]//2, ny*Constant.BOX[1]+Constant.BOX[1]//2)
                    game_objects_group.add(o)
                    nx += 1
                ny += 1
            game_objects_group.set_dimension(nx*Constant.BOX[0], ny*Constant.BOX[1])
        
        # return game_world_objects
        return game_objects_group

    @staticmethod
    def create_game_world2(camera:pygame.rect.Rect, location:tuple[str]=Constant.GAME_WORLD[2]):
        all_object:dict[str, CameraGroup] = {}
        with open(os.path.join(*location), 'r') as game_text:
            nx,ny=0,0
            for line in game_text:
                nx=0
                for ch in line.strip():
                    if ch=='0' or ch==" ":
                        nx += 1
                        continue
                    o = Game.REFER[ch](str(os.path.join(*Constant.TILEMAP[ch])))
                    o.set_center_pos(nx*Constant.BOX[0]+Constant.BOX[0]//2, ny*Constant.BOX[1]+Constant.BOX[1]//2)
                    avail_group = all_object.get(ch, None)
                    if avail_group is None:
                        all_object[ch] = CameraGroup(camera=camera)
                    all_object[ch].add(o)
                    nx += 1
                ny += 1
        
        return all_object
                    

                


class CameraGroup(pygame.sprite.Group):
    def __init__(self, *sprites: Any | AbstractGroup, camera:Camera) -> None:
        super().__init__(*sprites)
        self.camera = camera
        self.dimension = [0,0]
    
    def set_dimension(self, x, y):
        self.dimension[0] = x
        self.dimension[1] = y
    
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
    
    def contains_object(self, rect: pygame.Rect):
        return self.rect.contains(rect)
    
    def follow_target(self, target: pygame.Rect):
        # self.rect.center = target.center
        dx, dy = self.rect.centerx - target.centerx, self.rect.centery - target.centery
        if abs(dx) > Constant.CAMERA_FOCUS[0]:
            dx = dx // Constant.CAMERA_SMOOTHER
            dx = dx if abs(dx)<=Constant.CAMERA_SPEED_LIM else ((dx)//abs(dx))*Constant.CAMERA_SPEED_LIM
            self.rect.centerx -= dx
        if abs(dy) > Constant.CAMERA_FOCUS[1]:
            dy = dy // Constant.CAMERA_SMOOTHER
            dy = dy if abs(dy)<=Constant.CAMERA_SPEED_LIM else ((dy)//abs(dy))*Constant.CAMERA_SPEED_LIM
            self.rect.centery -= dy

