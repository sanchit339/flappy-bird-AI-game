import pygame
import neat
import time
import os
import random #for random assign of pipes
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird1.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird2.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird3.png")))] #array of bird imgs
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans" , 40)
#defining class
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 #ANGLE OF ROTAION 
    ROT_VEL = 20 
    ANIMATION_TIME = 2

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

        d = self.velocity * self.tick_count + (0.5)*(3)* self.tick_count**2 # s = ut + (1/2)t^2
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

    def draw(self, win):  # window
        self.img_count += 1

        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME * 6:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 6 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotate_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotate_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)  # stackoverflow code
        win.blit(rotate_image, new_rect.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.img) #surface = self.img

class Pipe:
    GAP = 200
    VEL = 5 #velocity towards the bird

    def __init__(self , x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0 # starting co-ordinates
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG , False , True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50 , 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL #we are moving the 
    
    def draw(self , win):
        win.blit(self.PIPE_TOP , (self.x , self.top))
        win.blit(self.PIPE_BOTTOM , (self.x , self.bottom))
    
    def collide(self , bird):
        #we are using the musk function to find collision
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x , self.top - round(bird.y))
        bottom_offset = (self.x - bird.x , self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask , bottom_offset)
        t_point = bird_mask.overlap(top_mask , top_offset)

        if(b_point or t_point):
            return True
        return False

class Base:
    VEL = 5 #same as pipe velocity
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self , y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self , win):
        win.blit(self.IMG , (self.x1 , self.y))
        win.blit(self.IMG , (self.x2 , self.y))


def draw_window(win , bird , pipes , base , score): #the main drawing function
    win.blit(BG_IMG , (0,0)) #render BG img at index 0 , 0
    #on the base image we put all stuf
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score : " + str(score) , 1 , (255 , 255 , 255))
    win.blit(text , (WIN_WIDTH -  text.get_width() - 15 , 15 ))
    
    base.draw(win)
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(230 , 350)
    base = Base(730)
    pipes = [Pipe(600)] #can have multiple pipes
    win = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
    clock = pygame.time.Clock()

    
    score = 0
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            #handle missing pipe 
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe) #push that pipe to remove array
            
            if not pipe.passed and pipe.x < bird.x: #if bird passed the pipe (Logic to add the new pipe)
                pipe.passed = True
                add_pipe = True

            pipe.move()
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730:
            pass
        
        # bird.move()
        base.move()
        draw_window(win , bird , pipes , base , score)

    pygame.quit()
    quit()

main()



