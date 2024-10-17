import os
import pygame
import json

class Constant:
    BOX = (36,36)
    SCREEN_RATIO = (32, 20)
    SCREEN_RES = (BOX[0]*SCREEN_RATIO[0]*1, BOX[1]*SCREEN_RATIO[1]*1)
    CAMERA_FOCUS = (BOX[0]*SCREEN_RATIO[0] // 6, BOX[1]*SCREEN_RATIO[1] // 5) 
    CAMERA_SMOOTHER = CAMERA_FOCUS[0]//3
    CAMERA_SPEED_LIM = 10
    GAME_NAME = "Beyond Oblivion"
    FPS = 60
    CHAR_SPEED = 5
    VELOCITY_X_LIM = 6
    JUMP_VELOCITY = 30
    VELOCITY_Y_LIM = 25
    DEFAULT_ACCELERATION = 3
    RESISTANCE_DECELERATION = 0.4
    DEFAULT_GRAVITY = 1
    FONT_SIZE = 20
    TEXT_DELAY = 3
    TEXT_BOX_DIM_R = (5, 3, 15) # 5 words and 3 lines ratio
    TEXT_BOX_DIM_CONST = (10, 6)
    TEXT_FONT_COLOR = (0,0,0)
    TEXT_BOX_OFFSET = 15
    TEXT_BOX_INFLATION = (15,15)
    TEXT_BOX_RADIUS = 6
    LOADING_DELAY = 45
    GAME_WORLD = {
        1: ('asset', 'world', 'world1.txt'),
        2: ('asset', 'world', 'chap3.txt')
    }
    TILEMAP = {
        't': ('asset', 'tiles', 'tile_0001.png'),
        'c': ('asset', 'character', 'tile_0006.png'),
        'p': ('asset', 'character', 'tile_0006.png'),
        'e': ('asset', 'character', 'tile_0006.png')
    }




class SpriteCollection:
    PLAYER = {
        "source": ('asset', 'character'),
        "resize": 1,
        "frames": {
            "s": 6,
            "f": 5,
            "r": 10
        },
        "delay": {
            "s": 4,
            "f": 4,            
            "r": 2,
        }
    }


class AssetLoader:
    PLAYER = 'player'
    ENEMY = 'enemy'
    PEOPLE = 'people'
    SOURCE = 'source'
    RESIZE = 'resize'
    FRAMES = 'frames'
    DELAY = 'delay'
    def __init__(self, filepath:str="asset_info.json") -> None:
        with open(filepath, "r") as asset:
            self.asset_info = json.load(asset)
    
    def load_asset(self, asset_cat:str):
        images = {}
        delays = {}
        data: dict = self.asset_info[asset_cat]
        for key in data[self.FRAMES].keys():
            images[key] = list()
            delays[key] = data[self.DELAY][key]
            for i in range(1, data[self.FRAMES][key]+1):
                img = pygame.image.load(os.path.join(*data[self.SOURCE], key, str(i)+'.png')).convert_alpha()
                # img.fill((200,50,50), special_flags=pygame.BLEND_RGB_SUB)
                images[key].append(img)
        
        return images, delays
