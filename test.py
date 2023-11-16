import pygame
import os

# Khai báo các hằng số
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 787
WHITE = (255, 255, 255)
FPS = 60

# Khởi tạo Pygame
pygame.init()

# Tạo cửa sổ trò chơi

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Animation Example")
bg=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
player=pygame.image.load('player_down/down_mid.png')
player_rect=player.get_rect(center=(SCREEN_WIDTH*0.5,SCREEN_HEIGHT*0.5))


running = True
clock = pygame.time.Clock()
speed=7
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.x>= speed:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT] and player_rect.x<=SCREEN_WIDTH:
        player_rect.x += speed
    if keys[pygame.K_UP]and player_rect.y>=speed:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]and player_rect.y<=SCREEN_HEIGHT:
        player_rect.y += speed

    screen.fill((0, 0, 0))
    screen.blit(player, player_rect)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()