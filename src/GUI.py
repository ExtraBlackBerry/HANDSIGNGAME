import pygame

# Setup
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Seal Strike - Main Menu")

clock = pygame.time.Clock()
running = True
delta_time = 0

# Colours
COLOR_BACKGROUND = (34,30,32,255)
COLOR_BUTTON = (58, 51, 120)
COLOR_TEXT = (255, 255, 255)
COLOR_PLAYER_BOX = (0, 255, 0)
COLOR_ENEMY_BOX = (255, 0, 0)
COLOR_HEALTH_BAR= (255, 0, 0)

# Fonts
# Get ttf file for fonts

if __name__ == "__main__":
    # Main Loop
    while running:
        
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                

        screen.fill(COLOR_BACKGROUND) # Clear frame
        
        # Rendering
        
        # Controls
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]: # Example w key
        
        pygame.display.flip() # Update Frame
        delta_time = clock.tick(60) / 1000

    pygame.quit()

