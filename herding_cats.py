#####
# Art attribution:
#   Cats: "[LPC] Cats and Dogs" by bluecarrot16
#   https://opengameart.org/content/lpc-cats-and-dogs
#
#   Player: "Universal LPC Sprite Male 01"
#   https://opengameart.org/content/universal-lpc-sprite-male-01
#
#   Terrain and Fences: "[LPC] Farming tilesets, magic animations and UI elements" by daneeklu
#   https://opengameart.org/content/lpc-farming-tilesets-magic-animations-and-ui-elements
#
#   Meow Sounds:    https://opengameart.org/content/meow
#
#   RPG Music: https://opengameart.org/content/rpg-the-mysterious-companion
#
#   Fence Hammer Sound: https://opengameart.org/content/fast-hammer-sfx
#
#####


import pygame
import random
from sys import exit
from Cat import PlayerCat, AutoCat
from Herder import Herder
from Fence import Fence_Segment


def reset_game():
    global frames_till_start, winner

    winner = None

    if len(herder.sprites()) > 0:
        herder.remove(herder.sprites()[0])
    herder.add(Herder(herder_speed))

    if len(player_cat.sprites()) > 0:
        player_cat.remove(player_cat.sprites()[0])
    for c in npc_cats.sprites():
        npc_cats.remove(c)

    for f in fences.sprites():
        fences.remove(f)

    player_cat.add(PlayerCat(cat_speed))
    for _ in range(10):
        npc_cats.add(AutoCat(cat_speed))
    frames_till_start = 180

    generateBackground()


def generateBackground():

    background.fill([47, 129, 53])

    for _ in range(20):
        background.blit(
            grass,
            (
                random.randint(50, screen.get_width() - 50),
                random.randint(50, screen.get_height() - 50),
            ),
        )


def drawFence2(
    coords, stepX, stepY, lastX, lastY, whileLoopCondition, start, mid, stop
):
    pauseTime = 30
    if whileLoopCondition(coords):
        print("Drawing bottom fence at coords: " + str(coords))
        # background.blit(start, coords)
        fences.add(Fence_Segment(start, coords))
        pauseTime = 15
        while whileLoopCondition(coords):

            coords = (coords[0] + stepX, coords[1] + stepY)
            print("Drawing mid fence at coords: " + str(coords))
            # background.blit(mid, coords)
            fences.add(Fence_Segment(mid, coords))
            pauseTime += 15
        coords = (lastX, lastY)
        print("Drawing top fence at coords: " + str(coords))
        # background.blit(stop, coords)
        fences.add(Fence_Segment(stop, coords))
        pauseTime += 15
    else:
        print("Can't draw fence here. Too close to edge")

    return pauseTime


def drawFence(direction):
    halfFence = 32 / 2

    # start at the centerY of the herder, and a little to the left of the centerX of the herder
    coords = (
        herder.sprites()[0].rect.centerx - halfFence,
        herder.sprites()[0].rect.centery,
    )

    pauseTime = 0

    if direction == "u":
        pauseTime = drawFence2(
            coords=(coords[0], coords[1] - 64),
            stepX=0,
            stepY=-32,
            lastX=coords[0],
            lastY=0,
            whileLoopCondition=lambda coords: coords[1] > 32,
            start=fence_v_bottom,
            mid=fence_v_center,
            stop=fence_v_top,
        )
    elif direction == "d":
        pauseTime = drawFence2(
            coords=(coords[0], coords[1] + 32),
            stepX=0,
            stepY=32,
            lastX=coords[0],
            lastY=screen.get_height() - 32,
            whileLoopCondition=lambda coords: coords[1] < (screen.get_height() - 64),
            start=fence_v_top,
            mid=fence_v_center,
            stop=fence_v_bottom,
        )
    elif direction == "r":
        pauseTime = drawFence2(
            coords=(coords[0] + 32, coords[1]),
            stepX=32,
            stepY=0,
            lastX=screen.get_width() - 32,
            lastY=coords[1],
            whileLoopCondition=lambda coords: coords[0] < (screen.get_width() - 64),
            start=fence_h_left,
            mid=fence_h_center,
            stop=fence_h_right,
        )
    elif direction == "l":
        pauseTime = drawFence2(
            coords=(coords[0] - 32, coords[1]),
            stepX=-32,
            stepY=0,
            lastX=0,
            lastY=coords[1],
            whileLoopCondition=lambda coords: coords[0] > 32,
            start=fence_h_right,
            mid=fence_h_center,
            stop=fence_h_left,
        )
    hammer_sound.play(pauseTime // 60)
    return pauseTime


###Variables
numCats = 10
herder_speed = 3
cat_speed = 2
frames_till_start = 180
width = 800
height = 800

pygame.init()


joystick_herder = None
if pygame.joystick.get_count() > 0:
    joystick_herder = pygame.joystick.Joystick(0)


screen = pygame.display.set_mode((width, height))
background = pygame.Surface((screen.get_width(), screen.get_height()))
pygame.display.set_caption("Herding Cats")
clock = pygame.time.Clock()


myfont = pygame.font.Font(None, 100)
subtitleFont = pygame.font.Font(None, 50)
get_ready_text = myfont.render("GET READY", False, "Red")
get_ready_rect = get_ready_text.get_rect(center=(width / 2, height / 4))

herder_instructions_text = subtitleFont.render(
    "HERDER: Use the gamepad's left joystick to move. \n"
    + "Press A to draw a fence\n"
    + "Making a fence takes time - longer fence = longer freeze",
    False,
    "Red",
)
herder_instructions_rect = herder_instructions_text.get_rect(
    center=(width / 3, height / 2)
)

cat_instructions_text = subtitleFont.render(
    "CAT: Use arrow keys to move. \n" + "Try to blend in with the other cats!\n",
    False,
    "Red",
)
cat_instructions_rect = cat_instructions_text.get_rect(
    center=(2 * width / 3, height / 2)
)

cats_won_text = myfont.render("THE CATS WON", False, "Red")
cats_won_rect = cats_won_text.get_rect(center=(width / 2, height / 2))

herder_won_text = myfont.render("THE HERDER WON", False, "Red")
herder_won_rect = herder_won_text.get_rect(center=(width / 2, height / 2))

grass = pygame.image.load(f"graphics/grass/tile016.png")  # .convert_alpha()

fence_h_left = pygame.image.load(f"graphics/fence/tile000.png")
fence_h_center = pygame.image.load(f"graphics/fence/tile001.png")
fence_h_right = pygame.image.load(f"graphics/fence/tile002.png")
fence_v_bottom = pygame.image.load(f"graphics/fence/tile003.png")
fence_v_center = pygame.image.load(f"graphics/fence/tile004.png")
fence_v_top = pygame.image.load(f"graphics/fence/tile005.png")

meow_sound = pygame.mixer.Sound("sounds/Meow.ogg")
music = pygame.mixer.music.load("sounds/RPG - The Mysterious Companion.ogg", "ogg")
hammer_sound = pygame.mixer.Sound("sounds/craft.ogg")
pygame.mixer.music.play(-1)

player_cat = pygame.sprite.GroupSingle()
herder = pygame.sprite.GroupSingle()
npc_cats = pygame.sprite.Group()
fences = pygame.sprite.Group()
winner = None
reset_game()

while True:

    # exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1:

                pause_time = drawFence(herder.sprite.direction)
                herder.sprite.pause_time = pause_time
            # if event.button == 0:
            # print("B button pressed")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        reset_game()
    if keys[pygame.K_f]:
        pause_time = drawFence(herder.sprite.direction)
        herder.sprite.pause_time = pause_time

    screen.blit(background, (0, 0))

    player_cat.draw(screen)
    npc_cats.draw(screen)
    fences.draw(screen)
    herder.draw(screen)

    if frames_till_start > 0:
        # pygame.mixer.music.pause()
        frames_till_start -= 1
        screen.blit(get_ready_text, get_ready_rect)
        #screen.blit(herder_instructions_text, herder_instructions_rect)
        #screen.blit(cat_instructions_text, cat_instructions_rect)
        # 2 motors here, first parameter is low frequency, second is high
        # values are 0-1
        # joystick_herder.rumble(1, 0, 100)
    elif winner == "cats":
        screen.blit(cats_won_text, cats_won_rect)
    elif winner == "herder":
        screen.blit(herder_won_text, herder_won_rect)
    else:
        # if pygame.mixer.music.
        # pygame.mixer.music.unpause()
        player_cat.update(fences)
        npc_cats.update(fences)
        herder.update(fences)

        # did the herder hit any cats?
        for c in npc_cats:
            if pygame.sprite.collide_mask(herder.sprite, c):
                npc_cats.remove(c)
                meow_sound.play()
                if len(npc_cats.sprites()) == 0:
                    winner = "cats"

        # did the herder hit the player cat?
        if pygame.sprite.collide_mask(herder.sprite, player_cat.sprites()[0]):
            winner = "herder"

    pygame.display.update()
    # pygame.event.pump()
    clock.tick(60)
