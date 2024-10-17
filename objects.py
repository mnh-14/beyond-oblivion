from __future__ import annotations
import random
from typing import Any
import pygame

# from game import Camera
from settings import Constant, AssetLoader

asset_loader = AssetLoader()


class Object(pygame.sprite.Sprite):
    RESTRICT_IMPACT = 1
    BOUNCE_IMPACT = 2
    def __init__(self, img_path:str, gravity=False, passthrough=False) -> None:
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        # self.rect = pygame.Rect(0, 0, Constant.BOX[0], Constant.BOX[1])
        self.pre_rect = self.rect.copy()
        self.anim_direction = [1, 1]
        self.rect.center = (0,0)
        self.velocity = [0,0]
        self.resistance = [0, 0]
        self.acceleration = [0, 0]
        self.acceleration[1] = -1 * Constant.DEFAULT_GRAVITY if gravity else 0
        self.passthrough = passthrough
        self.direction = 1
    
    def get_image_rect(self):
        rect = self.image.get_rect()
        rect.bottom = self.rect.bottom
        if self.anim_direction[0] > 0:
            rect.left = self.rect.left
        else:
            rect.right = self.rect.right
        return rect

    def show(self, screen:pygame.Surface, camera):
        rect = self.get_image_rect()
        rel_rect = camera.relative_rect(rect)
        screen.blit(self.image, rel_rect)
    
    def load_animations(self, animation_cat):
        self.animations, self.delays = asset_loader.load_asset(animation_cat)
        self.frame_count = 0
        self.curr_frame = 1
        self.anim_frame = 0
        self.anim_state = ""

    def animation_state_switch(self):
        pass
    
    def animate(self):
        pass

    
    def set_position(self, x:int, y:int):
        self.rect.x=x
        self.rect.y=y

    def set_center_pos(self, x:int, y:int):
        self.rect.centerx = x
        self.rect.centery = y
    
    def move(self):
        # self.pre_rect = self.rect.copy()
        self.rect.x += int(self.velocity[0])
        self.rect.y -= int(self.velocity[1])
    
    def handle_xaxis_collision(self, obj:Object=None, impact_type=RESTRICT_IMPACT):
        if self.passthrough:
            return
        if obj is None:
            return
        dx = obj.rect.centerx - self.rect.centerx
        if impact_type==Object.RESTRICT_IMPACT:
            self.velocity[0] = 0
            if dx < 0:
                self.rect.left = obj.rect.right
            if dx > 0:
                self.rect.right = obj.rect.left
    
    def handle_yaxis_collision(self, obj:Object=None, impact_type=RESTRICT_IMPACT):
        if self.passthrough:
            return
        if obj is None:
            return
        dy = obj.rect.centery - self.rect.centery
        if impact_type==Object.RESTRICT_IMPACT:
            self.velocity[1] = 0
            # print("Changed v", self.velocity)
            if dy < 0:
                self.rect.top = obj.rect.bottom
            if dy > 0:
                self.rect.bottom = obj.rect.top
        
    
    def movement_impact(self, obj:Object=None, impact_type=RESTRICT_IMPACT):
        if self.passthrough:
            return
        if obj is None:
            return
        rect = obj.rect
        dx = rect.centerx - self.rect.centerx
        dy = rect.centery - self.rect.centery
        if impact_type==Object.RESTRICT_IMPACT:
            print("======================================================")
            print("Self rect:", self.rect.topleft, self.rect.bottomright)
            print("Coll rect", rect.topleft, rect.bottomright)
            if abs(dx) < abs(dy):
                print("Y collision:")
                self.velocity[1] = 0
                if dy < 0:
                    self.rect.top = rect.bottom
                if dy > 0:
                    self.rect.bottom = rect.top
            if abs(dx) > abs(dy):
                print("X collision:")
                self.velocity[0] = 0
                if dx < 0:
                    self.rect.left = rect.right
                if dx > 0:
                    self.rect.right = rect.left
            print("Self rect:", self.rect.topleft, self.rect.bottomright)
            print("Coll rect", rect.topleft, rect.bottomright)
            print("======================================================")

    def controll_velocity(self):
        if int(self.velocity[0]) == 0 and self.acceleration[0] == 0:
            self.resistance[0] = 0
        self.velocity[0] += self.acceleration[0]-self.resistance[0]
        self.velocity[1] += self.acceleration[1]-self.resistance[1]

        if abs(self.velocity[0]) > Constant.VELOCITY_X_LIM:
            self.velocity[0] = (self.velocity[0] / abs(self.velocity[0])) * Constant.VELOCITY_X_LIM
        if abs(self.velocity[1]) > Constant.VELOCITY_Y_LIM:
            self.velocity[1] = (self.velocity[1] / abs(self.velocity[1])) * Constant.VELOCITY_Y_LIM


    
    def update(self, *args: Any, **kwargs: Any) -> None:
        # if self.velocity[0] or self.velocity[1]:
            # self.pre_rect = self.rect.copy()
        self.controll_velocity()

        self.rect.y -= int(self.velocity[1])
        col_sprite = pygame.sprite.spritecollideany(self, kwargs["sprites"])
        self.handle_yaxis_collision(col_sprite)

        self.rect.x += int(self.velocity[0])
        col_sprite = pygame.sprite.spritecollideany(self, kwargs["sprites"])
        self.handle_xaxis_collision(col_sprite)
        
        # self.rect.y -= self.velocity[1]
        # col_sprite = pygame.sprite.spritecollideany(self, kwargs["sprites"])
        # self.movement_impact(col_sprite)

    
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
    STANDING = 's'
    RUNNING = 'r'
    JUMP = 'j'
    FIGHT = 'f'
    DYING = 'd'
    HURT = 'h'
    
    def __init__(self, img_path: str) -> None:
        super().__init__(img_path, True)
        self.rect = pygame.Rect(0, 0, Constant.BOX[0], int(Constant.BOX[1] * 1.75))
        self.set_position(100, -100)
        self.load_animations(AssetLoader.PLAYER)
        self.anim_direction = [1, 1]
        self.anim_state = self.STANDING
        self.talking = False
        self.dead = False
        self.health = Constant.CHAR_BASE_HEALTH
        self.detection_rect = pygame.Rect(0, 0, Constant.BOX[0]*15, Constant.BOX[1]*2)
        self.autoplayer = AutoPlayer(self)

    
    def handle_keydown(self, key, **kwargs):
        if self.health <= 0:
            return
        if key == pygame.K_LEFT:
            self.move_left()
            print(self.rect.center)
        if key == pygame.K_RIGHT:
            self.move_right()
            print(self.rect.center)
        if key == pygame.K_SPACE:
            self.make_jump()
            jump=pygame.mixer.Sound('sounds/player-jumping-in-a-video-game-2043.wav')
            jump.play()
            print(self.rect.center)
        if key == pygame.K_x:
            fight=pygame.mixer.Sound('sounds/Hitting.wav')
            fight.play()
            return self.do_fight()
            
    
    def handle_keyup(self, key):
        if self.health <= 0:
            return
        if key == pygame.K_LEFT:
            self.move_left(False)
        if key == pygame.K_RIGHT:
            self.move_right(False)
    
    def do_fight(self):
        self.velocity[0]=0
        self.anim_state=self.FIGHT
        self._frame_reset()
        return Bullet(self.anim_direction[0], self.rect.center)
    
    def make_jump(self):
        if int(self.velocity[1])==0:
            self.velocity[1] = Constant.JUMP_VELOCITY
    
    def got_shot(self, damage:int=Constant.BASE_BULLETE_DAMAGE):
        if self.anim_state == self.DYING:
            return
        # self.dead = True
        # self.alive = False
        if self.health > 0:
            self.health -= damage

        self._frame_reset()
        self.anim_state = self.DYING
        self.acceleration[0] = 0
    

    def stop_movement(self):
        self.acceleration[0] = 0

            
    

    def _frame_reset(self):
        self.frame_count = 0
        # self.curr_frame = 0
        self.anim_frame = 0

    def animation_state_switch(self):
        if self.dead:
            return
        if self.health <= 0:
            if self.anim_frame==len(self.animations[self.anim_state]):
                self.dead = True
            return
        if int(self.velocity[0]) == 0 and self.anim_state==self.FIGHT:
            if self.anim_frame==len(self.animations[self.anim_state]):
                self.anim_state = self.STANDING
                self._frame_reset()
                    
        elif (int(self.velocity[0]) == 0 and int(self.acceleration[0]==0)) and self.anim_state!=self.STANDING:
            self.anim_state = self.STANDING
            self._frame_reset()
        
        elif int(self.velocity[0]) > 0 or int(self.acceleration[0]) > 0:
            if self.anim_state == self.RUNNING:
                self.anim_direction[0] = 1
            else:
                self.anim_state = self.RUNNING
                self._frame_reset()
        
        elif int(self.velocity[0]) < 0 or int(self.acceleration[0]) < 0:
            if self.anim_state == self.RUNNING:
                self.anim_direction[0] = -1
            else:
                self.anim_state = self.RUNNING
                self._frame_reset()
    

    def animate(self):
        self.animation_state_switch()
        # self.frame_count += 1
        if self.dead:
            return
        if (self.frame_count) % self.delays[self.anim_state] == 0:
            self.anim_frame = (self.anim_frame % len(self.animations[self.anim_state])) + 1
            self.frame_count = 0
        self.frame_count += 1
        
        self.image = self.animations[self.anim_state][self.anim_frame-1]
        if self.anim_direction[0] < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        # x = self.rect.centerx
        # b = self.rect.bottom
    
    def set_target(self, target:Player):
        self.autoplayer.set_target(target)
    
    def autoplay(self):
        return self.autoplayer.autoplay()


class AutoPlayer:
    def __init__(self, player:Player) -> None:
        self.target:Player = None
        self.player = player
        self.movement_delay = (100, 850)
        self.shooting_delay = 45
        self.jumping_delay = 45
        self.shoot_frame = 0
        self.move_frame = 0
        self.jump_frame=0
        self.dir = 1
    
    def set_target(self, target:Player):
        if self.target is None:
            self.target = target
    
    def autoplay(self):
        if self.target is None:
            self.roaming()
        else:
            return self.follow_target()
        return None
    

    def follow_target(self):
        self.shoot_frame += 1
        self.move_frame += 1
        self.jump_frame += 1
        dx = self.player.rect.centerx - self.target.rect.centerx
        if dx > 0:
            self.player.move_left()
        if self.move_frame % self.movement_delay[1] == 0:
            if dx < 0:
                self.player.move_right(False)
            else:
                self.player.move_left(False)
        elif self.move_frame % self.movement_delay[0] == 0:
            if self.player.acceleration[0] == 0:
                if self.dir > 0:
                    self.player.move_left()
                    self.dir = -1
                else:
                    self.player.move_right()
                    self.dir = 1
        if self.shoot_frame % self.shooting_delay:
            return self.player.do_fight()
        
            


    def roaming_arround(self):
        self.shoot_frame += 1
        self.move_frame += 1
        self.jump_frame += 1
        if self.move_frame % self.movement_delay[1] == 0:
            print("Roaming around")
            self.player.stop_movement()
        elif self.move_frame % self.movement_delay[0] == 0:
            if self.player.acceleration[0] == 0:
                if self.dir > 0:
                    self.player.move_left()
                    self.dir = -1
                else:
                    self.player.move_right()
                    self.dir = 1
    def roaming(self):
        c = random.choice([x for x in range(45)])
        if c == 25:
            if self.dir > 0:
                self.player.move_left()
                self.dir = -1
            else:
                self.player.move_right()
                self.dir = 1
        elif c==40:
            self.player.stop_movement()





class Enemy(Player):
    def __init__(self, img_path: str) -> None:
        super().__init__(img_path)
        self.load_animations(AssetLoader.ENEMY)


class People(Player):
    def __init__(self, img_path: str) -> None:
        super().__init__(img_path)
        self.load_animations(AssetLoader.PEOPLE)

            

            

class TextBox:
    def __init__(self, font_size_mult=1, delay=1) -> None:
        pygame.init()
        self.font = pygame.font.Font(None, Constant.FONT_SIZE*font_size_mult)
        self.text = ""
        self.lines = []
        self.current_line = ""
        self.curr_line_idx = 0
        self.line_rects: list[pygame.Rect] = []
        self.line_surface: list[pygame.Surface] = []
        self.frame = 0
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.rr: pygame.Rect = None
        self.is_finished = False
        self.delay_count = 0
        self.delay = delay
        self.font_size_mul = font_size_mult
    
    def set_text(self, txt:str):
        self.__init__(self.font_size_mul, self.delay)
        self.text = txt.strip()
        words = self.text.split(" ")
        horizontal_count = int((len(words) * Constant.TEXT_BOX_DIM_R[0]) // Constant.TEXT_BOX_DIM_R[2]) + 1
        vertical_count = int((len(words) * Constant.TEXT_BOX_DIM_R[1]) // Constant.TEXT_BOX_DIM_R[2]) * Constant.TEXT_BOX_DIM_CONST[1]
        lws = []
        for w in words:
            lws.append(w)
            if len(lws) == horizontal_count:
                self.lines.append(" ".join(lws))
                lws = []
        if len(lws) != 0:
            self.lines.append(" ".join(lws))
            lws = []
        self.current_line = ""
        for l in self.lines:
            s:pygame.Surface = self.font.render(l, True, Constant.TEXT_FONT_COLOR)
            self.line_surface.append(s)
            self.line_rects.append(s.get_rect())
        self.rect.width = max([r.width for r in self.line_rects])
        self.rect.height = self.line_rects[0].height * len(self.line_rects)
        self.is_finished = False

    def _set_position(self, target:pygame.Rect):
        self.rect.centerx = target.centerx
        dy = target.height//2 + self.rect.height // 2 + Constant.TEXT_BOX_OFFSET
        self.rect.centery = target.centery - dy
        self.rr = self.rect.copy()
        self.rr.inflate_ip(*Constant.TEXT_BOX_INFLATION)
        self.rr.center = self.rect.center

    
    def show_text(self, screen:pygame.Surface, target:pygame.Rect, camera):
        calc = self.delay_count % self.delay == 0
        self.delay_count = (self.delay_count+1) % self.delay
        self._set_position(target)
        rad = Constant.TEXT_BOX_RADIUS
        pygame.draw.rect(screen, (255, 255, 255), camera.relative_rect(self.rr), width=0, border_radius=rad)
        pygame.draw.rect(screen, (0,0,0), camera.relative_rect(self.rr), width=3, border_radius=rad)
        
        tl = self.rect.topleft
        idx = 0
        for idx in range(len(self.line_surface)):
            self.line_rects[idx].topleft = tl
            if idx == self.curr_line_idx:
                break
            screen.blit(self.line_surface[idx], camera.relative_rect(self.line_rects[idx]))
            tl = self.line_rects[idx].bottomleft

        if self.is_finished:
            return
        if calc:
            if self.frame >= len(self.lines[self.curr_line_idx]):
                self.frame = 0
                self.curr_line_idx += 1
                self.current_line = ""
            
            if self.curr_line_idx >= len(self.lines):
                self.is_finished = True
                return
            self.current_line += self.lines[self.curr_line_idx][self.frame]
        
        img = self.font.render(self.current_line, True, Constant.TEXT_FONT_COLOR)
        img_rect = img.get_rect()
        img_rect.topleft = tl
        screen.blit(img, camera.relative_rect(img_rect))
        if calc:
            self.frame += 1


class Bullet:
    def __init__(self, dir, center, damage=Constant.BASE_BULLETE_DAMAGE, speed=Constant.BASE_BULLETE_SPEED) -> None:
        self.circle_rect = pygame.Rect(0,0, Constant.BULLET_2R, Constant.BULLET_2R)
        self.circle_rect.center = center
        self.circle_rect.centery -= Constant.BOX[1]//2
        self.h_speed = speed
        self.damage = damage
        self.dir = dir
        self.delay = 18
        self.frame = 1
    
    def show_bullet(self,screen:pygame.Surface, camera):
        if self.frame % self.delay == 0:
            relrect = camera.relative_rect(self.circle_rect)
            pygame.draw.circle(screen, (0,0,0), relrect.center, Constant.BULLET_2R//2)
    
    def run_bullete(self):
        if self.frame % self.delay == 0:
            self.circle_rect.centerx += self.dir * self.h_speed
        else:
            self.frame += 1
    
    def shot_character(self, chars:list[Player]):
        if self.frame % self.delay:
            return
        for c in chars:
            if c.rect.colliderect(self.circle_rect):
                c.got_shot(self.damage)
                del self
                return
        
        
        
            


