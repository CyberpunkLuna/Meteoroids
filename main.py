import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score import Score

def main():
    #init pygame and associated clock and screen objects
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Meteoroids!')

    #init font
    font = pygame.font.Font('freesansbold.ttf', 32)

    respawn_text = font.render('You died... Respawning...', True, "white", "black")
    respawn_rect = respawn_text.get_rect()
    respawn_rect.center = (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2)

    gameover_text = font.render('GAME OVER', True, "white", "black")
    gameover_rect = gameover_text.get_rect()
    gameover_rect.center = (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2)

    #init groups for easy updating
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    
    #init the game objects
    score = Score()
    player = Player((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))
    asteroidfield = AsteroidField()

    #game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        updatable.update(dt)
        for asteroid in asteroids:
            if player.is_colliding(asteroid):
                if player.death():
                    screen.blit(gameover_text, gameover_rect)
                    pygame.display.flip()
                    pygame.time.delay(5000)
                    print("Game over!")
                    score.update_time(pygame.time.get_ticks() - (RESPAWN_TIMER * 1000 * PLAYER_STARTING_LIVES))
                    score.print_score()
                    return
                else:
                    for asteroid in asteroids:
                        asteroid.kill()
                    screen.fill("black")
                    screen.blit(respawn_text, respawn_rect)
                    pygame.display.flip()
                    pygame.time.delay(RESPAWN_TIMER * 1000)
                    player.respawn()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.is_colliding(shot):
                    asteroid.split()
                    shot.kill()
                    score.update_score()

        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60)/1000

if __name__ == "__main__":
    main()
