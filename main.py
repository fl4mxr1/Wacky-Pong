import pygame
import ui as UI

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")

# Initialize the UI system
UI.init(screen)

# Create some UI elements
test_button = UI.Button("Click Me!", size=20, x=400, y=300, align="center", bg_color=(50, 50, 50))

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    screen.fill((0, 0, 0))  # Fill with black
    
    # Render UI
    UI.render_ui()
    
    # Update the display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(60)

pygame.quit() 