import pygame
pygame.init()

class Player:
    def __init__(self, x, y, speed, image_paths, max_health):
        
        self.speed = speed
        self.image_paths = image_paths
        self.current_index = 0
        self.current_image = pygame.image.load(self.image_paths[self.current_index])
        self.health = max_health
        self.max_health = max_health
        self.rect = pygame.Rect(x, y, self.current_image.get_width(), self.current_image.get_height())
        # Thêm các biến mới
        self.is_attacking = False
        self.attack_frame_count = 0
        self.attack_delay = 100  # Độ trễ giữa các cú đánh
        self.attack_duration = 30   # Thời gian hiển thị mỗi cú đánh

    def update(self, key_presses):
        self.rect.x += self.speed * (key_presses[pygame.K_RIGHT] - key_presses[pygame.K_LEFT])
        self.rect.y += self.speed * (key_presses[pygame.K_DOWN] - key_presses[pygame.K_UP])

        if key_presses[pygame.K_UP]:
            self.image_paths = up_image_paths
            self.is_attacking = False  # Không đánh khi di chuyển lên
        elif key_presses[pygame.K_DOWN]:
            self.image_paths = down_image_paths
            self.is_attacking = False  # Không đánh khi di chuyển xuống
        elif key_presses[pygame.K_LEFT]:
            self.image_paths = left_image_paths
            self.is_attacking = False  # Không đánh khi di chuyển sang trái
        elif key_presses[pygame.K_RIGHT]:
            self.image_paths = right_image_paths
            self.is_attacking = False  # Không đánh khi di chuyển sang phải
        else:
            self.image_paths = [idle_image_path]
            self.is_attacking = key_presses[pygame.K_SPACE]  # Đánh khi ở trạng thái đứng yên và nhấn Space

        # Xử lý sự kiện đánh   
        if self.is_attacking:
            self.attack_frame_count += 1 
            if self.attack_frame_count <= self.attack_duration:
                # Hiển thị animation đánh khi nhấn Space
                self.current_image = pygame.image.load(image_attack[self.attack_frame_count % len(image_attack)])
            else:
                # Kết thúc cú đánh, reset các biến liên quan
                self.is_attacking = False
                self.attack_frame_count = 0
                self.current_image = pygame.image.load(self.image_paths[self.current_index]).convert_alpha()
                self.current_index = 0  # Reset current_index when the idle image is selected
    def animate(self):
        if frame_count >= frame_delay:
            # Hiển thị animation bình thường
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.current_image = pygame.image.load(self.image_paths[self.current_index])
            return True  # Animation frame changed
        return False  # Animation frame not changed

    def draw_health_bar(self):
        health_bar_width = 50
        health_ratio = max(0, self.health / self.max_health)
        health_bar_height = 5
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, health_bar_height))

class Enemy:
    def __init__(self, x, y, speed, image_path, max_health):
        
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.health = max_health
        self.max_health = max_health
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
    def update(self, player_rect):
        dx = player_rect.x - self.rect.x
        dy = player_rect.y - self.rect.y
        distance = ((dx ** 2) + (dy ** 2)) ** 0.5
        if distance > 0:
            self.rect.x += self.speed * (dx / distance)
            self.rect.y += self.speed * (dy / distance)

    def draw_health_bar(self):
        health_bar_width = 50
        health_ratio = max(0, self.health / self.max_health)
        health_bar_height = 5
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, health_bar_height))

# Đường dẫn đến các hình ảnh
idle_image_path = 'player_attack/att1.png'
up_image_paths = ['player_up/up_1.png', 'player_up/up_2.png', 'player_up/up_3.png']
down_image_paths = ['player_down/down_1.png', 'player_down/down_2.png', 'player_down/down_3.png']
left_image_paths = ['player_move/left_1.png', 'player_move/left_2.png', 'player_move/left_1.png']
right_image_paths = ['player_move/right_1.png', 'player_move/right_2.png', 'player_move/right_1.png']
image_attack = ['player_attack/att1.png','player_attack/att2.png','player_attack/att3.png']

# Initialize the player
player = Player(100, 100, 5, down_image_paths, max_health=100)

# Initialize an enemy
enemy = Enemy(700, 700, 2, 'player_down/down_2.png', max_health=50) 
 
screen_size = (1400, 787)
screen = pygame.display.set_mode(screen_size)

fps = 60
frame_count = 0
frame_delay = 10

clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    key_presses = pygame.key.get_pressed()

    player.update(key_presses)
    enemy.update(player.rect)
    if frame_count >= frame_delay:
        if player.animate():
            frame_count = 0  # Reset frame count

    # Check for collision (simple rectangle collision)
    print(player.rect, enemy.rect)
    print(player.rect.colliderect(enemy.rect))
    if pygame.Rect.colliderect(enemy.rect, player.rect):
        player.health -= 0.1
        enemy.health -= 0.5
    print(player.health, enemy.health)
    # Draw on the screen
    screen.fill((0, 0, 0))
    player.draw_health_bar()
    enemy.draw_health_bar()
    screen.blit(player.current_image, player.rect)
    screen.blit(enemy.image, enemy.rect)

    # Check if player or enemy health reaches zero
    if player.health <= 0:
        print("Game Over - Player defeated!")
        pygame.quit()
        break

    if enemy.health <= 0:
        print("Game Over - Enemy defeated!")
        pygame.quit()
        break

    pygame.display.flip()

    frame_count += 1

    clock.tick(fps)
