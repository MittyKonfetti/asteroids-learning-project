import pygame
from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, SHOT_RADIUS, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, BOOST_TIMER, BOOSTED_RADIUS

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cd_timer = 0
        self.boost_timer = 0
        

    def star(self):
        start_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        points = []
        for i in range(10):
            point_vector = start_vector.rotate(i * 36)
            if i % 2 != 0:
                points.append(self.position + point_vector * self.radius)
            else:
                points.append(self.position + point_vector * (self.radius * 0.5))
        return points
    
    def draw(self, screen):
        points = self.star()
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)
        pygame.draw.lines(screen, "red", False, points[4:7], LINE_WIDTH)
        if self.boost_timer > 0:
            pygame.draw.circle(screen, "red", self.position, BOOSTED_RADIUS, LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_DOWN]:
            self.move(dt * -1)
        if keys[pygame.K_LEFT]:
            self.rotate(dt * -1)                    
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.shoot()
        if keys[pygame.K_SPACE]:
            self.multi_shot()
        ########### weapon/other cooldown timers below #############    
        if self.cd_timer > 0:
            self.cd_timer -= dt
        if self.boost_timer > 0:
            self.boost_timer -= dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, -1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def collides_with(self, other):
        distance = pygame.math.Vector2.distance_to(self.position, other.position)
        if self.boost_timer > 0:
            return distance <= (BOOSTED_RADIUS + other.radius)
        return distance <= (self.radius + other.radius)

    def shoot(self):
        if self.cd_timer <= 0:
            self.cd_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def multi_shot(self):
        if self.cd_timer <= 0:
            self.cd_timer = PLAYER_SHOOT_COOLDOWN_SECONDS * 5
            for i in range(5):
                multi_shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
                multi_shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation + (i * 72)) * PLAYER_SHOOT_SPEED

    def get_boosted(self):
        self.boost_timer = BOOST_TIMER