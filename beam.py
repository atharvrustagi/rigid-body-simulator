import pygame as pg
import math as mt

sz = (500, 500)
win = pg.display.set_mode(sz)
pg.display.set_caption('Physics')

# colors
blk = (0,0,0)
wht = (255,255,255)

class beam:
    def __init__(self, length, angle):
        # beam parameters (all distance measurements (meters) are in pixels)
        self.l = length              # beam length
        self.vx, self.vy = 0.0, 0.0       # beam initial speed
        self.theta = angle           # initial angle
        self.omega = 0.0             # initial angular velocity
        self.bx, self.by = 250.0, 100.0   # intial position
        self.g = 0.1                 # acceleration due to gravity 
    
   
    def update_beam(self, fy):
        # update
        self.vy += self.g
        self.by += self.vy
        self.bx += self.vx
        self.theta += self.omega
        # check for collision
        self.collide(fy)
    
    def collide(self, fy):
        # lower bound box
        lc = self.l*mt.cos(self.theta)/2
        lb = self.by + abs(lc)
        if lb < fy:
            return
        # handle collision
        # print(self.by)
        tant_1 = 1 / (1 + (mt.tan(self.theta)**2) / 12)
        self.omega = (12 * self.vy**2) * tant_1 / self.l**2
        v2 = (1-tant_1) * self.vy**2
        self.vy = v2 * mt.sin(self.theta)
        self.vx = v2 * mt.cos(self.theta)
        

# beam
beam_1 = beam(100.0, mt.pi/4)

# floor
fx, fy = None, 450

# framerate
clock = pg.time.Clock()
fps = 75

def draw_beam(beam_1):
    lc = beam_1.l*mt.cos(beam_1.theta)/2
    ls = beam_1.l*mt.sin(beam_1.theta)/2
    start = (beam_1.bx-ls, beam_1.by+lc)
    end = (beam_1.bx+ls, beam_1.by-lc)
    pg.draw.line(win, wht, start, end)

def show(beam_1):
    win.fill(blk)
    draw_beam(beam_1)     # beam_1
    pg.draw.line(win, wht, (0, fy), (sz[0], fy))    # floor
    pg.display.update()

run = True
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
    # theta += 0.001
    clock.tick(fps)
    beam_1.update_beam(fy)
    show(beam_1)
pg.quit()