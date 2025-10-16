import pygame
import sys
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 60)

        self.game_over = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Only update if game not over
        if self.game_over:
            return

        self.ball.move(self.player, self.ai)

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # AI movement
        self.ai.auto_track(self.ball, self.height)

        # Check for game over
        self.check_game_over()

    def check_game_over(self):
        if self.player_score >= 5:
            self.display_winner("Idhant Wins!")
            self.game_over = True
        elif self.ai_score >= 5:
            self.display_winner("AI Wins!")
            self.game_over = True

    def display_winner(self, text):
        screen = pygame.display.get_surface()
        screen.fill(BLACK)

        message = self.large_font.render(text, True, WHITE)
        text_rect = message.get_rect(center=(self.width // 2, self.height // 2))
        screen.blit(message, text_rect)
        pygame.display.flip()

        # Keep screen visible for 3 seconds before closing
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    def render(self, screen):
        if not self.game_over:
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

            # Draw scores
            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width//4, 20))
            screen.blit(ai_text, (self.width * 3//4, 20))
