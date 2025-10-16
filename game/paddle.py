import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7

    def move(self, dy, screen_height):
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        """Make AI paddle slower and less perfect."""
        ai_speed = 4  # slower speed for fairness
        margin = 10   # margin for imperfection

        if ball.y + ball.height / 2 < self.y + margin:
            self.move(-ai_speed, screen_height)
        elif ball.y + ball.height / 2 > self.y + self.height - margin:
            self.move(ai_speed, screen_height)
