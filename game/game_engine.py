import pygame
import os
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

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
        self.game_over = False
        self.winner = None
        self.winning_score = 5
        self.show_replay_menu = False

        # Initialize sound
        self.init_sounds()

    def init_sounds(self):
        """Load sound effects."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            sounds_dir = os.path.dirname(__file__)
            self.paddle_hit_sound = pygame.mixer.Sound(os.path.join(sounds_dir, 'paddle_hit.wav'))
            self.wall_bounce_sound = pygame.mixer.Sound(os.path.join(sounds_dir, 'wall_bounce.wav'))
            self.score_sound = pygame.mixer.Sound(os.path.join(sounds_dir, 'score.wav'))

            self.paddle_hit_sound.set_volume(0.3)
            self.wall_bounce_sound.set_volume(0.2)
            self.score_sound.set_volume(0.4)

        except pygame.error as e:
            print(f"Warning: Could not load sound files: {e}")
            self.paddle_hit_sound = None
            self.wall_bounce_sound = None
            self.score_sound = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def play_sound(self, sound_type):
        """Play sound effect."""
        if sound_type == 'paddle_hit' and self.paddle_hit_sound:
            self.paddle_hit_sound.play()
        elif sound_type == 'wall_bounce' and self.wall_bounce_sound:
            self.wall_bounce_sound.play()
        elif sound_type == 'score' and self.score_sound:
            self.score_sound.play()

    def update(self):
        if not self.game_over:
            self.ball.move(self.play_sound)
            self.ball.check_collision(self.player, self.ai, self.play_sound)

            # Scoring
            if self.ball.x <= 0:
                self.ai_score += 1
                self.play_sound('score')
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.play_sound('score')
                self.ball.reset()

            # Win check
            if self.player_score >= self.winning_score:
                self.game_over = True
                self.winner = "Idhant"
            elif self.ai_score >= self.winning_score:
                self.game_over = True
                self.winner = "AI"

            self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        if not self.game_over:
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

            # Draw score
            idhant_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(idhant_text, (self.width // 4, 20))
            screen.blit(ai_text, (self.width * 3 // 4, 20))
        else:
            if self.show_replay_menu:
                self.render_replay_menu(screen)
            else:
                self.render_game_over(screen)

    def render_game_over(self, screen):
        game_over_font = pygame.font.SysFont("Arial", 48)
        winner_font = pygame.font.SysFont("Arial", 36)
        instruction_font = pygame.font.SysFont("Arial", 24)

        game_over_text = game_over_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 60))
        screen.blit(game_over_text, game_over_rect)

        winner_text = winner_font.render(f"{self.winner} Wins!", True, WHITE)
        winner_rect = winner_text.get_rect(center=(self.width // 2, self.height // 2 - 10))
        screen.blit(winner_text, winner_rect)

        score_text = instruction_font.render(
            f"Final Score: Idhant {self.player_score} - AI {self.ai_score}", True, WHITE
        )
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 30))
        screen.blit(score_text, score_rect)

        instruction_text = instruction_font.render("Press ESC to exit or SPACE for replay options", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(self.width // 2, self.height // 2 + 70))
        screen.blit(instruction_text, instruction_rect)

    def reset_game(self):
        """Reset all values for new match."""
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.ball.reset()
        self.player = Paddle(10, self.height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(self.width - 20, self.height // 2 - 50, self.paddle_width, self.paddle_height)

    def render_replay_menu(self, screen):
        title_font = pygame.font.SysFont("Arial", 36)
        option_font = pygame.font.SysFont("Arial", 28)
        instruction_font = pygame.font.SysFont("Arial", 20)

        title_text = title_font.render("Choose Game Mode", True, WHITE)
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2 - 100))
        screen.blit(title_text, title_rect)

        options = [
            ("Press 3 - Best of 3 (First to 2 wins)", 3),
            ("Press 5 - Best of 5 (First to 3 wins)", 5),
            ("Press 7 - Best of 7 (First to 4 wins)", 7),
            ("Press ESC - Exit Game", 0),
        ]

        y_offset = self.height // 2 - 40
        for option_text, _ in options:
            text = option_font.render(option_text, True, WHITE)
            rect = text.get_rect(center=(self.width // 2, y_offset))
            screen.blit(text, rect)
            y_offset += 40

        instruction_text = instruction_font.render("Select your preferred game mode", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(self.width // 2, self.height // 2 + 120))
        screen.blit(instruction_text, instruction_rect)

    def start_new_game(self, winning_score):
        """Start new game with target score."""
        self.winning_score = winning_score
        self.reset_game()
        self.show_replay_menu = False
