import pygame
pygame.init()

class Player:
    def __init__(self, x, y, speed, image_paths, max_health):
        self.rect = pygame.Rect(x, y, 0, 0)
        self.speed = speed
        self.image_paths = image_paths
        self.current_index = 0
        self.current_image = pygame.image.load(self.image_paths[self.current_index])
        self.health = max_health
        self.max_health = max_health

    def update(self, key_presses):
        self.rect.x += self.speed * (key_presses[pygame.K_RIGHT] - key_presses[pygame.K_LEFT])
        self.rect.y += self.speed * (key_presses[pygame.K_DOWN] - key_presses[pygame.K_UP])

        if key_presses[pygame.K_UP]:
            self.image_paths = up_image_paths
        elif key_presses[pygame.K_DOWN]:
            self.image_paths = down_image_paths
        elif key_presses[pygame.K_LEFT]:
            self.image_paths = left_image_paths
        elif key_presses[pygame.K_RIGHT]:
            self.image_paths = right_image_paths
        else:
            self.image_paths = [idle_image_path]
            self.current_index = 0  # Reset current_index when the idle image is selected

    def animate(self):
        if frame_count >= frame_delay:
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

# Đường dẫn đến các hình ảnh
idle_image_path = 'player_down/down_2.png'
up_image_paths = ['player_up/up_1.png', 'player_up/up_2.png', 'player_up/up_3.png']
down_image_paths = ['player_down/down_1.png', 'player_down/down_2.png', 'player_down/down_3.png']
left_image_paths = ['player_move/left_1.png', 'player_move/left_2.png', 'player_move/left_1.png']
right_image_paths = ['player_move/right_1.png', 'player_move/right_2.png', 'player_move/right_1.png']

# Initialize the player
player = Player(100, 100, 5, down_image_paths, max_health=100)

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

    if frame_count >= frame_delay:
        if player.animate():
            frame_count = 0  # Reset frame count

    screen.fill((0, 0, 0))
    player.draw_health_bar()
    screen.blit(player.current_image, player.rect)

    pygame.display.flip()

    frame_count += 1

    clock.tick(fps)
