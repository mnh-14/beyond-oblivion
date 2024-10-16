from abc import ABC, abstractmethod

class Chapter(ABC):
    def __init__(self) -> None:
        # pass
        from game import Game
        self.game: Game = None
        self.finished = False
        self.current_phase = ""
        self.phases = {}
    
    def initiate_chapter(self, game):
        self.game = game
        self.main_char = self.game.char
        self.camera = self.game.camera
    
    def is_finished(self):
        return self.finished

    @abstractmethod
    def handle_logic(self):
        pass

    @abstractmethod
    def handle_event(self):
        pass

    @abstractmethod
    def handle_graphics(self):
        pass