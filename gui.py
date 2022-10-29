import pygame

WIDTH = 500
HEIGHT = 750

palette = {
    "green" : (83,141,78),
    "yellow" : (181,159,59),
    "gray" : (58,58,60),
    "white" : (215,218,220),
    "black" : (18,18,19),
}

# Set up the drawing window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Run until the user asks to quit
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Fill the background with black
    screen.fill(palette["black"])

    pygame.draw.rect(screen, palette["gray"], (0,0,100,100))
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()