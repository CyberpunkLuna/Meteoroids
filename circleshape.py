import pygame
from constants import *

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    # Collision behavior (subclasses may override)
    def is_colliding(self, object):
        if (self.position.distance_to(object.position) <= (self.radius + object.radius)):
            return True
        else:
            return False
        
    # returns True if the entire circular sprite is offscreen (subclasses may override)
    def is_offscreen(self):
        if self.position.x + self.radius < 0:
            return True
        if self.position.x - self.radius > SCREEN_WIDTH:
            return True
        if self.position.y + self.radius < 0:
            return True
        if self.position.y - self.radius > SCREEN_HEIGHT:
            return True
        return False

    def wrap_around(self):
        # sub-classes must override
        pass

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass