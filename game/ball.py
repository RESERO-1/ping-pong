import pygame

class Ball:
    def __init__(self, x, y, velocity_x, velocity_y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self):
        # Move ball
        self.x += self.velocity_x
        self.y += self.velocity_y

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def reset(self):
        self.x = self.screen_width // 2 - self.width // 2
        self.y = self.screen_height // 2 - self.height // 2
        self.velocity_x *= -1  # change direction
        self.velocity_y = 0
