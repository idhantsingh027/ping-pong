import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, sound_callback=None):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if sound_callback:
                sound_callback('wall_bounce')

    def check_collision(self, player, ai, sound_callback=None):
        # Player (Idhant) paddle collision
        if self.rect().colliderect(player.rect()):
            if self.velocity_x < 0:  # Only if moving toward Idhant
                self.velocity_x *= -1
                hit_pos = (self.y + self.height / 2) - (player.y + player.height / 2)
                self.velocity_y += hit_pos * 0.1
                self.velocity_y = max(-8, min(8, self.velocity_y))
                if sound_callback:
                    sound_callback('paddle_hit')

        # AI paddle collision
        if self.rect().colliderect(ai.rect()):
            if self.velocity_x > 0:  # Only if moving toward AI
                self.velocity_x *= -1
                hit_pos = (self.y + self.height / 2) - (ai.y + ai.height / 2)
                self.velocity_y += hit_pos * 0.1
                self.velocity_y = max(-8, min(8, self.velocity_y))
                if sound_callback:
                    sound_callback('paddle_hit')

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
