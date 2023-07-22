import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

#Creating the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Apex Assault')

#Set framerate
clock = pygame.time.Clock()
FPS = 60

#Player control variables
move_left = False
move_right = False

#Define Colors
BG = (144,201,120)

def draw_Background():
    screen.fill(BG)


class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y,scale,speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        img = pygame.image.load(f'images/{self.char_type}/idle/idle.png')
        self.image = pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def move(self,move_left,move_right):
        #Reset movement variables
        dx = 0
        dy = 0
        
        #Assign movement variables if moving left or right
        if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

player = Soldier('player',200,200,1,5)

#x = 200
#y = 200
#Scale the image
#scale = 1

run = True
#Game loop
while run:

    clock.tick(FPS)
    draw_Background()
    #screen.blit(player.image,player.rect)
    player.draw()
    player.move(move_left,move_right)
    #event loop
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        
        #Keyboard Inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_ESCAPE:
                run = False

        #Keyboard Released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False


    pygame.display.update()

pygame.quit()



