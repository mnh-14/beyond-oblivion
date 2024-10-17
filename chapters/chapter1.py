import os, sys
import pygame

from chapters.chapter import Chapter
from objects import Player, TextBox
from settings import AssetLoader, Constant


class Chapter1(Chapter):
    WOLRD = ("asset", "world", "chap1.txt")
    CONV = ("asset", "converse", "ch1.json")
    puzzle_1_finished = False;puzzle_2_finished = False;puzzle_3_finished = False

    riddles = {
        1 : ("I give you option-To choose between two-You cannot choose both but only one-Got any clue?", "XOR"),
        2 : ("When one calls himself-He carries things on,-Being baseless makes him-Forever gone.", "Recursion"),
        3 : ("A number when number++-Cannot be found,-Make sure that every resource-Stays within the bound.", "403")
    }

    TEXTING = 't'
    LOADING = 'l'
    DEFAULT = "df"
    TALKING = "tk"
    MOVEMENT = "mv"
    MOVEMENT_AND_TEXT = "mvt"
    LEAVING = "lv"
    def __init__(self) -> None:
        super().__init__()
        ppath = os.path.join(*Constant.TILEMAP['c'])
        # self.characters = [Player(ppath), Player(ppath)]
        self.main_char: Player = None
        self.texbox = TextBox(3, 5)
        self.texbox.set_text("CHAPTER 1: LOADING..........!")
        self.state = self.LOADING
        self.frames = 0
        self.all_states = ["cs1","gp1", "cs2", "gp2", "df"]
        self.scene_count = 0
        self.free_text = 0
        self.curr_convers_line = 0
    
    def initiate_chapter(self, game):
        super().initiate_chapter(game)
        self.all_objects = self.game.create_game_world2(self.game.camera, self.WOLRD)
        self.characters: list[Player] = [char for char in self.all_objects["c"]]
        self.peoples: list[Player] = [char for char in self.all_objects["p"]]
        self.bg_objects = self.all_objects["t"]
        self.main_char = self.characters[0]
        self.enemiea = self.all_objects['e']
        self.finale = self.all_objects['f']
        self.chidx = 0
        self.detect_rect = pygame.Rect(1, 1, Constant.BOX[0]*3, Constant.BOX[1]*1)
        self.search_rect = pygame.Rect(1, 1, Constant.BOX[0]*20, Constant.BOX[1]*1)
        print(os.path.join(*self.CONV))
        self.conversation = AssetLoader.load_conversation(os.path.join(*self.CONV))
        self.char_assign = {
            "mc": self.main_char,
            "e1": self.enemiea.sprites()[0],
            "e2": self.enemiea.sprites()[1]
        }
        self.char_talked_to = []
        self.p_taken = 1
    
    def toggle_main_char(self):
        self.chidx = (self.chidx+1) % len(self.characters)
        self.main_char = self.characters[self.chidx]
    
    def loading_logic(self):
        if self.texbox.is_finished: self.frames += 1
        for c in self.characters:
            c.update(sprites=self.bg_objects)
        for p in self.peoples:
            p.update(sprites=self.bg_objects)

        self.camera.follow_target(self.main_char.rect)
        if self.frames > Constant.LOADING_DELAY:
            self.frames = 0
            self.state = self.MOVEMENT #state switch
            self.texbox = TextBox(1, 5)
    
    def detect_character(self):
        self.search_rect.bottom = self.main_char.rect.bottom
        self.search_rect.centerx = self.main_char.rect.centerx
        self.detect_rect.bottom = self.main_char.rect.bottom
        self.detect_rect.centerx = self.main_char.rect.centerx
        for p in self.peoples:
            if self.search_rect.colliderect(p.rect):
                print("Collision here ")
                if p not in self.char_assign.values():
                    ch = self.conversation['characters'][self.p_taken]
                    print(ch, "detected")
                    self.char_assign[self.conversation['characters'][self.p_taken]] = p
                    self.p_taken += 1
        for p in self.peoples:
            if self.detect_rect.colliderect(p.rect) and p not in self.char_talked_to:
                self.char_talked_to.append(p)
                return True
        for e in self.enemiea:
            if self.detect_rect.colliderect(e.rect) and e not in self.char_talked_to:
                self.char_talked_to.append(e)
                return True
        return False

    
    def loading_scene_event(self, event:pygame.event.Event):
        return
    
    def loading_scene_graphic(self):
        self.game.screen.fill((10,10,10))
        crect = pygame.Rect(1, 1, 1, 1)
        crect.center = self.game.camera.rect.center
        self.texbox.show_text(self.game.screen, crect, self.game.camera)
        
    def def_logic(self):
        if self.camera.contains_object(self.main_char.rect):
            self.main_char.update(sprites=self.bg_objects.camera_captured_sprites())

        self.camera.follow_target(self.main_char.rect)
    
    def def_event(self, event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.toggle_main_char()
            # elif event.key == pygame.K_k:
            #     self.main_char.got_shot()
            else:
                self.main_char.handle_keydown(event.key)
        
        if event.type == pygame.KEYUP:
            self.main_char.handle_keyup(event.key)
    

    def def_graphics(self):
        self.bg_objects.draw(self.game.screen)
        self.main_char.animate()
        self.main_char.show(self.game.screen, self.camera)

        for p in self.peoples:
            if self.game.camera.captured_objects(p.rect):
                p.animate()
                p.show(self.game.screen, self.game.camera)
        for e in self.enemiea:
            if self.game.camera.captured_objects(e.rect):
                e.animate()
                e.show(self.game.screen, self.game.camera)
            
        if self.state == self.TEXTING:
            self.texbox.show_text(self.game.screen, self.main_char.rect, self.game.camera)
        for ch in self.characters:
            ch.animate()
            ch.show(self.game.screen, self.camera)
    


    def movement_logic(self):
        self.def_logic()
        for f in self.finale:
            if self.main_char.rect.colliderect(f.rect):
                self.game.current_phase = "ch-2"
                return
        if self.detect_character():
            self.state = self.TALKING
            self.texbox.set_text(self.conversation["converse"][self.curr_convers_line][1])
            self.main_char.stop_movement()
        if self.free_text:
            if self.texbox.is_finished:
                self.curr_convers_line += 1
                if len(self.conversation["converse"])==self.curr_convers_line:
                    self.state = self.LEAVING
                else:
                    self.texbox.set_text(self.conversation["converse"][self.curr_convers_line][1])

        
    def movement_event(self, event):
        self.def_event(event=event)

    def movement_graphics(self):
        self.def_graphics()
        if self.free_text:
            tar = self.conversation["converse"][self.curr_convers_line][0]
            self.texbox.show_text(self.game.screen, self.char_assign[tar].rect, self.game.camera)
        
        
    def talking_logic(self):
        self.def_logic()
        if self.conversation["converse"][self.curr_convers_line][2] == 'keep':
            self.state = self.MOVEMENT
            self.free_text = True
            return
        # self.def_logic()
    def toggle_to_next_converse(self, force = False):
        if self.texbox.is_finished or force:
            if self.conversation["converse"][self.curr_convers_line][2] == 'finish':
                self.state = self.MOVEMENT
                self.curr_convers_line += 1
                return
            self.curr_convers_line += 1
            self.texbox.set_text(self.conversation["converse"][self.curr_convers_line][1])

    def talking_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.toggle_to_next_converse()
            if event.key == pygame.K_LSHIFT:
                self.toggle_to_next_converse(True)
                
                

    def talking_graphic(self):
        self.def_graphics()
        ch = self.conversation["converse"][self.curr_convers_line][0]
        char = self.char_assign[ch]
        self.texbox.show_text(self.game.screen, char.rect, self.game.camera)
    
        
    

    

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if self.state == self.LOADING:
                self.loading_scene_event(event)
            elif self.state == self.MOVEMENT:
                self.movement_event(event)
            elif self.state == self.TALKING:
                self.talking_event(event)
            else:
                self.def_event(event=event)

    

    def handle_logic(self):
        if self.state == self.LOADING:
            self.loading_logic()
        elif self.state == self.MOVEMENT:
            self.movement_logic()
        elif self.state == self.TALKING:
            self.talking_logic()
        else:
            self.def_logic()


    
    def handle_graphics(self):
        if self.state == self.LOADING:
            self.loading_scene_graphic()
        elif self.state == self.MOVEMENT:
            self.movement_graphics()
        elif self.state == self.TALKING:
            self.talking_graphic()
        else:
            self.def_graphics()
