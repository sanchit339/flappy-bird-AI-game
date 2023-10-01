import pygame
import neat
import time
import os
import random #for random assign of pipes

WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird1.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird2.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird3.png")))] #array of bird imgs
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bg.png")))

#defining class
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 #ANGLE OF ROTAION 
    ROT_VEL = 20 
    ANIMATION_TIME = 5

    def __init__(self , x , y): #starting position
        self.x = x
        self.y = y
        self.tilt = 0 #initial angle
        self.velocity = 0
        self.tick_count = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0] #initial condition
    
    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.velocity * self.tick_count + 0.5 * self.tick_count**2 # s = ut + (1/2)t^2
        # so to create arc first it will go very up then tick_cnt( time ) will inc . creationg a arc

        #handle out of bound
        if(d >= 16):
            d = 16 
        if(d < 0):
            d -= 2
        
        #update y 
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50 :
            if self.tilt < self.MAX_ROTATION :
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self , win): #window 
        self.img_count += 1

        if(self.img_count < self.ANIMATION_TIME):
            self.img = self.IMGS[0]
        if(self.img_count < self.ANIMATION_TIME * 2):
            self.img = self.IMGS[1]
        if(self.img_count < self.ANIMATION_TIME * 3):
            self.img = self.IMGS[2]
        if(self.img_count < self.ANIMATION_TIME * 4):
            self.img = self.IMGS[1]
        if(self.img_count < self.ANIMATION_TIME * 4 + 1):
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2


        rotate_image = pygame.transform.rotate(self.img , self.tilt)
        new_rect = rotate_image.get_rect(center = self.img.get_rect(topleft = (self.x , self.y)).center) #stackoverflow code
        win.blit(rotate_image , new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img) #surface = self.img

def draw_window(win , bird):
    win.blit(BG_IMG , (0,0)) #render BG img at index 0 , 0
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200 , 200)
    win = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.move()
        draw_window(win , bird)

    pygame.quit()
    quit()

main()



