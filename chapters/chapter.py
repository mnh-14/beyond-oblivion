from abc import ABC, abstractmethod

class Chapter(ABC):
    def __init__(self) -> None:
        # pass
        from game import Game
        self.game: Game = None
    
    def set_game(self, game):
        self.game = game
        self.main_char = self.game.char
        self.camera = self.game.camera

    @abstractmethod
    def handle_logic(self):
        pass

    @abstractmethod
    def handle_event(self):
        pass

    @abstractmethod
    def handle_graphics(self):
        pass