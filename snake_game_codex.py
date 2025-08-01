import pygame
import random
from collections import deque
from enum import Enum
import sys

# ————————————————————————————————————————————————————————
# Constants / Config
WIDTH, HEIGHT = 600, 600
CELL = 20
COLS, ROWS = WIDTH // CELL, HEIGHT // CELL
FPS_START = 10
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

class Dir(Enum):
    UP    = (0, -1)
    DOWN  = (0,  1)
    LEFT  = (-1, 0)
    RIGHT = (1,  0)

    @property
    def dx(self): return self.value[0]
    @property
    def dy(self): return self.value[1]

    def is_opposite(self, other):
        return self.dx == -other.dx and self.dy == -other.dy

class Food:
    def __init__(self, occupied):
        self.position = None
        self.spawn(occupied)

    def spawn(self, occupied):
        while True:
            pos = (random.randrange(COLS), random.randrange(ROWS))
            if pos not in occupied:
                self.position = pos
                return

    def draw(self, surf):
        r = pygame.Rect(self.position[0] * CELL, self.position[1] * CELL, CELL, CELL)
        pygame.draw.rect(surf, RED, r)
        pygame.draw.rect(surf, BLACK, r, 1)

class Snake:
    def __init__(self):
        self.body  = deque([(COLS // 2, ROWS // 2)])
        self.body_set = {self.body[0]}
        self.dir   = Dir.RIGHT
        self.grow_next = False

    def turn(self, new_dir: Dir):
        if not new_dir.is_opposite(self.dir):
            self.dir = new_dir

    def move(self):
        head = self.body[0]
        new = ((head[0] + self.dir.dx) % COLS,
               (head[1] + self.dir.dy) % ROWS)
        if new in self.body_set:
            return None
        self.body.appendleft(new)
        self.body_set.add(new)
        if self.grow_next:
            self.grow_next = False
        else:
            tail = self.body.pop()
            self.body_set.remove(tail)
        return new

    def draw(self, surf):
        for (x, y) in self.body:
            r = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
            pygame.draw.rect(surf, GREEN, r)
            pygame.draw.rect(surf, BLACK, r, 1)

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.food  = Food(self.snake.body_set)
        self.score = 0
        self.game_over = False
        self.fps = FPS_START

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and self.snake.dir != Dir.DOWN:
            self.snake.turn(Dir.UP)
        if pressed[pygame.K_DOWN] and self.snake.dir != Dir.UP:
            self.snake.turn(Dir.DOWN)
        if pressed[pygame.K_LEFT] and self.snake.dir != Dir.RIGHT:
            self.snake.turn(Dir.LEFT)
        if pressed[pygame.K_RIGHT] and self.snake.dir != Dir.LEFT:
            self.snake.turn(Dir.RIGHT)

    def update(self):
        new_head = self.snake.move()
        if new_head is None:
            self.game_over = True
            return
        if new_head == self.food.position:
            self.score += 1
            self.snake.grow_next = True
            self.food.spawn(self.snake.body_set)

    def draw(self):
        screen.fill(WHITE)
        # Optional: draw grid if needed
        # for y in range(0, HEIGHT, CELL):
        #     for x in range(0, WIDTH, CELL):
        #         pygame.draw.rect(screen, BLACK, (x, y, CELL, CELL), 1)
        self.snake.draw(screen)
        self.food.draw(screen)
        font = pygame.font.Font(None, 36)
        surf = font.render(f"Score: {self.score}", True, BLUE)
        screen.blit(surf, (8, 8))
        pygame.display.flip()

    def run(self):
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN and self.game_over:
                    self.reset()
            if not self.game_over:
                self.handle_input()
                self.update()
                self.draw()
            else:
                font = pygame.font.Font(None, 72)
                over = font.render("GAME OVER", True, BLUE)
                rect = over.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(over, rect)
                sub = pygame.font.Font(None, 36).render("Press any key to restart", True, BLUE)
                sr = sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
                screen.blit(sub, sr)
                pygame.display.flip()
            clock.tick(self.fps)

if __name__ == "__main__":
    Game().run()
