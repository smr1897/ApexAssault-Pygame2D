import pygame
import os

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
shoot = False
grenade = False
grenade_thrown = False

bullet_img = pygame.image.load('images/bullet/bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img,(bullet_img.get_width()//3,bullet_img.get_height()//3))

grenade_img = pygame.image.load('images/grenade/grenade.png').convert_alpha()
grenade_img = pygame.transform.scale(grenade_img,(grenade_img.get_width()//1.5,grenade_img.get_height()//1.5))



#Define Colors
BG = (144,201,120)
RED = (255,0,0)

def draw_Background():
    screen.fill(BG)
    pygame.draw.line(screen,RED,(0,300),(SCREEN_WIDTH,300))

class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y,scale,speed,ammo,grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.shoot_timeout = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.ammo = ammo
        self.start_ammo = ammo
        self.velocity_y = 0
        self.jump = False
        self.in_air = True
        #self.shooting = False
        self.flip = False

        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        #Load all images for the players
        animation_types = ['idle','run','jump','shoot','Death']
        for animation in animation_types:
            temp_list = []

            #Count number of files in the folder
            num_of_frames = len(os.listdir(f'images/{self.char_type}/{animation}'))

            for i in range(num_of_frames):
                img = pygame.image.load(f'images/{self.char_type}/{animation}/{i}.png').convert_alpha()
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

    def update(self):

        self.update_animation()
        self.check_dead()
        #Update shooting timeout
        if self.shoot_timeout > 0:
            self.shoot_timeout -= 1

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
        if self.jump == True and self.in_air == False:
            self.velocity_y = -11
            self.jump = False
            self.in_air = True

        #Apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > 10:
            self.velocity_y
        dy += self.velocity_y

        #Check for collision
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        #Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_timeout == 0 and self.ammo > 0:
            self.shoot_timeout = 20
            bullet = Bullet(self.rect.centerx +(0.5*self.rect.size[0]*self.direction), self.rect.centery+(self.rect.height)/4,self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
        

    def update_animation(self): 
        ANIMATION_COOLDOWN = 200

        self.image = self.animation_list[self.action][self.frame_index] 

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        #if the animation has run out again back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action])-1
            else:    
                self.frame_index = 0

    def update_action(self,new_action):
        #Check if the new action is different than the prevoius one
        if new_action != self.action:
            self.action = new_action
            #Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_dead(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(4)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        if pygame.sprite.spritecollide(player,bullet_group,False):
            if player.alive:
                self.kill()
                player.health -= 5
        
        if pygame.sprite.spritecollide(enemy,bullet_group,False):
            if enemy.alive:
                self.kill()
                enemy.health -= 25

        # bullet_group.add(self)
        
class Grenade(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.velocity_y = -10
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        self.velocity_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.velocity_y 

        #Check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0
             

        #Check collision with walls
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        self.rect.x += dx
        self.rect.y += dy 

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.velocity_y = -10
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        

#Creating a sprite group for bullets 
bullet_group = pygame.sprite.Group() 
grenade_group = pygame.sprite.Group()

player = Soldier('player',200,200,0.8,5,20,5)
enemy = Soldier('enemy',400,200,0.8,5,20,0)

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
    player.update()
    player.draw()
    
    enemy.update()
    enemy.draw()

    #Draw Bullets
    bullet_group.update()
    bullet_group.draw(screen)
    grenade_group.update()
    grenade_group.draw(screen) 

    #Update player actions
    if player.alive:

        if shoot:
            # bullet = Bullet(player.rect.centerx +(0.28*player.rect.size[0]*player.direction), player.rect.centery+(player.rect.height)/4,player.direction)
            # bullet_group.add(bullet)
            player.shoot()
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx+(0.2 * player.rect.size[0] * player.direction),player.rect.centery,player.direction)
            grenade_group.add(grenade)
            grenade_thrown = True
            player.grenades -= 1

        if player.in_air:
            player.update_action(2)

        elif move_left or move_right:
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
            #shoot bullets
            if event.key == pygame.K_SPACE:
                shoot = True
                player.update_action(3)
            #Thorow grenade
            if event.key == pygame.K_q:
                grenade = True
            #quit game
            if event.key == pygame.K_ESCAPE:
                run = False

        #Keyboard Released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False


    pygame.display.update()

pygame.quit()



