import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player1 import Player
from asteroid import Asteroid
from circleshape import CircleShape
from asteroidfield import AsteroidField
from powerups import Powerup
from shot import Shot, Bomb


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    FPS = 60
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    players = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    Player.containers = (updatable, drawable, players)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Powerup.containers = (updatable, drawable, powerups)
    Shot.containers = (shots, drawable, updatable)
    Bomb.containers = (bombs, drawable, updatable)
    asteroid_field = AsteroidField()
    player1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for ast in asteroids:
            for player in players:
                if player.collides_with(ast):
                    if player.boost_timer > 0:
                        ast.split()
                    else:
                        still_alive = player.handle_collision()
                        if not still_alive:
                            log_event("player_hit")
                            print("Game Over!")
                            sys.exit()
            for shot in shots:
                if shot.collides_with(ast):
                    log_event("asteroid_shot")
                    shot.kill()
                    ast.split()
            for bomb in bombs:
                if bomb.collides_with(ast):
                    log_event("asteroid_bombed")
                    bomb.explodes()
                    ast.bombed()
        for p in powerups:
            for player in players:
                if p.collides_with(player):
                    log_event("power_boost_gained")
                    print("Power Boost!")
                    p.kill()
                    player.get_boosted()
        for dr in drawable:
            dr.draw(screen)
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000

if __name__ == "__main__":
    main()