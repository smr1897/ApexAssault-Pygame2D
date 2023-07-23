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

#Game Variables
GRAVITY = 0.75

#Player control variables
move_left = False
move_right = False

#Define Colors
BG = (144,201,120)
RED = (255,0,0)

def draw_Background():
    screen.fill(BG)
    pygame.draw.line(screen,RED,(0,300),(SCREEN_WIDTH,300))

class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y,scale,speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.velocity_y = 0
        self.jump = False
        self.flip = False

        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        #Load all images for the players
        animation_types = ['idle','run']
        for animation in animation_types:
            temp_list = []
            for i in range(5):
                img = pygame.image.load(f'images/{self.char_type}/idle/{i}.png')
                img = pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))        
                temp_list.append(img)
            #Now self.animation_list becomes a list of lists    
            self.animation_list.append(temp_list)

            # temp_list = []
            # for i in range(8):
            #     img = pygame.image.load(f'images/{self.char_type}/run/{i}.png')
            #     img = pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))
            #     temp_list.append(img)
            # self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]     
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

        #Jump
        if self.jump == True:
            self.velocity_y = -11
            self.jump = False

        #Apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > 10:
            self.velocity_y
        dy += self.velocity_y

        #Check for collision
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom

        #Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self): 
        ANIMATION_COOLDOWN = 100

        self.image = self.animation_list[self.action][self.frame_index] 

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        #if the animation has run out again back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self,new_action):
        #Check if the new action is different than the prevoius one
        if new_action != self.action:
            self.action = new_action
            #Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

player = Soldier('player',200,200,1,5)
#enemy = Soldier('enemy',400,200,1,5)

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
    player.update_animation()
    player.draw()
    
    #enemy.draw()

    #Update player actions
    if player.alive:
        if move_left or move_right:
            player.update_action(1)
        else:
            player.update_action(0)

        player.move(move_left,move_right)
    #event loop
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        
        #Keyboard Inputs
        if event.type == pygame.KEYDOWN:
            #move left
            if event.key == pygame.K_a:
                move_left = True
            #move right
            if event.key == pygame.K_d:
                move_right = True
            #jump
            if event.key == pygame.K_w:
                player.jump = True
            #quit game
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



