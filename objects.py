
import pygame

from settings import Constant


class Object:
    def __init__(self, img_path:str) -> None:
        self.img = pygame.image.load(img_path)
        self.rect = self.img.get_rect()
        self.rect.center = (0,0)
        self.velocity = [0,0]
    
    def show(self, screen:pygame.Surface, camera:pygame.Rect):
        rel_rect = self.rect.copy()
        rel_rect.x = self.rect.x - camera.x
        rel_rect.y = self.rect.y - camera.y
        screen.blit(self.img, rel_rect)
    
    def set_position(self, x:int, y:int):
        self.rect.x=x
        self.rect.y=y
    
    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y -= self.velocity[1]
    

class Player(Object):
    def __init__(self, img_path: str) -> None:
        super().__init__(img_path)
        self.set_position(0, 0)
    
    def handle_keydown(self, key):
        if key == pygame.K_LEFT:
            self.velocity[0] -= Constant.CHAR_SPEED
        if key == pygame.K_UP:
            self.velocity[1] += Constant.CHAR_SPEED
        if key == pygame.K_DOWN:
            self.velocity[1] -= Constant.CHAR_SPEED
        if key == pygame.K_RIGHT:
            self.velocity[0] += Constant.CHAR_SPEED
    
    def handle_keyup(self, key):
        if key == pygame.K_LEFT:
            self.velocity[0] = 0
        if key == pygame.K_UP:
            self.velocity[1] = 0
        if key == pygame.K_DOWN:
            self.velocity[1] = 0
        if key == pygame.K_RIGHT:
            self.velocity[0] = 0
