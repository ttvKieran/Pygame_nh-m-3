import pygame
import sys
import csv
import os
import button
import Zombie_game.Zombie_game as Z

pygame.init()

screen_width = 1400
screen_height = 780

# Global variables
run = True
level = 1
start_game = False
ROWS = 16
COLS = 29
TILE_SIZE = screen_height // ROWS
TILE_TYPES = 21
scroll = 200
screen_scroll = 0
bg_scroll = 0
isdie = True
#Display and asset info

bg_musicHome = pygame.mixer.Sound('Sound/cottagecore-17463.mp3')
hit_sound = pygame.mixer.Sound('Sound/sound bắn trúg zombie.mp3')
bg_music = pygame.mixer.Sound('Sound/nền.mp3')
shot_music = pygame.mixer.Sound('Sound/tiếng súng .mp3')
start_music = pygame.mixer.Sound('Sound/fight khi start game.mp3')
died_music = pygame.mixer.Sound('Sound/Mình chết.mp3')

bg_music.set_volume(0.1)
bg_musicHome.set_volume(0.4)
shot_music.set_volume(0.2)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ngoi truong xac song")
clock = pygame.time.Clock()


#Load images

#Button images
start_img = pygame.transform.scale(pygame.image.load('asset2/start.png').convert_alpha(), (200, 111))
exit_img = pygame.transform.scale(pygame.image.load('asset2/exit.png'), (200, 111))
resume_img = pygame.transform.scale(pygame.image.load('asset2/resume.png'), (200, 111))
restart_img = pygame.transform.scale(pygame.image.load('asset2/restart.png'), (200, 111))
board_img = pygame.transform.scale(pygame.image.load('asset2/board.png'), (1200, 635))
menu_img = pygame.transform.scale(pygame.image.load('asset2/menu.png'), (200, 111))

#Background images
bg_surface = pygame.transform.scale(pygame.image.load('asset2/background13.png'), (1400, 787))
heart_img = pygame.transform.scale(pygame.image.load('asset2/green.png'), (30, 60))
heart_rect = heart_img.get_rect(center = (25, 28))
bg_img = pygame.transform.scale(pygame.image.load('asset2/background11.png'), (1400, 787))
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'asset2/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
    
# #define fonts
# font = pygame.font.SysFont('arialblack', 40)
# def draw_text(text, font, text_col, x, y):
#     img = font.render(text, True, text_col)
#     screen.blit(img, (x, y))


#define player action variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False
attacking = False

def draw_bg():
    screen.fill('#89A477')
    screen.blit(bg_surface, (0, 0))
    screen.blit(heart_img, heart_rect)
    
def reset_level():
    data = []
    for row in range(ROWS + 1):
        r = [-1] * COLS
        data.append(r)
    return data

class Character(pygame.sprite.Sprite):
    def __init__(self, char, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.awin = False
        self.char = char
        self.scale = scale
        self.speed = speed
        self.direction = 1 
        self.flip = False
        self.frame_index = 0
        self.animation_list = []
        self.action = 0
        self.health = 100
        self.max_health = self.health
        self.update_time = pygame.time.get_ticks()
        #load all images for the player
        animation_types = ['left', 'right', 'up', 'down']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'player_{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'player_{animation}/{animation}_{i + 1}.png').convert_alpha()
                img = pygame.transform.scale(img, (40, 80))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.imgage = self.animation_list[self.action][self.frame_index]
        self.rect = self.imgage.get_rect(center = (x, y))
        self.x = x
        self.y = y
        self.width = self.imgage.get_width()
        self.height = self.imgage.get_height()

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
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
        self.check_alive()
    
    def draw(self):
        if self.action != -1: screen.blit(self.imgage ,self.rect)
        else: 
            screen.blit(pygame.transform.scale(pygame.image.load('player_down/down_2.png').convert_alpha(), (40, 80)), self.rect)
    def move(self, moving_left, moving_right, moving_up, moving_down):
        screen_scroll = 0
        dx = 0
        dy = 0
        if moving_left:
            dx -= self.speed
            self.direction = -1
        if moving_right:
            dx += self.speed
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
        self.x += dx
        self.y += dy
        if (self.rect.right > screen_width - scroll and bg_scroll < (world.level_length * TILE_SIZE - 300) - screen_width) or (self.rect.right < scroll and (self.direction == -1 or moving_down or moving_up) and bg_scroll > abs(dx)):
            self.rect.x -= dx
            screen_scroll = -dx
        return screen_scroll
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            
            
class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health
	def draw(self, health):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(screen, 'BLACK', (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(screen, 'RED', (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, 'GREEN', (self.x, self.y, 150 * ratio, 20))
        
        
#Creat map     
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
                    player = Character('player_img', 80, 680, 1, 5)  
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
                       
#get data from excel
world_data = []
for row in range(ROWS + 1):
	r = [-1] * COLS
	world_data.append(r)
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
            
#creat buttons
start_button = button.Button(screen_width // 2 - 100, screen_height // 2 - 300, start_img, 1)
exit_button = button.Button(screen_width // 2 - 100, screen_height // 2 - 150, exit_img, 1)
restart_button = button.Button(screen_width // 2 - 100, screen_height // 2 - 150, restart_img, 1)
menu_button = button.Button(screen_width // 2 - 100, screen_height // 2 - 300, menu_img, 1)

#Create objects
world = World()
player = world.process_data(world_data)
enemy1 = Z.Enemy(161, 173, 75, 75, 'Zombies/Baby Zombie.png', 3, 5)
enemy2 = Z.Enemy(1292, 121, 75, 75, 'Zombies/Boy Zombie.png', 3, 5)
enemy3 = Z.Enemy(1306, 611, 75, 75, 'Zombies/Baby Zombie.png', 3, 5)
# enemy = Z.Enemy(600, 370, 75, 75, 'Zombies/Bald Zombie.png', 2, 5)
# enemy = Z.Enemy(600, 370, 75, 75, 'Zombies/Baby Zombie.png', 2, 5)
target=Z.Object(0,0,50,50,pygame.image.load("player_bullet/tam.png"))
health_bar = HealthBar(10, 10, player.health, player.health)
bullets = []

def shoot():
    player_center =player.rect.center
    bullet=Z.Object(player_center[0]-15,player_center[1]-17,30,34,pygame.image.load("player_bullet/bullet_red.png"))
    target_center=target.get_center()
    bullet.velocity=pygame.math.Vector2(target_center[0]-player_center[0],target_center[1]-player_center[1])
    bullet.velocity.normalize_ip()
    bullet.velocity*=6
    bullets.append(bullet)


while run:
    clock.tick(60)
    
    if start_game == False:
        bg_music.stop()
        bg_musicHome.play(loops = -1, fade_ms = 5)
        screen.blit(bg_img, (0, 0))
        if start_button.draw(screen):
            bg_musicHome.stop()
            start_music.play()
            start_game = True
        if exit_button.draw(screen):
            run = False
    else:
        if player.alive:
            pygame.mouse.set_visible(False)
        bg_music.play(loops = -1, fade_ms = 3)  
        world.draw()
        draw_bg()
        health_bar.draw(player.health)
        player.update()
        player.draw()
        for obj in Z.objects:
            if (type(obj)==Z.Enemy):
                obj.update(player)
            else:
                obj.update()
        for e in Z.enemies:
            if pygame.Rect.colliderect(e.image_rect,player.rect)==True:
                player.health-=1
                if player.health<=0:
                    player.alive=False
                continue      
            for b in bullets:
               if pygame.Rect.colliderect(e.image_rect,b.image_rect)==True:
                    e.take_damage(1)
                    bullets.remove(b)
                    Z.objects.remove(b)     
        for p in Z.particles:
            p.image.set_alpha(p.image.get_alpha()-1)
            if p.image.get_alpha()==0:
                Z.objects.remove(p)
                Z.particles.remove(p)
                continue
            Z.objects.remove(p)
            Z.objects.insert(0,p)
 

        if player.alive:
            isdie = True
            bg_musicHome.stop()
            if moving_up:
                player.update_action(2)
            elif moving_down:
                player.update_action(3)
            elif moving_left:
                player.update_action(0) 
            elif moving_right:
                player.update_action(1) 
            else: player.action = -1
            screen_scroll = player.move(moving_left, moving_right, moving_up, moving_down)
            bg_scroll -= screen_scroll
        else:
            # pygame.mouse.set_visible(True)
            bg_music.stop()
            if isdie:
                died_music.play()
                isdie = False
            bg_musicHome.play(loops = -1, fade_ms = 5)
            screen.blit(bg_img, (0, 0))
            screen_scroll = 0
            #button restart
            if restart_button.draw(screen):
                player.alive = True
                player.health = 100
                world_data = reset_level()
                player.health = 100
                #restart map
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player = world.process_data(world_data)
            #button menu
            if menu_button.draw(screen):
                player.alive = True
                player.health = 100
                world_data = reset_level()
                player.health = 100
                #restart map
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player = world.process_data(world_data)
                start_game = False  #Go to menu
                
        mousePos=pygame.mouse.get_pos()
        target.x=mousePos[0]-target.width//2
        target.y=mousePos[1]-target.height//2
        if player.alive == False:
            pygame.mouse.set_visible(True)
            pygame.display.update()
    #Even game            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if player.alive:
            if event.type == pygame.MOUSEBUTTONDOWN:
                bg_music.stop()
                shot_music.play()
                bg_music.play(loops = -1, fade_ms = 5)
                shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_UP:
                moving_up = True
            if event.key == pygame.K_DOWN:
                moving_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_UP:
                moving_up = False
            if event.key == pygame.K_DOWN:
                moving_down = False
            if event.key == pygame.K_ESCAPE:
                run = False
    #draw_text('Press SPACE to pause', font, 'White', 100, 250)
    pygame.display.update()
    
    
pygame.quit()
sys.exit()