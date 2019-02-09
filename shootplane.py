import pygame
from pygame.locals import *
from sys import exit
from random import randint





class Bullet(pygame.sprite.Sprite):

    def __init__(self, bullet_surface, bullet_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = bullet_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = bullet_init_pos
        self.speed = 8

    def update(self):
        self.rect.top -= self.speed
        if self.rect.top < -self.rect.height:
            self.kill()

            


class Hero(pygame.sprite.Sprite):

    def __init__(self, hero_surface, hero_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = hero_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = hero_init_pos
        self.speed = 6
        self.bullets1 = pygame.sprite.Group()


    def move(self, offset):
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]
        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x

        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y


    def single_shoot(self, bullet1_surface):
        bullet1 = Bullet(bullet1_surface, self.rect.midtop)
        self.bullets1.add(bullet1)




class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy1_surface, enemy_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy1_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos
        self.speed = 2
        self.down_index = 2
        
    def update(self):
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    
        
            
########################

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640


FRAME_RATE = 60


ANIMATE_CYCLE = 30


ticks = 0
clock = pygame.time.Clock()
offset = {pygame.K_LEFT:0, pygame.K_RIGHT:0, pygame.K_UP:0, pygame.K_DOWN:0}



pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('shootplane_demo')




background = pygame.image.load('background.png')


shoot_img = pygame.image.load('bullet.png')



hero_surface = []
hero_surface.append(shoot_img.subsurface(pygame.Rect(0, 99, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(165, 360, 102, 126)))
hero_pos = [200, 500]


bullet1_surface = shoot_img.subsurface(pygame.Rect(1004, 987, 9, 21))


#enemy_img = pygame.image.load('enemy.png')


enemy1_surface = shoot_img.subsurface(pygame.Rect(534, 612, 57, 43))
enemy1_down_surface = []
enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(930, 697, 57, 43)))



hero = Hero(hero_surface[0], hero_pos)


enemy1_group = pygame.sprite.Group()


enemy1_down_group = pygame.sprite.Group()




#########################

while True:


    clock.tick(FRAME_RATE)



    screen.blit(background, (0, 0))


    

    if ticks >= ANIMATE_CYCLE:
        ticks = 0
    hero.image = hero_surface[ticks//(ANIMATE_CYCLE//2)]

    screen.blit(hero.image, hero.rect)



    if ticks % 10 == 0:
        hero.single_shoot(bullet1_surface)

    hero.bullets1.update()

    hero.bullets1.draw(screen)



    if ticks % 30 == 0:
        enemy = Enemy(enemy1_surface, [randint(0, SCREEN_WIDTH - enemy1_surface.get_width()),
        -enemy1_surface.get_height()])

        enemy1_group.add(enemy)

    enemy1_group.update()

    enemy1_group.draw(screen)


    enemy1_down_group.add(pygame.sprite.groupcollide(enemy1_group, hero.bullets1, True, True))
    
    for enemy1_down in enemy1_down_group:
        screen.blit(enemy1_down_surface[enemy1_down.down_index], enemy1_down.rect)
        if ticks % (ANIMATE_CYCLE//2) == 0:
            if enemy1_down.down_index < 3:
                enemy1_down.down_index += 1
            else:
                enemy1_down_group.remove(enemy1_down)


                
    ticks += 1


    pygame.display.update()


    
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()



        if event.type == pygame.KEYDOWN:
            if event.key in offset:
                offset[event.key] = hero.speed
        elif event.type == pygame.KEYUP:
                if event.key in offset:
                    offset[event.key] = 0


                


    hero.move(offset)
    
                
   

    
            

