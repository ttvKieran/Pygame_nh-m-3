import pygame
pygame.init()

screen_size = (1400, 787)
screen = pygame.display.set_mode(screen_size)

# Đường dẫn đến các hình ảnh
idle_image = 'player_down/down_mid.png'
up_images = ['player_up/up_left.png', 'player_up/up_mid.png', 'player_up/up_right.png']
down_images = ['player_down/down_left.png', 'player_down/down_mid.png', 'player_down/down_right.png']
left_images = ['player_move/left_1.png', 'player_move/left_2.png', 'player_move/left_1.png']
right_images = ['player_move/right_1.png', 'player_move/right_2.png', 'player_move/right_1.png']

# Load tất cả hình ảnh vào pygame
idle_image = pygame.image.load(idle_image)
up_images = [pygame.image.load(image) for image in up_images]
down_images = [pygame.image.load(image) for image in down_images]
left_images = [pygame.image.load(image) for image in left_images]
right_images = [pygame.image.load(image) for image in right_images]

# Một số thuộc tính của game
fps = 60
frame_count = 0
frame_delay = 10
current_index = 0
current_images = down_images  # Ảnh mặc định
current_image = current_images[current_index]
player_rect = current_image.get_rect()
speed = 5  # Tốc độ của nhân vật

clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    key_presses = pygame.key.get_pressed()

    # Cập nhật vị trí của nhân vật dựa trên sự kiện nhấn phím
    player_rect.x += speed * (key_presses[pygame.K_RIGHT] - key_presses[pygame.K_LEFT])
    player_rect.y += speed * (key_presses[pygame.K_DOWN] - key_presses[pygame.K_UP])

    if key_presses[pygame.K_UP]:
        current_images = up_images
    elif key_presses[pygame.K_DOWN]:
        current_images = down_images
    elif key_presses[pygame.K_LEFT]:
        current_images = left_images
    elif key_presses[pygame.K_RIGHT]:
        current_images = right_images
    else:
        current_images = [idle_image]
        current_index = 0  # Reset current_index khi ảnh idle được chọn

    if frame_count >= frame_delay:
        current_index = (current_index + 1) % len(current_images)
        current_image = current_images[current_index]
        frame_count = 0  # Reset frame count

    screen.fill((0, 0, 0))
    screen.blit(current_image, player_rect)

    pygame.display.flip()

    frame_count += 1

    clock.tick(fps)