import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, BOMB_TIMER, BOMB_RADIUS

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += (self.velocity * dt)

class Bomb(Shot):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.timer = BOMB_TIMER
        self.radius = BOMB_RADIUS

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.explodes()

    def explodes(self):
        self.kill()
