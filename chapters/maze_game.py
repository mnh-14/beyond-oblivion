import pygame
import random
from settings import Constant

# Constants
SCREEN_WIDTH = 1150
SCREEN_HEIGHT = 720  # Increased height for timer display
CELL_SIZE = 20
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAZE_HEIGHT = (SCREEN_HEIGHT - 50) // CELL_SIZE  # Adjusted height for timer display
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (192, 192, 192)

class MazeGame:
    def __init__(self, countdown_time=120):
        self.constants = Constant()
        self.screen = pygame.display.set_mode(self.constants.SCREEN_RES)  # Use screen resolution from Constant
        print(self.constants.SCREEN_RES)
        pygame.display.set_caption(self.constants.GAME_NAME)  # Use game name from Constant
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, self.constants.FONT_SIZE)  # Use font size from Constant
        self.countdown_time = countdown_time  # Retain the countdown time logic
        self.isSolved = False

        # Maze and player
        self.maze = self.create_maze()
        self.player = self.Player()
        self.countdown_time = countdown_time

        # Timer and scoring
        self.timer = self.Timer(countdown_time)
        self.running = True
        self.won = False
        self.score = 0

    # Maze creation
    def create_maze(self):
        maze = [[0] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
    
    # Increase the number of obstacles to make the maze denser
        num_obstacles = int(MAZE_WIDTH * MAZE_HEIGHT * 0.4)  # 40% of the grid filled with obstacles
    
    # Randomly add obstacles
        for _ in range(num_obstacles):
            x = random.randint(0, MAZE_WIDTH - 1)
            y = random.randint(0, MAZE_HEIGHT - 1)
            maze[y][x] = 1
    
    # Ensure start and end points are open
        maze[0][0] = 0  # Start point
        maze[MAZE_HEIGHT - 1][MAZE_WIDTH - 1] = 2  # End point
        
        return maze

    # Draw maze
    def draw_maze(self):
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if self.maze[y][x] == 1:
                    pygame.draw.rect(self.screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.maze[y][x] == 2:
                    pygame.draw.rect(self.screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Run the game loop
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_player_movement(event)

            #self.screen.fill(WHITE)
            self.draw_maze()
            self.player.draw(self.screen)
            self.timer.draw(self.screen)

            # Check win condition
            if self.maze[self.player.y][self.player.x] == 2:
                self.won = True
                self.score = self.timer.get_remaining_time() * 10  # Score based on remaining time
                self.running = False

            # Check if time is up
            if self.timer.is_time_up():
                self.running = False

            pygame.display.flip()
            self.clock.tick(30)

        # End screen
        self.display_end_screen()

    # Display end screen with score
    def display_end_screen(self):
       # self.screen.fill(WHITE)
        if self.won and not self.isSolved:
            self.isSolved = True  # Mark puzzle as solved to prevent replaying the sound
            end_text = f''
            sound = pygame.mixer.Sound('sounds/puzzleSolve.wav')
            sound.play()  # Play the sound only once

        else:
            end_text = ''
            sound2 = pygame.mixer.Sound('sounds/player-losing-or-failing-2042.wav')
        time_text = self.font.render(end_text, True, BLACK)
        self.screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 - time_text.get_height() // 2))
        # pygame.display.flip()
        # pygame.time.wait(3000)
        #pygame.quit()
        return

    # Handle player movement
    def handle_player_movement(self, event):
        if event.key == pygame.K_UP:
            self.player.move(0, -1, self.maze)
        elif event.key == pygame.K_DOWN:
            self.player.move(0, 1, self.maze)
        elif event.key == pygame.K_LEFT:
            self.player.move(-1, 0, self.maze)
        elif event.key == pygame.K_RIGHT:
            self.player.move(1, 0, self.maze)

    # Nested Player class
    class Player:
        def __init__(self):
            self.x = 0
            self.y = 0

        def move(self, dx, dy, maze):
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[new_y][new_x] != 1:
                self.x = new_x
                self.y = new_y

        def draw(self, screen):
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Nested Timer class
    class Timer:
        def __init__(self, countdown_time):
            self.font = pygame.font.SysFont(None, 36)
            self.start_time = pygame.time.get_ticks()
            self.countdown_time = countdown_time  # Time in seconds

        def get_remaining_time(self):
            elapsed_time = pygame.time.get_ticks() - self.start_time
            remaining_time = self.countdown_time - elapsed_time // 1000
            if remaining_time < 0:
                remaining_time = 0
            return remaining_time

        def get_time_display(self):
            remaining_time = self.get_remaining_time()
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            return f"Time: {minutes:02}:{seconds:02}"

        def draw(self, screen):
            time_text = self.font.render(self.get_time_display(), True, BLACK)
            screen.blit(time_text, (10, 600))

        def is_time_up(self):
            return self.get_remaining_time() <= 0

# To integrate into another game, you can instantiate MazeGame and call its run() method
# if __name__ == "__main__":
#     maze_game = MazeGame(countdown_time=120)  # 2 minutes countdown
#     maze_game.run()


