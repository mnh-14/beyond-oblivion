
class Constant:
    BOX = (36,36)
    SCREEN_RATIO = (32, 20)
    SCREEN_RES = (BOX[0]*SCREEN_RATIO[0]*1, BOX[1]*SCREEN_RATIO[1]*1)
    GAME_NAME = "Beyond Oblivion"
    FPS = 90
    CHAR_SPEED = 5
    VELOCITY_X_LIM = 10
    JUMP_VELOCITY = 20
    DEFAULT_ACCELERATION = 4
    RESISTANCE_DECELERATION = 1
    GAME_WORLD = {
        1: ('asset', 'world', 'world1.txt')
    }
    DEFAULT_GRAVITY = 1
    TILEMAP = {
        't': ('asset', 'tiles', 'tile_0001.png'),
        'c': ('asset', 'character', 'tile_0006.png'),
    }