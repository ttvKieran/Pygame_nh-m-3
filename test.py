import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Character Animation")

# Load player images for animation
player_images = [pygame.image.load(f'player{i}.png') for i in range(1, 13)]  # Load 12 images player1.png, player2.png, ..., player12.png
player_index = 0  # Index to track the current player image

# Player attributes
player_width, player_height = 64, 64
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_vel = 1
is_jumping = False
jump_count = 10
jump_vel = 5
moving_left = False
moving_right = False
clock = pygame.time.Clock()  # Create a clock to control the frame rate

def draw_window():
    screen.fill((255, 255, 255))  # Fill the screen with white color
    # Draw the player image to the screen
    player_img = player_images[player_index]
    screen.blit(player_img, (player_x, player_y))
    pygame.display.update()  # Update the display

# Main loop
run = True
while run:
    clock.tick(10)  # Set the frame rate (10 frames per second)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    # Animation control
    if keys[pygame.K_LEFT] and player_x - player_vel > 0:
        player_x -= player_vel
        moving_left = True
        moving_right = False
    elif keys[pygame.K_RIGHT] and player_x + player_vel < screen_width - player_width:
        player_x += player_vel
        moving_left = False
        moving_right = True
    else:
        moving_left = False
        moving_right = False

    if player_index < 11:
        player_index += 1
    else:
        player_index = 0

    # Handle jumping
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg * jump_vel
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    draw_window()  # Update the display

pygame.quit()  # Quit the game
sys.exit()