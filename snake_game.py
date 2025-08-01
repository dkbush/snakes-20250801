import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 10

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Starting direction: right
        self.grow = False
    
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_position = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        
        # Game over if snake collides with itself
        if new_position in self.positions[1:]:
            return False
        
        self.positions.insert(0, new_position)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True
    
    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
    
    def render(self, surface):
        for position in self.positions:
            rect = pygame.Rect(
                (position[0] * GRID_SIZE, position[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
    
    def render(self, surface):
        rect = pygame.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, BLACK, rect, 1)

def draw_score(surface, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLUE)
    surface.blit(text, (5, 5))

def main():
    snake = Snake()
    food = Food()
    score = 0
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over:
                    game_over = False
                    snake.reset()
                    food.randomize_position()
                    score = 0
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
        
        if not game_over:
            # Update the snake's position
            if not snake.update():
                game_over = True
            
            # Check if snake ate the food
            if snake.get_head_position() == food.position:
                snake.grow = True
                score += 1
                food.randomize_position()
                # Make sure food doesn't spawn inside the snake
                while food.position in snake.positions:
                    food.randomize_position()
        
        screen.fill(WHITE)
        draw_grid(screen)
        snake.render(screen)
        food.render(screen)
        draw_score(screen, score)
        
        if game_over:
            font = pygame.font.Font(None, 72)
            text = font.render("GAME OVER", True, BLUE)
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, text_rect)
            
            font = pygame.font.Font(None, 36)
            text = font.render("Press any key to restart", True, BLUE)
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            screen.blit(text, text_rect)
            
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()