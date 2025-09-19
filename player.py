import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_timer = 0
        self.lives = PLAYER_STARTING_LIVES

    # creates triangle points
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c] 
    
    # rotates the player
    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)

    # moves the player forwards and backwards
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += (forward * PLAYER_SPEED * dt)
        if self.velocity.length() >= PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

    # Handles velocity drifting
    def drift(self, dt):
        self.position += (self.velocity * dt)

    # Collision behavior (overrides __super__ as to create a triangular hitbox)
    def is_colliding(self, object):
        bool_touching_edge = list(map(lambda x: True if (x.distance_to(object.position) - object.radius) <= 0 else False, self.triangle()))
        if True in bool_touching_edge:
            return True
        else:
            return False
        
    #behavior to respawn after dying if more lives are available
    def death(self):
        if self.lives > 1:
            self.lives -= 1
            return False
        else:
            return True
    
    def respawn(self):
        self.velocity = pygame.Vector2(0, 0)
        self.position = pygame.Vector2((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))

    # updates game sprite rotation
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shot_timer -= dt
        self.wrap_around()
        self.drift(dt)

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    # handles shooting behaivior
    def shoot(self):
        if self.shot_timer > 0:
            pass
        else:
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            shot.velocity = (pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED)
            self.shot_timer = PLAYER_SHOOT_COOLDOWN

    #checks to see if player is offscreen and wraps the player to the other side of the screen (while this functions similarly to is_offscreen I didnt want to duplicate the logic that checks if a sprite is offscreen)
    def wrap_around(self):
        if self.position.x + self.radius < 0:
            self.position.x = SCREEN_WIDTH + self.radius
        if self.position.x - self.radius > SCREEN_WIDTH:
            self.position.x = 0 - self.radius
        if self.position.y + self.radius < 0:
            self.position.y = SCREEN_HEIGHT + self.radius
        if self.position.y - self.radius > SCREEN_HEIGHT:
            self.position.y = 0 - self.radius
        return
    
    # override of draw method
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), width=2)