import pygame
import random
from sys import exit

###Variables
width = 600
height = 600
box_x_vel = 3
box_y_vel = 4

pygame.init()


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("DVD Screensaver")
clock = pygame.time.Clock()

box = pygame.Surface((100,100))
box_rect = box.get_rect()
box.fill('Red')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    box_rect.centerx += box_x_vel
    box_rect.centery += box_y_vel


    if box_rect.right>=width or box_rect.left <= 0:
        box_x_vel *= random.randint(-110,-90)/100
    if box_rect.top <= 0 or box_rect.bottom >= height :
        box_y_vel *= random.randint(-110,-90)/100

    screen.fill('Black')
    screen.blit(box, box_rect)

    

    pygame.display.update()
    clock.tick(60)
