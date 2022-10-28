from __future__ import barry_as_FLUFL
import pygame
from OpenGL.GL import *

pygame.init()

black = (0.0, 0.0, 0.0, 1.0)

size = 4
width = 100 * size
height = 100 * size

pixels = []
for i in range(width):
    pixels.append([])
    for j in range(height):
        pixels[i].append(0)

screen = pygame.display.set_mode(
    (width, height),
    pygame.OPENGL | pygame.DOUBLEBUF
)

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

def Tub(x, y):
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
            try:
                if pixels[i][j+1] == 1 or pixels[i][j+1] == 2:
                    vecinos += 1
                if pixels[i][j-1] == 1 or pixels[i][j-1] == 2:
                    vecinos += 1
                if pixels[i-1][j-1] == 1 or pixels[i-1][j-1] == 2:
                    vecinos += 1
                if pixels[i+1][j-1] == 1 or pixels[i+1][j-1] == 2:
                    vecinos += 1
                if pixels[i-1][j+1] == 1 or pixels[i-1][j+1] == 2:
                    vecinos += 1
                if pixels[i+1][j+1] == 1 or pixels[i+1][j+1] == 2:
                    vecinos += 1
                if pixels[i-1][j] == 1 or pixels[i-1][j] == 2:
                    vecinos += 1
                if pixels[i+1][j] == 1 or pixels[i+1][j] == 2:
                    vecinos += 1

                if pixels[i][j] == 1:
                    if vecinos < 2 or vecinos > 3:
                        pixels[i][j] = 2
                elif vecinos == 3:
                    pixels[i][j] = 3
            except:
                pass
    
    for i in range(width):
        for j in range(height):
            if pixels[i][j] == 3:
                pixels[i][j] = 1
            elif pixels[i][j] == 2:
                pixels[i][j] = 0
            
    return pixels


Beacon(10, 10)
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
    # break