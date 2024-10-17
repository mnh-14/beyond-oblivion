import os, sys
import pygame

from chapters.chapter import Chapter
from objects import Player, TextBox
from settings import AssetLoader, Constant


class Chapter3(Chapter):
    WOLRD = ("asset", "world", "chap3.txt")
    puzzle_1_finished = False;puzzle_2_finished = False;puzzle_3_finished = False

    riddles = {
        1 : ("I give you option-To choose between two-You cannot choose both but only one-Got any clue?", "XOR"),
        2 : ("When one calls himself-He carries things on,-Being baseless makes him-Forever gone.", "Recursion"),
        3 : ("A number when number++-Cannot be found,-Make sure that every resource-Stays within the bound.", "403")
    }

    TEXTING = 't'
    LOADING = 'l'
    DEFAULT = "df"
    def __init__(self) -> None:
        super().__init__()
        ppath = os.path.join(*Constant.TILEMAP['c'])
        # self.characters = [Player(ppath), Player(ppath)]
        self.texbox = TextBox(3, 5)
        self.texbox.set_text("LOADING..........!")
        self.state = self.LOADING
        self.frames = 0
        self.all_states = ["cs1", "df"]
        self.scene_count = 0
    
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
    
    def loading_logic(self):
        if self.texbox.is_finished: self.frames += 1
        # self.main_char.update(sprites=self.bg_objects)
        for c in self.characters:
            c.update(sprites=self.bg_objects)

        self.camera.follow_target(self.main_char.rect)
        if self.frames > Constant.LOADING_DELAY:
            self.frames = 0
            self.state = "df"
            self.texbox = TextBox()
    
    def loading_scene_event(self, event:pygame.event.Event):
        return
    
    def loading_scene_graphic(self):
        self.game.screen.fill((10,10,10))
        crect = pygame.Rect(1, 1, 1, 1)
        crect.center = self.game.camera.rect.center
        # self.texbox.show_text(self.game.screen, self.game.camera.relative_rect(crect), self.game.camera)
        self.texbox.show_text(self.game.screen, crect, self.game.camera)
        
    def def_logic(self):
        if self.camera.contains_object(self.main_char.rect):
            self.main_char.update(sprites=self.bg_objects.camera_captured_sprites())

        self.camera.follow_target(self.main_char.rect)
    
    def def_event(self, event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.toggle_main_char()
            else:
                self.main_char.handle_keydown(event.key)
        
        if event.type == pygame.KEYUP:
            self.main_char.handle_keyup(event.key)
    

    def def_graphics(self):
        self.bg_objects.draw(self.game.screen)
        self.main_char.animate()
        self.main_char.show(self.game.screen, self.camera)
        if self.puzzle_1_finished == False:
            for i in range(20):
                rectngl = self.camera.relative_rect(pygame.Rect(4080 + 10*i, 570, 1, 75))
                pygame.draw.rect(self.game.screen, (0, 0, 0), rectngl, width=20)
            pygame.draw.rect(self.game.screen, (0, 0, 0), self.camera.relative_rect(pygame.Rect(4080, 570, 192, 1)), width=20)
        if self.state == self.TEXTING:
            self.texbox.show_text(self.game.screen, self.main_char.rect, self.game.camera)
        for ch in self.characters:
            ch.animate()
            ch.show(self.game.screen, self.camera)
        
    
        
    


        
    

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if self.state == self.DEFAULT:
                self.def_event(event)
            elif self.state == self.LOADING:
                self.loading_scene_event(event)

    

    def handle_logic(self):
        if self.state == self.DEFAULT:
            self.def_logic()
        elif self.state == self.LOADING:
            self.loading_logic()


    
    def handle_graphics(self):
        if self.state == self.DEFAULT:
            self.def_graphics()
        elif self.state == self.LOADING:
            self.loading_scene_graphic()
