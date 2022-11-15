import pygame
import random
from math import * 
from OpenGL.GL import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (152, 0, 136)
SKY = (50, 100, 200)
GROUND = (200, 200, 100)

colors = [
  (0, 20, 10),
  (4, 91, 82),
  (219, 242, 38),
  (0, 0, 255),
  (255, 255, 255)
]

walls = {
    "1": pygame.image.load('./grass.jpg'),
    "2": pygame.image.load('./wall2.png'),
    "3": pygame.image.load('./wall3.png'),
    "4": pygame.image.load('./wall4.png'),
    "5": pygame.image.load('./wall5.png'),
}

sprite1 = pygame.image.load('./sprite1.png')
sprite2 = pygame.image.load('./sprite2.png')
sprite3 = pygame.image.load('./sprite3.png')
sprite4 = pygame.image.load('./sprite4.png')

enemies = [
    {
        "x": 120,
        "y": 120,
        "sprite": sprite1
    },
    {
        "x": 300,
        "y": 300,
        "sprite": sprite2
    }
]

class Raycaster(object):
    def __init__ (self, screen):
        self.screen = screen
        x, y, self.width, self.height = screen.get_rect()
        self.blocksize = 50
        self.scale = 10
        self.player = {
            "x": int(self.blocksize + self.blocksize / 2),
            "y": int(self.blocksize + self.blocksize / 2),
            "fov": int(pi/3),
            "a": int(pi/10)
        }
        self.zbuffer = [99999 for z in range(0, int(self.width/2))]
        self.map = []
        self.clearZ()

    def clearZ(self):
        self.zbuffer = [99999 for z in range(0, int(self.width/2))]

    def point(self, x, y, c = WHITE):
        self.screen.set_at((x, y), c)

    def block(self, x, y, wall):
        for i in range(x, x + self.blocksize):
            for j in range(y, y + self.blocksize):
                tx = int((i - x) * 128 / self.blocksize)
                ty = int((j - y) * 128 / self.blocksize)
                c = wall.get_at((tx, ty))
                self.point(i, j, c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))
    
    def draw_map(self):
        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ':
                    self.block(x, y, walls[self.map[j][i]])

    def draw_player(self):
        self.point(self.player["x"], self.player["y"])

    def render(self):
        self.draw_map()
        self.draw_player()
        density = 50

        #minimap 
        for i in range(0, density):
            a = self.player["a"] - self.player["fov"] / 2 + self.player["fov"]*i/density
            d, c, tx = self.cast_ray(a)

        # line
        for i in range(0, 500):
            self.point(499, i)
            self.point(500, i)
            self.point(501, i)

        #draw in 3d
        density = 50
        for i in range(0, int(self.width/2)):
            a = self.player["a"] - self.player["fov"] / 2 + self.player["fov"]*i/(self.width/2)
            d, c, tx = self.cast_ray(a)
            x = int(self.width/2) + i
            h = self.height * self.height/self.scale
            if (d * cos(a - self.player["a"])) > 0:
                h = (self.height/(d * cos(a - self.player["a"]))) * self.height/self.scale

            if self.zbuffer[i] >= d:
                self.draw_stake(x, h, c, tx)
                self.zbuffer[i] = d
        
        for enemy in enemies:
            self.point(enemy["x"], enemy["y"], (255, 0, 0))

        for enemy in enemies:
            self.draw_sprite(enemy)

    def draw_sprite(self, sprite):
        sprite_a = atan2(
            sprite["y"] - self.player["y"], 
            sprite["x"] - self.player["x"]
        )

        d = (
            (self.player["x"] - sprite["x"])**2 + 
            (self.player["y"] - sprite["y"])**2
            )** 0.5

        sprite_size = int(((self.width/2)/d) * self.height/self.scale)

        sprite_x = int(
            (self.width/2) + 
            (sprite_a - self.player["a"]) * 
            (self.width/2) / self.player["fov"] 
            + sprite_size/2)

        sprite_y = int(self.height/2 - sprite_size/2)
        
        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                tx = int((x - sprite_x) * 128 / sprite_size)
                ty = int((y - sprite_y) * 128 / sprite_size)
                
                c = sprite["sprite"].get_at((tx, ty))

                if c != TRANSPARENT:
                    if(x > int(self.width/2) and x < self.width):
                        if self.zbuffer[x - int(self.width/2)] >= d:
                            self.zbuffer[x - int(self.width/2)] = d
                            self.point(x, y, c)

    def cast_ray(self, a):
        d = 0
        ox = self.player["x"]
        oy = self.player["y"]

        while True:
            x = int(ox + d*cos(a))
            y = int(oy + d*sin(a))

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x - i * self.blocksize
                hity = y - j * self.blocksize
                
                if 1 < hitx < self.blocksize-1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / self.blocksize)
                return d, self.map[j][i], tx
            
            self.point(x, y)

            d += 1
    
    def draw_stake(self, x, h, c, tx):
        start_y = int(self.height/2 - h/2)
        end_y = int(self.height/2 + h/2)
        height = end_y - start_y

        for y in range(start_y, end_y):
            ty = int((y - start_y) * 128 / height)
            color = walls[c].get_at((tx, ty))
            self.point(x, y, color)

pygame.init()
screen = pygame.display.set_mode((1000, 500))
r = Raycaster(screen)
r.load_map("./map.txt")

running = True
while running:
    screen.fill(BLACK, (0, 0, r.width/2, r.height))
    screen.fill(SKY, (r.width/2, 0, r.width, r.height/2))
    screen.fill(GROUND, (r.width/2, r.height/2, r.width, r.height/2))
    r.clearZ()
    r.render()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        a = r.player["a"]
        # cambiar el movimiento segun el angulo en el que esta el jugador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if a == pi/2:
                    r.player["x"] -= 10
                elif a == 0 or a == 2*pi:
                    r.player["y"] += 10
                elif a == 3*pi/2:
                    r.player["x"] += 10
                elif a == pi:
                    r.player["y"] -= 10
                elif a < pi/2 :
                    r.player["x"] -= int(10 * cos(r.player["a"]))
                    r.player["y"] += int(10 * sin(r.player["a"]))
                elif a > pi/2 and a < pi:
                    r.player["y"] -= int(10 * sin(r.player["a"]))
                    r.player["x"] += int(10 * cos(r.player["a"]))
                elif a > pi and a < 3*pi/2:
                    r.player["x"] -= int(10 * cos(r.player["a"]))
                    r.player["y"] += int(10 * sin(r.player["a"]))
                elif a > 3*pi/2 and a < 2*pi:
                    r.player["y"] -= int(10 * sin(r.player["a"]))
                    r.player["x"] += int(10 * cos(r.player["a"]))
            if event.key == pygame.K_LEFT:
                if a == pi/2:
                    r.player["x"] += 10
                elif a == 0 or a == 2*pi:
                    r.player["y"] -= 10
                elif a == 3*pi/2:
                    r.player["x"] -= 10
                elif a == pi:
                    r.player["y"] += 10
                elif a < pi/2 :
                    r.player["x"] += int(10 * cos(r.player["a"]))
                    r.player["y"] -= int(10 * sin(r.player["a"]))
                elif a > pi/2 and a < pi:
                    r.player["y"] += int(10 * sin(r.player["a"]))
                    r.player["x"] -= int(10 * cos(r.player["a"]))
                elif a > pi and a < 3*pi/2:
                    r.player["x"] += int(10 * cos(r.player["a"]))
                    r.player["y"] -= int(10 * sin(r.player["a"]))
                elif a > 3*pi/2 and a < 2*pi:
                    r.player["y"] += int(10 * sin(r.player["a"]))
                    r.player["x"] -= int(10 * cos(r.player["a"]))
            if event.key == pygame.K_UP:
                if a == pi/2:
                    r.player["y"] += 10
                elif a == 0 or a == 2*pi:
                    r.player["x"] += 10
                elif a == 3*pi/2:
                    r.player["y"] -= 10
                elif a == pi:
                    r.player["x"] -= 10
                else :
                    r.player["y"] += int(10 * sin(r.player["a"]))
                    r.player["x"] += int(10 * cos(r.player["a"]))
            if event.key == pygame.K_DOWN:
                if a == pi/2:
                    r.player["y"] -= 10
                elif a == 0 or a == 2*pi:
                    r.player["x"] -= 10
                elif a == 3*pi/2:
                    r.player["y"] += 10
                elif a == pi:
                    r.player["x"] += 10
                else:
                    r.player["y"] -= int(10 * sin(r.player["a"]))
                    r.player["x"] -= int(10 * cos(r.player["a"]))
            if event.key == pygame.K_a:
                if r.player["a"] <= 0:
                    r.player["a"] = 2*pi - pi/10
                r.player["a"] -= pi/10
            if event.key == pygame.K_d:
                if r.player["a"] >= 2*pi:
                    r.player["a"] = pi/10
                r.player["a"] += pi/10