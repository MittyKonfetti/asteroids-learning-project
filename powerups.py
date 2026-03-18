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

    def draw(self, screen):
        pygame.draw.circle(screen, "gold", self.position, self.radius, 0)

    def update(self, dt):
        if self.life_span <= 0:
            self.kill()
        self.life_span -= dt
