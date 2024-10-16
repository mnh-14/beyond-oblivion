import os, sys
import pygame

from chapters.chapter import Chapter
from objects import Player, TextBox
from settings import AssetLoader, Constant


class Chapter3(Chapter):
    WOLRD = ("asset", "world", "chap3.txt")
    TEXTING = 't'
    def __init__(self) -> None:
        super().__init__()
        ppath = os.path.join(*Constant.TILEMAP['c'])
        # self.characters = [Player(ppath), Player(ppath)]
        self.texbox = TextBox()
        self.state = ""
    
    def initiate_chapter(self, game):
        super().initiate_chapter(game)
        self.all_objects = self.game.create_game_world2(self.game.camera, self.WOLRD)
        self.characters = [char for char in self.all_objects["c"]]
        self.bg_objects = self.all_objects["t"]
        self.main_char = self.characters[0]
        self.chidx = 0
    
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
                elif event.key == pygame.K_t:
                    self.texbox.set_text("I am Nafis Hussain, Nice to meet you. How are you and who are you ?")
                    if self.state == self.TEXTING:
                        self.state = ""
                        self.texbox.__init__()
                    else:
                        self.state = self.TEXTING
                else:
                    self.main_char.handle_keydown(event.key)
            
            if event.type == pygame.KEYUP:
                self.main_char.handle_keyup(event.key)
    

    def handle_logic(self):
        if self.camera.contains_object(self.main_char.rect):
            self.main_char.update(sprites=self.bg_objects.camera_captured_sprites())

        self.camera.follow_target(self.main_char.rect)

    
    def handle_graphics(self):
        self.bg_objects.draw(self.game.screen)
        self.main_char.animate()
        self.main_char.show(self.game.screen, self.camera)
        if self.state == self.TEXTING:
            self.texbox.show_text(self.game.screen, self.main_char.rect, self.game.camera)
        for ch in self.characters:
            ch.animate()
            ch.show(self.game.screen, self.camera)