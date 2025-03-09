# filename: pong_game.py

import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Clock to control game refresh rate
clock = pygame.time.Clock()

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 5

    def move(self, up, down):
        keys = pygame.key.get_pressed()
        if keys[up] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.x_speed = random.choice([5, -5])
        self.y_speed = random.choice([5, -5])

    def move(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Ball collision with top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.y_speed = -self.y_speed

    def reset(self):
        self.rect.x = WIDTH // 2 - BALL_RADIUS
        self.rect.y = HEIGHT // 2 - BALL_RADIUS
        self.x_speed = random.choice([5, -5])
        self.y_speed = random.choice([5, -5])

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

# Main game loop
def game_loop():
    paddle_left = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle_right = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    # Game loop
    running = True
    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Paddle movement
        paddle_left.move(pygame.K_w, pygame.K_s)
        paddle_right.move(pygame.K_UP, pygame.K_DOWN)

        # Ball movement
        ball.move()

        # Ball collision with paddles
        if paddle_left.rect.colliderect(ball.rect) or paddle_right.rect.colliderect(ball.rect):
            ball.x_speed = -ball.x_speed

        # Ball out of bounds (left side or right side)
        if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
            ball.reset()

        # Draw everything
        paddle_left.draw()
        paddle_right.draw()
        ball.draw()

        # Update the screen
        pygame.display.update()

        # Frame rate control
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    game_loop()