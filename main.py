
import pygame
import sys
import random

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480
BLOCK_SIZE = 20
COLORS = {
    "BACKGROUND": (30, 30, 30),
    "SNAKE": (0, 255, 0),
    "APPLE": (255, 0, 0),
    "TEXT": (255, 255, 255),
    "GAME_OVER": (200, 30, 30)
}

DIFFICULTY_LEVELS = [
    ("Leicht", 7),
    ("Normal", 12),
    ("Schwierig", 18)
]

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Schlangenspiel")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont('Arial', 25)
        self.font_medium = pygame.font.SysFont('Arial', 35)
        self.font_large = pygame.font.SysFont('Arial', 50)

    def show_menu(self):
        selected = 0
        while True:
            self.screen.fill(COLORS["BACKGROUND"])
            title = self.font_medium.render("Schwierigkeitsgrad wählen:", True, COLORS["TEXT"])
            self.screen.blit(title, (WINDOW_WIDTH // 6, WINDOW_HEIGHT // 6))
            for idx, (name, _) in enumerate(DIFFICULTY_LEVELS):
                color = COLORS["SNAKE"] if idx == selected else COLORS["TEXT"]
                option = self.font_medium.render(name, True, color)
                self.screen.blit(option, (WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3 + idx * 50))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(DIFFICULTY_LEVELS)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(DIFFICULTY_LEVELS)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return DIFFICULTY_LEVELS[selected][1]

    def draw_score(self, score):
        score_text = self.font_small.render(f"Punktzahl: {score}", True, COLORS["TEXT"])
        self.screen.blit(score_text, (10, 10))

    def spawn_apple(self, snake):
        while True:
            x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
            y = random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)
            if (x, y) not in snake:
                return (x, y)

    def show_game_over(self, score):
        self.screen.fill(COLORS["GAME_OVER"])
        over_text = self.font_large.render("Spiel beendet!", True, COLORS["TEXT"])
        score_text = self.font_medium.render(f"Endpunktzahl: {score}", True, COLORS["TEXT"])
        self.screen.blit(over_text, (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 3))
        self.screen.blit(score_text, (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    def game_loop(self, speed):
        direction = 'RIGHT'
        snake = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
        apple = self.spawn_apple(snake)
        score = 0
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        direction = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                        direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        direction = 'RIGHT'

            x, y = snake[0]
            if direction == 'UP':
                y -= BLOCK_SIZE
            elif direction == 'DOWN':
                y += BLOCK_SIZE
            elif direction == 'LEFT':
                x -= BLOCK_SIZE
            elif direction == 'RIGHT':
                x += BLOCK_SIZE

            new_head = (x, y)

            # Collision detection
            if (
                x < 0 or x >= WINDOW_WIDTH or
                y < 0 or y >= WINDOW_HEIGHT or
                new_head in snake
            ):
                running = False
                continue

            snake.insert(0, new_head)

            # Apple eaten
            if new_head == apple:
                score += 1
                apple = self.spawn_apple(snake)
            else:
                snake.pop()

            # Drawing
            self.screen.fill(COLORS["BACKGROUND"])
            for block in snake:
                pygame.draw.rect(self.screen, COLORS["SNAKE"], (*block, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.screen, COLORS["APPLE"], (*apple, BLOCK_SIZE, BLOCK_SIZE))
            self.draw_score(score)
            pygame.display.flip()
            self.clock.tick(speed)

        self.show_game_over(score)

    def run(self):
        while True:
            speed = self.show_menu()
            self.game_loop(speed)

if __name__ == "__main__":
    SnakeGame().run()
