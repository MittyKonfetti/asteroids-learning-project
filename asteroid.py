import pygame
import random
import math
from logger import log_event
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.radii = []
        for i in range(20):
            rad = random.randint(self.radius - 5, self.radius +5)
            angle_deg = i * (360 / 20)
            angle_rad = math.radians(angle_deg)
            vector = pygame.Vector2(math.cos(angle_rad) * rad, math.sin(angle_rad) * rad)
            self.radii.append(vector)

    def draw(self, screen):
        radii_to_draw = []
        for r in self.radii:
            radii_to_draw.append(self.position + r)
        pygame.draw.polygon(screen, "white", radii_to_draw, 2)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        pygame.sprite.Sprite.kill(self)
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            random_angle = random.uniform(20, 50)
            first_vector = self.velocity.rotate(random_angle)
            second_vector = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            new_asteroid_one = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_two = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_one.velocity = first_vector * 1.2
            new_asteroid_two.velocity = second_vector * 1.2

    def bombed(self):
        pygame.sprite.Sprite.kill(self)
        
