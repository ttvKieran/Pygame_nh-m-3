import pygame
import sys
import csv
pygame.init()
screen_width = 1400
screen_height = 787
level = 0
ROWS = 16
COLS = 150
TILE_SIZE = screen_height // ROWS
TILE_TYPES = 21
scroll = 200
screen_scroll = 0
bg_scroll = 0
#load images
bg_surface = pygame.transform.scale(pygame.image.load('Pygame_nh-m-3/asset2/background2.png'), (1400, 787))
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Pygame_nh-m-3/asset2/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Character Animation")
clock = pygame.time.Clock()
#define player action variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False
def draw_bg():
    screen.fill('#89A477')
    width = bg_surface.get_width()
    for x in range(3):
        screen.blit(bg_surface, ((x*width - bg_scroll*0.5), 0))
    
class Character(pygame.sprite.Sprite):
    def __init__(self, char, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char = char
        self.scale = scale
        self.speed = speed
        self.direction = 1 #right
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(1):
            img = pygame.image.load(f'Pygame_nh-m-3/{self.char}/player{i + 1}.png').convert_alpha()
            self.imgage = pygame.transform.scale(img, (int(img.get_width()*self.scale), int(img.get_height() * self.scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(2):
            img = pygame.image.load(f'Pygame_nh-m-3/{self.char}/player{i + 6}.png').convert_alpha()
            imgage = pygame.transform.scale(img, (int(img.get_width()*self.scale), int(img.get_height() * self.scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.imgage = self.animation_list[self.action][self.frame_index]
        self.rect = self.imgage.get_rect(center = (x, y))
        self.width = self.imgage.get_width()
        self.height = self.imgage.get_height()
    
    def update_animation(self):
        ANIMATION_COOLDOWN = 200
        self.imgage = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
    
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def update(self):
        self.update_animation()
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.imgage, self.flip, False),self.rect)
        
    def move(self, moving_left, moving_right, moving_up, moving_down):
        screen_scroll = 0
        dx = 0
        dy = 0
        if moving_left:
            dx -= self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx += self.speed
            self.flip = False
            self.direction = 1 
        if moving_up:
            dy -= self.speed
            self.direction = -1
        if moving_down:
            dy += self.speed
            self.direction = 1  
        #check for collision
        for tile in world.obstancle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0
        self.rect.x += dx
        self.rect.y += dy 
        if (self.rect.right > screen_width - scroll and bg_scroll < (world.level_length * TILE_SIZE - 300) - screen_width) or (self.rect.right < scroll and (self.direction == -1 or moving_down or moving_up) and bg_scroll > abs(dx)):
            self.rect.x -= dx
            screen_scroll = -dx
        return screen_scroll
            
class World():
    def __init__(self):
        self.obstancle_list = []
        self.tile_list = []
    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                img = img_list[tile]
                img_rect = img.get_rect()
                img_rect.x = x * TILE_SIZE
                img_rect.y = y * TILE_SIZE
                tile_data = (img, img_rect)
                if tile == 16:
                    self.obstancle_list.append(tile_data)
                elif tile == 15:
                    player = Character('player_down', x*TILE_SIZE, y*TILE_SIZE, 1, 5)  
                else:
                    self.tile_list.append(tile_data)
        return player
    def draw(self):
        for tile in self.obstancle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
        for tile in self.tile_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
                      

world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player = world.process_data(world_data)       

run = True
while run:
    clock.tick(60)
    draw_bg()
    world.draw()
    player.update()
    player.draw()
    print(player.rect.left)
    if player.alive:
        if moving_left or moving_right or moving_down or moving_up:
            player.update_action(1) #1: run
        else:
            player.update_action(0) #0: idle
        screen_scroll = player.move(moving_left, moving_right, moving_up, moving_down)
        bg_scroll -= screen_scroll
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False
            if event.key == pygame.K_ESCAPE:
                run = False
        if player.rect.top <= 0:
            player.rect.top = 0
            moving_up = False
        if player.rect.bottom >= screen_height:
            player.rect.bottom = screen_height
            moving_down = False
    pygame.display.update()
pygame.quit()
sys.exit()