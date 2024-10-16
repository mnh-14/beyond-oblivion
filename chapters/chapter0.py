import sys
import pygame
from chapters.chapter import Chapter

class Chapter0(Chapter):
    def __init__(self) -> None:
        super().__init__()
    
    def handle_logic(self):
        self.main_char.update(sprites=self.game.game_object_group.camera_captured_sprites())
        self.camera.follow_target(self.main_char.rect)
    
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                self.main_char.handle_keydown(event.key)
            
            if event.type == pygame.KEYUP:
                self.main_char.handle_keyup(event.key)

    def handle_graphics(self):
        self.game.game_object_group.draw(self.game.screen)
        self.main_char.animate()
        self.main_char.show(self.game.screen, self.camera)