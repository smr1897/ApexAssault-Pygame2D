import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

#Creating the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Apex Assault')

x = 200
y = 200
img = pygame.image.load('images/player/idle/idle.png')
rect = img.get_rect()
rect.center = (x,y)

run = True
#Game loop
while run:

    screen.blit(img,rect)

    #event loop
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()



