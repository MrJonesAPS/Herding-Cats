import pygame

class Fence_Segment(pygame.sprite.Sprite):
    # a fence is a vector - it has a start point and a direction
    #
    def __init__(self, image, location):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=location)
        self.mask = pygame.mask.from_surface(self.image)