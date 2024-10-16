import os

from chapters.chapter import Chapter
from objects import Player
from settings import Constant


class Chapter3(Chapter):
    def __init__(self) -> None:
        super().__init__()
        ppath = Player(os.path.join(*Constant.TILEMAP['c']))
        self.characters = [Player(ppath), Player(ppath)]
    
    def initiate_chapter(self, game):
        super().initiate_chapter(game)
        self.characters.append(self.main_char)
        self.chidx = len(self.characters)-1