import os, sys
import pygame

from chapters.chapter import Chapter
from objects import Player
from settings import AssetLoader, Constant


class Chapter3(Chapter):
    WOLRD = ("asset", "world", "chap3.txt")
    def __init__(self) -> None:
        super().__init__()
        ppath = os.path.join(*Constant.TILEMAP['c'])
        self.characters = [Player(ppath), Player(ppath)]
    
    def initiate_chapter(self, game):
        super().initiate_chapter(game)
        for ch in self.characters:
            ch.load_animations(AssetLoader.PLAYER)
        self.characters.append(self.main_char)
        self.chidx = len(self.characters)-1
        self.bg_objects = self.game.create_game_world(3, self.game.camera, self.WOLRD)
    
    def toggle_main_char(self):
        self.chidx = (self.chidx+1) % len(self.characters)
        self.main_char = self.characters[self.chidx]
    
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.toggle_main_char()
                else:
                    self.main_char.handle_keydown(event.key)
            
            if event.type == pygame.KEYUP:
                self.main_char.handle_keyup(event.key)
    
    def handle_logic(self):
        self.main_char.update(sprites=self.bg_objects.camera_captured_sprites())
        self.camera.follow_target(self.main_char.rect)
    
    def handle_graphics(self):
        self.bg_objects.draw(self.game.screen)
        self.main_char.animate()
        self.main_char.show(self.game.screen, self.camera)
        for ch in self.characters:
            ch.animate()
            ch.show(self.game.screen, self.camera)