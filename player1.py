import pygame
from circleshape import CircleShape
from shot import Shot, Bomb
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, ACCELERATE_CD, ACCELERATE_RATE, SHOT_RADIUS, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_MULTISHOT_CD, PLAYER_LIFE_COUNT, BOOST_TIMER, BOOSTED_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH, BOMB_TIMER, BOMB_RADIUS, BOMB_CD

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cd_timer = 0
        self.multishot_cd = 0
        self.bomb_cd = 0
        self.boost_timer = 0
        self.lives = PLAYER_LIFE_COUNT  
        self.speed = PLAYER_SPEED
        self.accelerate_cd = 0   
        self.accelerate_rate = ACCELERATE_RATE

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
            pygame.draw.circle(screen, "darkgreen", self.position, BOOSTED_RADIUS, LINE_WIDTH)
    
    def player_ui(self, screen, font):
        show_multishot_cd = font.render(f"{self.multishot_cd:.1f}", True, "white")
        show_bomb_cd = font.render(f"{self.bomb_cd:.1f}", True, "white")
        screen.blit(show_multishot_cd, (self.position.x + 25, self.position.y + 5))
        screen.blit(show_bomb_cd, (self.position.x + 25, self.position.y + 20))

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
        if keys[pygame.K_SPACE]:
            self.accelerate()
        if keys[pygame.K_q]:
            self.shoot()
        if keys[pygame.K_e]:
            self.bomb()
        if keys[pygame.K_w]:
            self.multi_shot()
        ########### weapon/other cooldown timers below #############    
        if self.cd_timer > 0:
            self.cd_timer -= dt
        if self.multishot_cd > 0:
            self.multishot_cd -= dt
        if self.boost_timer > 0:
            self.boost_timer -= dt
        if self.bomb_cd > 0:
            self.bomb_cd -= dt
        if self.accelerate_cd > 0:
            self.accelerate_cd -= dt
            self.speed += ACCELERATE_RATE * dt
        if self.accelerate_cd <= 0:
            if self.speed > PLAYER_SPEED:
                self.speed -= ACCELERATE_RATE * 2 * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, -1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * self.speed * dt
        self.position += rotated_with_speed_vector

    def accelerate(self):
        if self.accelerate_cd <= 0:
            self.accelerate_cd = ACCELERATE_CD

    def collides_with(self, other):
        distance = pygame.math.Vector2.distance_to(self.position, other.position)
        if self.boost_timer > 0:
            return distance <= (BOOSTED_RADIUS + other.radius)
        return distance <= (self.radius + other.radius)
    
    def handle_collision(self):
        if self.lives > 0:
            self.lives -= 1
            self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.get_boosted()
            print("You have 5 lives total. Might stay dead next time...")
            return True
        return False

    def shoot(self):
        if self.cd_timer <= 0:
            self.cd_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def multi_shot(self):
        if self.multishot_cd <= 0:
            self.multishot_cd = PLAYER_MULTISHOT_CD
            Shot.multi_shot(self.position, self.rotation)

    def bomb(self):
        if self.bomb_cd <= 0:
            self.bomb_cd = BOMB_CD
            bomb = Bomb(self.position.x, self.position.y, BOMB_RADIUS, self.rotation)

    def get_boosted(self):
        self.boost_timer = BOOST_TIMER