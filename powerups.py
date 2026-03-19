import pygame
import random
from circleshape import CircleShape
from constants import PLAYER_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH, POWERUP_LIFE_SPAN

class Powerup(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
        self.radius = PLAYER_RADIUS / 3
        self.life_span = POWERUP_LIFE_SPAN
        self.generate = random.randint(1, 4)
        self.type = ""

    def draw(self, screen):
        if self.generate == 1:
            pygame.draw.circle(screen, "green", self.position, self.radius, 0)
            self.type = "green"
        if self.generate == 2:
            pygame.draw.circle(screen, "red", self.position, self.radius, 0)
            self.type = "red"
        if self.generate == 3:
            pygame.draw.circle(screen, "orange", self.position, self.radius, 0)
            self.type = "orange"
        if self.generate == 4:
            pygame.draw.circle(screen, "white", self.position, self.radius, 0)
            self.type = "white"

    def update(self, dt):
        if self.life_span <= 0:
            self.kill()
        self.life_span -= dt
