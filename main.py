import pygame
import random
from OpenGL.GL import *

pygame.init()

black = (0.0, 0.0, 0.0, 1.0)

size = 4
width = 150 * size
height = width

screen = pygame.display.set_mode(
    (width, height),
    pygame.OPENGL | pygame.DOUBLEBUF
)

width = int(width/size)
height = width


pixels = []
for i in range(width):
    pixels.append([])
    for j in range(height):
        pixels[i].append(0)

def Block(x, y):
    pixels[x][y] = 1
    pixels[x+1][y] = 1
    pixels[x][y+1] = 1
    pixels[x+1][y+1] = 1

def BeeHive(x, y):
    pixels[x][y+1] = 1
    pixels[x+1][y] = 1
    pixels[x+2][y] = 1
    pixels[x][y+3] = 1
    pixels[x+1][y+2] = 1
    pixels[x+2][y+2] = 1

def Loaf(x, y):
    pixels[x+2][y] = 1
    pixels[x][y+2] = 1
    pixels[x+1][y+1] = 1
    pixels[x+1][y+3] = 1
    pixels[x+2][y] = 1
    pixels[x+2][y+3] = 1
    pixels[x+3][y+1] = 1
    pixels[x+3][y+2] = 1

def Boat(x, y):
    pixels[x+1][y] = 1
    pixels[x][y+1] = 1
    pixels[x][y+2] = 1
    pixels[x+1][y+2] = 1
    pixels[x+2][y+1] = 1

def Tube(x, y):
    pixels[x+1][y] = 1
    pixels[x][y+1] = 1
    pixels[x+1][y+2] = 1
    pixels[x+2][y+1] = 1

def Toad(x, y):
    pixels[x][y] = 1
    pixels[x+1][y] = 1
    pixels[x+1][y+1] = 1
    pixels[x+2][y] = 1
    pixels[x+2][y+1] = 1
    pixels[x+3][y+1] = 1

def Beacon(x, y):
    pixels[x][y+2] = 1
    pixels[x][y+3] = 1
    pixels[x+1][y+3] = 1
    pixels[x+2][y] = 1
    pixels[x+3][y] = 1
    pixels[x+3][y+1] = 1


def Blinker(x, y):
    pixels[x][y] = 1
    pixels[x][y+1] = 1
    pixels[x][y-1] = 1

def Pulsar(x, y):
    #izquierda
    pixels[x-2][y+1] = 1
    pixels[x-3][y+1] = 1
    pixels[x-4][y+1] = 1
    pixels[x-1][y+2] = 1
    pixels[x-1][y+3] = 1
    pixels[x-1][y+4] = 1

    pixels[x-6][y+2] = 1
    pixels[x-6][y+3] = 1
    pixels[x-6][y+4] = 1

    pixels[x-2][y+6] = 1
    pixels[x-3][y+6] = 1
    pixels[x-4][y+6] = 1

    #izquierda abajo
    pixels[x-2][y-1] = 1
    pixels[x-3][y-1] = 1
    pixels[x-4][y-1] = 1
    pixels[x-1][y-2] = 1
    pixels[x-1][y-3] = 1
    pixels[x-1][y-4] = 1

    pixels[x-6][y-2] = 1
    pixels[x-6][y-3] = 1
    pixels[x-6][y-4] = 1

    pixels[x-2][y-6] = 1
    pixels[x-3][y-6] = 1
    pixels[x-4][y-6] = 1

    #derecha
    pixels[x+2][y+1] = 1
    pixels[x+3][y+1] = 1
    pixels[x+4][y+1] = 1
    pixels[x+1][y+2] = 1
    pixels[x+1][y+3] = 1
    pixels[x+1][y+4] = 1

    pixels[x+6][y+2] = 1
    pixels[x+6][y+3] = 1
    pixels[x+6][y+4] = 1

    pixels[x+2][y+6] = 1
    pixels[x+3][y+6] = 1
    pixels[x+4][y+6] = 1

    #derecha abajo
    pixels[x+2][y-1] = 1
    pixels[x+3][y-1] = 1
    pixels[x+4][y-1] = 1
    pixels[x+1][y-2] = 1
    pixels[x+1][y-3] = 1
    pixels[x+1][y-4] = 1

    pixels[x+6][y-2] = 1
    pixels[x+6][y-3] = 1
    pixels[x+6][y-4] = 1

    pixels[x+2][y-6] = 1
    pixels[x+3][y-6] = 1
    pixels[x+4][y-6] = 1

def PentaDecathlon(x, y):
    pixels[x][y+4] = 1
    pixels[x-1][y+4] = 1
    pixels[x+1][y+4] = 1
    pixels[x-2][y+3] = 1
    pixels[x+2][y+3] = 1
    pixels[x-3][y+2] = 1
    pixels[x+3][y+2] = 1
    pixels[x-4][y] = 1
    pixels[x+4][y] = 1
    pixels[x-4][y-1] = 1
    pixels[x+4][y-1] = 1
    pixels[x][y-5] = 1
    pixels[x-1][y-5] = 1
    pixels[x+1][y-5] = 1
    pixels[x-2][y-4] = 1
    pixels[x+2][y-4] = 1
    pixels[x-3][y-3] = 1
    pixels[x+3][y-3] = 1

def Glider(x, y):
    pixels[x-1][y] = 1
    pixels[x][y-1] = 1
    pixels[x+1][y-1] = 1
    pixels[x+1][y] = 1
    pixels[x+1][y+1] = 1

def LightSpaceship(x, y):
    pixels[x][y] = 1
    pixels[x][y+2] = 1
    pixels[x+1][y+3] = 1
    pixels[x+2][y+3] = 1
    pixels[x+3][y+3] = 1
    pixels[x+4][y+3] = 1
    pixels[x+4][y+2] = 1
    pixels[x+4][y+1] = 1
    pixels[x+3][y] = 1

def MiddleSpaceship(x, y):
    pixels[x][y+1] = 1
    pixels[x][y+3] = 1
    pixels[x+1][y] = 1
    pixels[x+2][y] = 1
    pixels[x+3][y] = 1
    pixels[x+4][y] = 1
    pixels[x+5][y] = 1
    pixels[x+5][y+1] = 1
    pixels[x+5][y+2] = 1
    pixels[x+4][y+3] = 1
    pixels[x+2][y+5] = 1

def Piramid(x, y): # creado
    pixels[x][y] = 1
    pixels[x+1][y] = 1
    pixels[x-1][y] = 1
    pixels[x-2][y+1] = 1
    pixels[x-1][y+2] = 1
    pixels[x][y+3] = 1
    pixels[x+2][y+1] = 1
    pixels[x+1][y+2] = 1

def Infinite(x, y):
    pixels[x][y] = 1
    pixels[x+1][y+1] = 1
    pixels[x+1][y-1] = 1
    pixels[x+2][y+2] = 1
    pixels[x+2][y-2] = 1
    pixels[x+3][y+1] = 1
    pixels[x+3][y-1] = 1
    pixels[x+4][y] = 1

    
    pixels[x-1][y+1] = 1
    pixels[x-1][y-1] = 1
    pixels[x-2][y+2] = 1
    pixels[x-2][y-2] = 1
    pixels[x-3][y+1] = 1
    pixels[x-3][y-1] = 1
    pixels[x-4][y] = 1


def pixel(x, y, color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(x, y, 10, 10)
    glClearColor(color[0], color[1], color[2], color[3])
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)

def Cells(pixels):
    glEnable(GL_SCISSOR_TEST)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    for i in range(width):
        for j in range(height):
            if pixels[i][j] == 1:
                glScissor(i*size, j*size, size, size)
                glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)

def GameOfLife(pixels):

    for i in range(width):
        for j in range(height):
            # cada pixel individual
            vecinos = 0

            if pixels[i][(j+1)%height] == 1 or pixels[i][(j+1)%height] == 2:
                vecinos += 1
            if pixels[i][j-1] == 1 or pixels[i][j-1] == 2:
                vecinos += 1
            if pixels[i-1][j-1] == 1 or pixels[i-1][j-1] == 2:
                vecinos += 1
            if pixels[(i+1)%width][j-1] == 1 or pixels[(i+1)%width][j-1] == 2:
                vecinos += 1
            if pixels[i-1][(j+1)%height] == 1 or pixels[i-1][(j+1)%height] == 2:
                vecinos += 1
            if pixels[(i+1)%width][(j+1)%height] == 1 or pixels[(i+1)%width][(j+1)%height] == 2:
                vecinos += 1
            if pixels[i-1][j] == 1 or pixels[i-1][j] == 2:
                vecinos += 1
            if pixels[(i+1)%width][j] == 1 or pixels[(i+1)%width][j] == 2:
                vecinos += 1

            if pixels[i][j] == 1:
                if vecinos < 2 or vecinos > 3:
                    pixels[i][j] = 2
            elif vecinos == 3:
                pixels[i][j] = 3
    
    for i in range(width):
        for j in range(height):
            if pixels[i][j] == 3:
                pixels[i][j] = 1
            elif pixels[i][j] == 2:
                pixels[i][j] = 0
            
    return pixels

def GenerateScreen(factor):
    for i in range(width):
        for j in range(height):

            if j % factor == 1 and i % factor == 1 and j > 10 and i > 10:
                
                probabilidad = random.randint(1, 10)
                if probabilidad >= 6:
                    x = i
                    y = j
                    func = random.randint(1, 15)

                    if func == 1:
                        Block(x, y)
                    elif func == 2:
                        BeeHive(x, y)
                    elif func == 3:
                        Loaf(x, y)
                    elif func == 4:
                        Boat(x, y)
                    elif func == 5:
                        Tube(x, y)
                    elif func == 6:
                        Toad(x, y)
                    elif func == 7:
                        Beacon(x, y)
                    elif func == 8:
                        Blinker(x, y)
                    elif func == 9:
                        Pulsar(x, y)
                    elif func == 10:
                        PentaDecathlon(x, y)
                    elif func == 11:
                        Glider(x, y)
                    elif func == 12:
                        LightSpaceship(x, y)
                    elif func == 13:
                        MiddleSpaceship(x, y)
                    elif func == 14:
                        Piramid(x, y)
                    elif func == 15:
                        Infinite(x, y)
        
GenerateScreen(int((height)/10))
running = True
while running:
    # clean
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # paint
    pixels = GameOfLife(pixels)
    Cells(pixels)

    # flip
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #break