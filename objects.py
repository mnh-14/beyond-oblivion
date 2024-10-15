from __future__ import annotations
from enum import Flag
import sys
from typing import Any
import pygame

# from game import Camera
from settings import Constant


class Object(pygame.sprite.Sprite):
    RESTRICT_IMPACT = 1
    BOUNCE_IMPACT = 2
    def __init__(self, img_path:str, gravity=False, passthrough=False) -> None:
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.pre_rect = self.rect.copy()
        self.rect.center = (0,0)
        self.velocity = [0,0]
        self.resistance = [0, 0]
        self.acceleration = [0, 0]
        self.acceleration[1] = -1 * Constant.DEFAULT_GRAVITY if gravity else 0
        self.passthrough = passthrough
    
    def show(self, screen:pygame.Surface, camera):
        rel_rect = camera.relative_rect(self.rect)
        screen.blit(self.image, rel_rect)
    
    def set_position(self, x:int, y:int):
        self.rect.x=x
        self.rect.y=y
    
    def move(self):
        self.pre_rect = self.rect.copy()
        self.rect.x += self.velocity[0]
        self.rect.y -= self.velocity[1]
    
    def movement_impact(self, obj:Object=None, impact_type=RESTRICT_IMPACT):
        if self.passthrough:
            return
        if obj is None:
            return
        rect = obj.rect
        dx = rect.centerx - self.pre_rect.centerx
        dy = rect.centery - self.pre_rect.centery
        if impact_type==Object.RESTRICT_IMPACT:
            if abs(dx) < abs(dy):
                self.velocity[1] = 0
                if dy > 0:
                    self.rect.bottom = rect.top
                elif dy < 0:
                    self.rect.top = rect.bottom
            elif abs(dx) > abs(dy):
                self.velocity[0] = 0
                if dx > 0:
                    self.rect.right = rect.left
                elif dx < 0:
                    self.rect.left = rect.right

    def controll_velocity(self):
        if self.velocity[0] == 0 and self.acceleration[0] == 0:
            self.resistance[0] = 0
        self.velocity[0] += int(self.acceleration[0]-self.resistance[0])
        self.velocity[1] += int(self.acceleration[1]-self.resistance[1])

        if abs(self.velocity[0]) > Constant.VELOCITY_X_LIM:
            self.velocity[0] = (self.velocity[0] / abs(self.velocity[0])) * Constant.VELOCITY_X_LIM


    
    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.velocity[0] or self.velocity[1]:
            self.pre_rect = self.rect.copy()
        self.rect.x += self.velocity[0]
        col_sprite = pygame.sprite.spritecollideany(self, kwargs["sprites"])
        self.movement_impact(col_sprite)
        self.rect.y -= self.velocity[1]
        col_sprite = pygame.sprite.spritecollideany(self, kwargs["sprites"])
        self.movement_impact(col_sprite)
        
        self.controll_velocity()
    
    def move_left(self, movement=True):
        if movement:
            self.acceleration[0] = -1 * Constant.DEFAULT_ACCELERATION
            self.resistance[0] = -1 * Constant.RESISTANCE_DECELERATION
        else:
            self.acceleration[0] = 0
    
    def move_right(self, movement=True):
        if movement:
            self.acceleration[0] = Constant.DEFAULT_ACCELERATION
            self.resistance[0] = Constant.RESISTANCE_DECELERATION
        else:
            self.acceleration[0] = 0
        

    

class Player(Object):
    
    def __init__(self, img_path: str) -> None:
        super().__init__(img_path, True)
        self.set_position(100, -100)
    
    def handle_keydown(self, key):
        if key == pygame.K_LEFT:
            # self.velocity[0] -= Constant.CHAR_SPEED
            self.move_left()
        # if key == pygame.K_UP:
        #     self.velocity[1] += Constant.CHAR_SPEED
        # if key == pygame.K_DOWN:
        #     self.velocity[1] -= Constant.CHAR_SPEED
        if key == pygame.K_RIGHT:
            # self.velocity[0] += Constant.CHAR_SPEED
            self.move_right()
        if key == pygame.K_SPACE:
            self.velocity[1] = Constant.JUMP_VELOCITY
    
    def handle_keyup(self, key):
        if key == pygame.K_LEFT:
            # self.velocity[0] = 0
            self.move_left(False)
        # if key == pygame.K_UP:
        #     self.velocity[1] = 0
        # if key == pygame.K_DOWN:
        #     self.velocity[1] = 0
        if key == pygame.K_RIGHT:
            self.move_right(False)
            
