import pygame
from sys import exit
from random import choice
# from src.player import Player
# from src.zombie import Zombie
from settings import Settings
import time
pygame.init()
#Global variables
isGameRunning = True
iswin = False
istop = False
isbottom = True
#Display and asset info

    #bg_music = ...
    #bg_music.set_volume(0.5)
    
custom_font = pygame.font.Font("Pygame_nh-m-3/fonts/VCR_OSD_MONO_1.001.ttf")
display_surface = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))    
pygame.display.set_caption("Pygame")
clock = pygame.time.Clock()

#Background and obstancles
tmp_surface = pygame.image.load('Pygame_nh-m-3/asset/rect3.jpg')
tiles_surface = pygame.transform.scale(tmp_surface, (1400, 787))
tiles_rect = tiles_surface.get_rect(bottomleft = (0, Settings.SCREEN_HEIGHT))
tmp = pygame.image.load('Pygame_nh-m-3/asset/2 Objects/6 Decor/13.png')
well_surface = pygame.transform.scale(tmp, (90, 90))
well_rect = well_surface.get_rect(center = (950, 450))
#Players
dx = 0
dy = 0

player_surface = pygame.image.load('Pygame_nh-m-3/asset/2 Objects/6 Decor/4.png')
player_rect = player_surface.get_rect(bottomleft = (0, 680))
#Zombies


#Display 
while isGameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameRunning = False
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                dx = -3
            if event.key == pygame.K_d:
                dx = 3
            if event.key == pygame.K_w:
                dy = -3
            if event.key == pygame.K_s:
                dy = 3    
    display_surface.blit(tiles_surface, tiles_rect)
    if not iswin:
        display_surface.blit(well_surface, well_rect)
    player_rect.x += dx
    player_rect.y += dy
    if player_rect.left <= 0:
        player_rect.left = 0
    if not iswin:
        if player_rect.right >= 920:
            player_rect.right = 920
    if player_rect.top <= 0:
        player_rect.top = 0
    if player_rect.bottom >= Settings.SCREEN_HEIGHT:
        player_rect.bottom = Settings.SCREEN_HEIGHT
    
    display_surface.blit(player_surface, player_rect)
    pygame.display.update()
    clock.tick(60)
pygame.quit()
    


