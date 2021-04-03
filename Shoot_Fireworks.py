import pygame
import math
from random import randint,uniform

vector = pygame.math.Vector2
gravity = vector(0,0.35)
Heigh = 500
Width = 700
trail_colors = [(45, 45, 45), (60, 60, 60), (75, 75, 75), (125, 125, 125), (150, 150, 150)]

class Trail:
    def __init__(self, n, size):
        self.npos = n
        self.size = int(size - n/2)
        if(self.size<0):
            self.size=0
        self.pos =(-10,-10)
        self.color = trail_colors[n]
    def set_pos(self, x, y):
        self.pos = vector(x,y)
    def show(self,win):
        pygame.draw.circle(win,self.color,(int(self.pos.x),int(self.pos.y)),self.size)
class Particle:
    def __init__(self, x, y,firework, color):
        self.firework = firework
        self.pos = vector(x,y)
        self.origin = vector(x,y)
        self.color = color
        self.radius = 20
        self.exploded_radius = randint(15,20)
        self.exploded = False
        self.remove = False
        
        self.trails = []
        self.pre_posx = [-10]*10 
        self.pre_posy = [-10]*10 
        
        if(self.firework):
            self.move_vector = vector(0,-randint(15,20))
            self.size = 5
            self.color = color
            for i in range(5):
                self.trails.append(Trail(i,self.size))
        else:
            self.move_vector = vector(uniform(-1,1),uniform(-1,1))
            self.move_vector.x*=randint(20,30)
            self.move_vector.y*=randint(20,30)
            self.size = randint(2,4)
            for i in range(5):
                self.trails.append(Trail(i,self.size))
    def trail_update(self):
        self.pre_posx.pop()
        self.pre_posy.pop()
        self.pre_posx.insert(0,self.pos.x)
        self.pre_posy.insert(0,self.pos.y)

        for n,t in enumerate(self.trails):
            self.trails[n].set_pos(self.pre_posx[n],self.pre_posy[n])
    def move(self):
        if not self.firework:
            self.move_vector.x*=0.8
            self.move_vector.y*=0.8
        
        self.move_vector += gravity
        self.pos += self.move_vector

        if not self.firework:
            distance = math.sqrt((self.pos.x-self.origin.x) ** 2 + (self.pos.y-self.origin.y)**2 )
            if(distance > self.exploded_radius):
                self.remove = True

        self.trail_update()
    def show(self,win):
        pygame.draw.circle(win,self.color,(self.pos.x,self.pos.y),self.size)
class Firework:
    def __init__(self):
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.colors = (
        (randint(0, 255), randint(0, 255), randint(0, 255)), (randint(0, 255), randint(0, 255), randint(0, 255)),
        (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.firework = Particle(randint(0,Width),Heigh,True,self.color)
        self.particles = []
        self.exploded = False
        self.nParticles = vector(100,255)

    def show(self, win):
        pygame.draw.circle(win,self.color,(self.firework.pos.x,self.firework.pos.y),self.firework.size)
    def explode(self):
        self.firework.exploded=True
        num = randint(self.nParticles.x,self.nParticles.y)
        for i in range(num):
            self.particles.append(Particle(self.firework.pos.x,self.firework.pos.y,False,self.color))
    def update(self,win):
        if not self.firework.exploded:
            self.firework.move_vector+=gravity
        self.firework.move()
        for Trails in self.firework.trails:
            Trails.show(win)
        self.show(win)
        if randint(0,10)==0:   #self.firework.move_vector.y >= 0:
            self.exploded = True
            self.explode()
        else:
            for pt in self.particles:
                pt.move_vector+= vector(gravity.x + uniform(-1, 1)/20, gravity.y / 2 + (randint(1, 8) / 100))
                pt.move()
                for t in pt.trails:
                    t.show(win)
                pt.show(win)
    def remove(self):
        if self.exploded:
            for xxx in self.particles:
                if xxx.remove is True:
                    self.particles.remove(xxx)
            if(len(self.particles) == 0):
                return True
            return False
def update(win, firework):
    for FW in firework:
        FW.update(win)
        if FW.remove():
            firework.remove(FW)
    pygame.display.update()
def main():
    pygame.init()
    pygame.display.set_caption("Happy new year 2021")
    win = pygame.display.set_mode((Width,Heigh))
    clock = pygame.time.Clock()
    firework = [Firework() for i in range(2)]
    run=True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    firework.append(Firework())
                if event.key == pygame.K_UP:
                    for i in range(5):
                        firework.append(Firework())
        win.fill((0,0,0))

        if randint(0,10) == 0:
            firework.append(Firework())
        update(win,firework)
    pyagme.quit()
    quit()

main()


            
