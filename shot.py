import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, BOMB_TIMER, BOMB_RADIUS, BOMB_EXPLOSION_RADIUS, BOMB_EXPLOSION_INCREMENT, SHOT_RADIUS, PLAYER_SHOOT_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def multi_shot(position, rotation):
        for i in range(5):
            multishot = Shot(position.x, position.y, SHOT_RADIUS)
            multishot.velocity = pygame.Vector2(0, -1).rotate(rotation + (i * 72)) * PLAYER_SHOOT_SPEED

class Bomb(Shot):
    def __init__(self, x, y, radius, rotation):
        super().__init__(x, y, radius)
        self.timer = BOMB_TIMER
        self.rotation = rotation
        self.explosion_radius = BOMB_EXPLOSION_RADIUS
        self.bomb_trigger = False

    def draw(self, screen):
        if self.bomb_trigger == False:
            pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)
            if pygame.time.get_ticks() % 1000 < 500:
                pygame.draw.circle(screen, "white", self.position, self.radius - 2, 0)
        else:
            pygame.draw.circle(screen, "orange", self.position, self.radius, LINE_WIDTH)
        

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            Shot.multi_shot(self.position, self.rotation)
            self.kill()
        ####explosion logic below####
        if self.bomb_trigger == True:
            self.radius += BOMB_EXPLOSION_INCREMENT
            if self.radius >= BOMB_EXPLOSION_RADIUS:
                self.kill()

    def explodes(self):
        self.bomb_trigger = True

