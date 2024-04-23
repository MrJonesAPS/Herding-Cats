import pygame
import random

class Herder(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        # walking right sprites
        walk_r_1 = pygame.image.load(f"graphics/herder/tile003.png").convert_alpha()
        walk_r_2 = pygame.image.load(f"graphics/herder/tile004.png").convert_alpha()
        walk_r_3 = pygame.image.load(f"graphics/herder/tile005.png").convert_alpha()
        self.walk_r = [walk_r_1, walk_r_2, walk_r_3, walk_r_2]

        # walking left sprites
        walk_l_1 = pygame.image.load(f"graphics/herder/tile009.png").convert_alpha()
        walk_l_2 = pygame.image.load(f"graphics/herder/tile010.png").convert_alpha()
        walk_l_3 = pygame.image.load(f"graphics/herder/tile011.png").convert_alpha()
        self.walk_l = [walk_l_1, walk_l_2, walk_l_3, walk_l_2]

        # walking up sprites
        walk_u_1 = pygame.image.load(f"graphics/herder/tile000.png").convert_alpha()
        walk_u_2 = pygame.image.load(f"graphics/herder/tile001.png").convert_alpha()
        walk_u_3 = pygame.image.load(f"graphics/herder/tile002.png").convert_alpha()
        self.walk_u = [walk_u_1, walk_u_2, walk_u_3, walk_u_2]

        # walking down sprites
        walk_d_1 = pygame.image.load(f"graphics/herder/tile006.png").convert_alpha()
        walk_d_2 = pygame.image.load(f"graphics/herder/tile007.png").convert_alpha()
        walk_d_3 = pygame.image.load(f"graphics/herder/tile008.png").convert_alpha()
        self.walk_d = [walk_d_1, walk_d_2, walk_d_3, walk_d_2]

        self.direction = "r"
        self.turn()

        self.animation_index = 0
        self.image = self.walk_r[self.animation_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.animate()
        screen = pygame.display.get_surface()
        self.rect = self.image.get_rect(
            topleft=(
                random.randint(50, screen.get_width() - 50),
                random.randint(50, screen.get_height() - 50),
            )
        )
        self.speed = speed
        self.pause_time = 0

    def turn(self):
        self.direction = random.choice(["l", "r", "u", "d"])

    def move(self, fences):

        oldPosition = self.rect.center

        screen = pygame.display.get_surface()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top >= 0:
            self.direction = "u"
            self.rect.top -= self.speed
            self.animation_index += 0.1
        elif keys[pygame.K_s] and self.rect.bottom <= screen.get_height():
            self.direction = "d"
            self.rect.bottom += self.speed
            self.animation_index += 0.1
        elif keys[pygame.K_a] and self.rect.left >= 0:
            self.direction = "l"
            self.rect.left -= self.speed
            self.animation_index += 0.1
        elif keys[pygame.K_d] and self.rect.right <= screen.get_width():
            self.direction = "r"
            self.rect.right += self.speed
            self.animation_index += 0.1
        
        joystick_herder = None
        if pygame.joystick.get_count() > 0:
            joystick_herder = pygame.joystick.Joystick(0)

        if joystick_herder is not None:
            deadzone = 0.1
            x_axis_pos = joystick_herder.get_axis(1)
            y_axis_pos = joystick_herder.get_axis(0)
            if abs(x_axis_pos) > abs(y_axis_pos):
                if x_axis_pos < -1 * deadzone:
                    self.direction = "u"
                    self.rect.top -= self.speed
                    self.animation_index += 0.1
                elif x_axis_pos > deadzone:
                    self.direction = "d"
                    self.rect.bottom += self.speed
                    self.animation_index += 0.1
            else:
                if y_axis_pos < -1 * deadzone:
                    self.direction = "l"
                    self.rect.left -= self.speed
                    self.animation_index += 0.1
                elif y_axis_pos > deadzone:
                    self.direction = "r"
                    self.rect.right += self.speed
                    self.animation_index += 0.1

        #after moving, if the cat collided with a fence, undo the move
        didCollide = False
        for f in fences.sprites():
            if pygame.sprite.collide_mask(self,f):
                didCollide = True
        if didCollide: 
            self.rect.center = oldPosition

    def animate(self):

        if self.animation_index >= 4:
            self.animation_index = 0
        if self.direction == "r":
            self.image = self.walk_r[int(self.animation_index)]
            self.mask = pygame.mask.from_surface(self.image)
        if self.direction == "l":
            self.image = self.walk_l[int(self.animation_index)]
            self.mask = pygame.mask.from_surface(self.image)
        if self.direction == "u":
            self.image = self.walk_u[int(self.animation_index)]
            self.mask = pygame.mask.from_surface(self.image)
        if self.direction == "d":
            self.image = self.walk_d[int(self.animation_index)]
            self.mask = pygame.mask.from_surface(self.image)

    def update(self, fences):
        if self.pause_time == 0:
            self.move(fences)
            self.animate()
        else:
            self.pause_time -= 1
