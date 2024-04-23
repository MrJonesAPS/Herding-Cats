import pygame
import random


class Cat(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.color = random.choice(["white", "black", "brown", "orange"])

        # walking right sprites
        walk_r_1 = pygame.image.load(
            f"graphics/cats/{self.color}/tile003.png"
        )  # .convert_alpha()
        walk_r_2 = pygame.image.load(
            f"graphics/cats/{self.color}/tile004.png"
        )  # .convert_alpha()
        walk_r_3 = pygame.image.load(
            f"graphics/cats/{self.color}/tile005.png"
        )  # .convert_alpha()
        self.walk_r = [walk_r_1, walk_r_2, walk_r_3, walk_r_2]

        # walking left sprites
        walk_l_1 = pygame.image.load(
            f"graphics/cats/{self.color}/tile009.png"
        )  # .convert_alpha()
        walk_l_2 = pygame.image.load(
            f"graphics/cats/{self.color}/tile010.png"
        )  # .convert_alpha()
        walk_l_3 = pygame.image.load(
            f"graphics/cats/{self.color}/tile011.png"
        )  # .convert_alpha()
        self.walk_l = [walk_l_1, walk_l_2, walk_l_3, walk_l_2]

        # walking up sprites
        walk_u_1 = pygame.image.load(
            f"graphics/cats/{self.color}/tile000.png"
        )  # .convert_alpha()
        walk_u_2 = pygame.image.load(
            f"graphics/cats/{self.color}/tile001.png"
        )  # .convert_alpha()
        walk_u_3 = pygame.image.load(
            f"graphics/cats/{self.color}/tile002.png"
        )  # .convert_alpha()
        self.walk_u = [walk_u_1, walk_u_2, walk_u_3, walk_u_2]

        # walking down sprites
        walk_d_1 = pygame.image.load(
            f"graphics/cats/{self.color}/tile006.png"
        )  # .convert_alpha()
        walk_d_2 = pygame.image.load(
            f"graphics/cats/{self.color}/tile007.png"
        )  # .convert_alpha()
        walk_d_3 = pygame.image.load(
            f"graphics/cats/{self.color}/tile008.png"
        )  # .convert_alpha()
        self.walk_d = [walk_d_1, walk_d_2, walk_d_3, walk_d_2]

        self.direction = "r"
        self.turn()

        self.animation_index = 0
        self.image = self.walk_r[self.animation_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.animate()
        self.speed = speed

        screen = pygame.display.get_surface()
        self.rect = self.image.get_rect(
            topleft=(
                random.randint(50, screen.get_width() - 50),
                random.randint(50, screen.get_height() - 50),
            )
        )

    def turn(self):
        self.direction = random.choice(["l", "r", "u", "d"])

    def move(self, fences):
        pass

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
        self.move(fences)
        self.animate()


class PlayerCat(Cat):
    # the only difference about the player cat is that we control with the keys
    def move(self, fences):
        keys = pygame.key.get_pressed()
        oldPosition = self.rect.center
        screen = pygame.display.get_surface()
        if keys[pygame.K_UP] and self.rect.top >= 0:
            self.direction = "u"
            self.rect.top -= self.speed
            self.animation_index += 0.1
        elif keys[pygame.K_DOWN] and self.rect.bottom <= screen.get_height():
            self.direction = "d"
            self.rect.bottom += self.speed
            self.animation_index += 0.1
        elif keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.direction = "l"
            self.rect.left -= self.speed
            self.animation_index += 0.1
        elif keys[pygame.K_RIGHT] and self.rect.right <= screen.get_width():
            self.direction = "r"
            self.rect.right += self.speed
            self.animation_index += 0.1

        # after moving, if the cat collided with a fence, undo the move
        didCollide = False
        for f in fences.sprites():
            if pygame.sprite.collide_mask(self, f):
                didCollide = True
        if didCollide:
            self.rect.center = oldPosition


class AutoCat(Cat):
    # the auto cat moves on it own

    def __init__(self, speed):
        super().__init__(speed)
        self.pause_timer = 0

    def move(self, fences):
        if self.pause_timer >= 0:
            self.pause_timer -= 1

        # elif self.:
        # if the farmer is close to the cat, it'll run away a little bit faster

        else:

            oldPosition = self.rect.center
            screen = pygame.display.get_surface()
            # by default it'll keep going, unless it runs into walls
            if random.randint(1, 60) == 1:
                self.turn()
            if self.direction == "r" and self.rect.right <= screen.get_width():
                self.rect.right += self.speed
                self.animation_index += 0.1
            elif self.direction == "l" and self.rect.left >= 0:
                self.rect.left -= self.speed
                self.animation_index += 0.1
            elif self.direction == "u" and self.rect.top >= 0:
                self.rect.top -= self.speed
                self.animation_index += 0.1
            elif self.direction == "d" and self.rect.bottom <= screen.get_height():
                self.rect.bottom += self.speed
                self.animation_index += 0.1
            else:
                # we hit a wall
                self.turn()

                # after moving, if the cat collided with a fence, undo the move
            didCollide = False
            for f in fences.sprites():
                if pygame.sprite.collide_mask(self, f):
                    didCollide = True
            if didCollide:
                self.rect.center = oldPosition

        # should we start a pause?
        if random.randint(0, 120) == 0:
            self.pause_timer = random.randint(30, 60)
