import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

#Creating the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Apex Assault')

class Soldier(pygame.sprite.Sprite):
    def __init__(self,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/player/idle/idle.png')
        #img = pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))
        rect = img.get_rect()
        rect.center = (x,y)


x = 200
y = 200
#Scale the image
scale = 2

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



