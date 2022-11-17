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

Key = pygame.image.load('./Key.png')
map_keys = pygame.image.load('./map_keys.png')
selected_key = pygame.image.load('./selected_key.png')

keys = [
    {
        "x": 120,
        "y": 120,
        "sprite": map_keys,
        "selected": False,
        "enabled": True
    },
    {
        "x": 290,
        "y": 170,
        "sprite": map_keys,
        "selected": False,
        "enabled": True
    },
    {
        "x": 380,
        "y": 370,
        "sprite": map_keys,
        "selected": False,
        "enabled": True
    }
]

start = pygame.image.load('./inicio.png')
final = pygame.image.load('./final.png')

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
        self.keys = 0
        self.avanzar = False
        self.prev_event = None

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

        # draw keys
        size = 55
        key_size = 128

        for i in range(self.keys):
            factor = i * size
            for x in range(factor, size + factor):
                for y in range(0, size):
                    tx = int((x - factor) * key_size / size)
                    ty = int(y * key_size / size)
                    c = Key.get_at((tx, ty))
                    
        
                    if c != TRANSPARENT:
                        self.point(x, y, c)

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
            
            try:
                h = (self.height/(d * cos(a - self.player["a"]))) * self.height/self.scale
                self.avanzar = True

                if self.zbuffer[i] >= d:
                    self.draw_stake(x, h, c, tx)
                    self.zbuffer[i] = d
            except e as Exception:
                print(e)
                self.avanzar = False
                self.movement()

        for key in keys:
            if key["enabled"]:
                self.point(key["x"]    , key["y"], (255, 0, 0))
                self.point(key["x"] + 1, key["y"] + 1, (255, 0, 0))
                self.point(key["x"] + 1, key["y"] - 1, (255, 0, 0))
                self.point(key["x"] - 1, key["y"] - 1, (255, 0, 0))
                self.point(key["x"] - 1, key["y"] + 1, (255, 0, 0))
                
        for key in keys:
            if key["enabled"]:
                self.draw_sprite(key)

    def draw_sprite(self, sprite):
        sprite_a = atan2(
            sprite["y"] - self.player["y"], 
            sprite["x"] - self.player["x"]
        )

        d = (
            (self.player["x"] - sprite["x"])**2 + 
            (self.player["y"] - sprite["y"])**2
            )** 0.5

        if d < 50:
            sprite["sprite"] = selected_key
            sprite["selected"] = True

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

    def draw_image(self, image):
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.point(x, y, image.get_at((x, y)))
    
    def fps_counter(self, clock):
        fps = str(float(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("Red"))
        self.screen.blit(fps_text, (self.width-50, self.height-30))

    def movement(self, r = None, event = None):
        if r == None:
            r = self
        
        if event == None:
            event = self.prev_event 
        
        a = r.player["a"]

        if event.key == pygame.K_RIGHT:
                if a == pi/2:
                    if r.avanzar:
                        r.player["x"] -= 10
                    else:
                        r.player["x"] += 10
                elif a == 0 or a == 2*pi:
                    if r.avanzar:
                        r.player["y"] += 10
                    else:
                        r.player["y"] -= 10
                elif a == 3*pi/2:
                    if r.avanzar:
                        r.player["x"] += 10
                    else:
                        r.player["x"] -= 10
                elif a == pi:
                    if r.avanzar:
                        r.player["y"] -= 10
                    else:
                        r.player["y"] += 10
                elif a < pi/2 :
                    if r.avanzar:
                        r.player["x"] -= int(10 * cos(r.player["a"]))
                        r.player["y"] += int(10 * sin(r.player["a"]))
                    else:
                        r.player["x"] += int(10 * cos(r.player["a"]))
                        r.player["y"] -= int(10 * sin(r.player["a"]))
                elif a > pi/2 and a < pi:
                    if r.avanzar:
                        r.player["y"] -= int(10 * sin(r.player["a"]))
                        r.player["x"] += int(10 * cos(r.player["a"]))
                    else:
                        r.player["y"] += int(10 * sin(r.player["a"]))
                        r.player["x"] -= int(10 * cos(r.player["a"]))
                elif a > pi and a < 3*pi/2:
                    if r.avanzar:
                        r.player["x"] -= int(10 * cos(r.player["a"]))
                        r.player["y"] += int(10 * sin(r.player["a"]))
                    else:
                        r.player["x"] += int(10 * cos(r.player["a"]))
                        r.player["y"] -= int(10 * sin(r.player["a"]))
                elif a > 3*pi/2 and a < 2*pi:
                    if r.avanzar:
                        r.player["y"] -= int(10 * sin(r.player["a"]))
                        r.player["x"] += int(10 * cos(r.player["a"]))
                    else:
                        r.player["y"] += int(10 * sin(r.player["a"]))
                        r.player["x"] -= int(10 * cos(r.player["a"]))
        if event.key == pygame.K_LEFT:
            if a == pi/2:
                if r.avanzar:
                    r.player["x"] += 10
                else:
                    r.player["x"] -= 10
            elif a == 0 or a == 2*pi:
                if r.avanzar:
                    r.player["y"] -= 10
                else:
                    r.player["y"] += 10
            elif a == 3*pi/2:
                if r.avanzar:
                    r.player["x"] -= 10
                else:
                    r.player["x"] += 10
            elif a == pi:
                if r.avanzar:
                    r.player["y"] += 10
                else:
                    r.player["y"] -= 10
            elif a < pi/2 :
                if r.avanzar:
                    r.player["x"] += int(10 * cos(r.player["a"]))
                    r.player["y"] -= int(10 * sin(r.player["a"]))
                else:
                    r.player["x"] -= int(10 * cos(r.player["a"]))
                    r.player["y"] += int(10 * sin(r.player["a"]))
            elif a > pi/2 and a < pi:
                if r.avanzar:
                    r.player["y"] += int(10 * sin(r.player["a"]))
                    r.player["x"] -= int(10 * cos(r.player["a"]))
                else:
                    r.player["y"] -= int(10 * sin(r.player["a"]))
                    r.player["x"] += int(10 * cos(r.player["a"]))
            elif a > pi and a < 3*pi/2:
                if r.avanzar:
                    r.player["x"] += int(10 * cos(r.player["a"]))
                    r.player["y"] -= int(10 * sin(r.player["a"]))
                else:
                    r.player["x"] -= int(10 * cos(r.player["a"]))
                    r.player["y"] += int(10 * sin(r.player["a"]))
            elif a > 3*pi/2 and a < 2*pi:
                if r.avanzar:
                    r.player["y"] += int(10 * sin(r.player["a"]))
                    r.player["x"] -= int(10 * cos(r.player["a"]))
                else:
                    r.player["y"] -= int(10 * sin(r.player["a"]))
                    r.player["x"] += int(10 * cos(r.player["a"]))
        if event.key == pygame.K_UP:
            if a == pi/2:
                if r.avanzar:
                    r.player["y"] += 10
                else:
                    r.player["y"] -= 10
            elif a == 0 or a == 2*pi:
                if r.avanzar:
                    r.player["x"] += 10
                else:
                    r.player["x"] -= 10
            elif a == 3*pi/2:
                if r.avanzar:
                    r.player["y"] -= 10
                else:
                    r.player["y"] += 10
            elif a == pi:
                if r.avanzar:
                    r.player["x"] -= 10
                else:
                    r.player["x"] += 10
            else :
                if r.avanzar:
                    r.player["y"] += int(10 * sin(r.player["a"]))
                    r.player["x"] += int(10 * cos(r.player["a"]))
                else:
                    r.player["y"] -= int(10 * sin(r.player["a"]))
                    r.player["x"] -= int(10 * cos(r.player["a"]))
        if event.key == pygame.K_DOWN:
            if a == pi/2:
                if r.avanzar:
                    r.player["y"] -= 10
                else:
                    r.player["y"] += 10
            elif a == 0 or a == 2*pi:
                if r.avanzar:
                    r.player["x"] -= 10
                else:
                    r.player["x"] += 10
            elif a == 3*pi/2:
                if r.avanzar:
                    r.player["y"] += 10
                else:
                    r.player["y"] -= 10
            elif a == pi:
                if r.avanzar:
                    r.player["x"] += 10
                else:
                    r.player["x"] -= 10
            else:
                if r.avanzar:
                    r.player["y"] -= int(10 * sin(r.player["a"]))
                    r.player["x"] -= int(10 * cos(r.player["a"]))
                else:
                    r.player["y"] += int(10 * sin(r.player["a"]))
                    r.player["x"] += int(10 * cos(r.player["a"]))
        if event.key == pygame.K_a:
            if r.player["a"] <= 0:
                r.player["a"] = 2*pi - pi/10
            r.player["a"] -= pi/10
        if event.key == pygame.K_d:
            if r.player["a"] >= 2*pi:
                r.player["a"] = pi/10
            r.player["a"] += pi/10
        if event.key == pygame.K_e:
            for key in keys:
                if key["selected"] and key["enabled"]:
                    pygame.mixer.Sound.play(key_effect)
                    key["enabled"] = False
                    r.keys += 1
        
        a = r.player["a"]

pygame.init()
screen = pygame.display.set_mode((1000, 500))
r = Raycaster(screen)
r.load_map("./map.txt")

key_effect = pygame.mixer.Sound('GrabKeys.mp3')
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

inicio = True
while inicio:
    r.draw_image(start)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                inicio = False

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20, bold = True)

#running = True
while r.keys < len(keys):

    screen.fill(BLACK, (0, 0, r.width/2, r.height))
    screen.fill(SKY, (r.width/2, 0, r.width, r.height/2))
    screen.fill(GROUND, (r.width/2, r.height/2, r.width, r.height/2))
    r.clearZ()
    r.render()

    r.fps_counter(clock)
    clock.tick(60)

    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # cambiar el movimiento segun el angulo en el que esta el jugador
        if event.type == pygame.KEYDOWN:
            r.prev_event = event
            r.movement(r, event)
    


victoria = True
while victoria:

    r.draw_image(final)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                victoria = False