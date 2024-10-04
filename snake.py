import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube(object):
    width = 500
    rows = 20
    #we initialize dir_x to 1 so it starts moving automatically
    def __init__(self, start, dir_x=1, dir_y=0, color=(255, 0, 0)):
        self.pos = start
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.color = color

    def move(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.pos = (self.pos[0] + self.dir_x, self.pos[1] + self.dir_y)

    def draw(self, surface, eyes=False):
        dis = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i*dis+center-radius, j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 1
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for k in keys:
                if keys[pygame.K_LEFT]:
                    self.dir_x = -1
                    self.dir_y = 0
                    #assign new turn at the position of the head of the snake - turns is a dictionary
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_RIGHT]:
                    self.dir_x = 1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_UP]:
                    self.dir_x = 0
                    self.dir_y = 1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_DOWN]:
                    self.dir_x = 0
                    self.dir_y = -1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

            for i, cell in enumerate(self.body):
                p = cell.pos[:]
                if p in self.turns:
                    turn = self.turns[p]
                    cell.move(turn[0], turn[1])
                    #if it is the last cell in body, it removes that turn
                    if i == len(self.body)-1:
                        self.turns.pop(p)
                else:
                    if cell.dir_x == -1 and cell.pos[0] <= 0: cell.pos = (cell.rows-1, cell.pos[1])
                    elif cell.dir_x == 1 and cell.pos[0] >= rows-1: cell.pos = (0, cell.pos[1])
                    elif cell.dir_y == -1 and cell.pos[1] <= 0: cell.pos = (cell.pos[0], cell.rows-1)
                    elif cell.dir_y == 1 and cell.pos[1] >= rows-1: cell.pos = (cell.pos[0], 0)
                    else: cell.move(cell.dir_x, cell.dir_y)

                     
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dir_x, tail.dir_y

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dir_x = dx
        self.body[-1].dir_y = dy


    def draw(self, surface):
        for i, cell in enumerate(self.body):
            if i == 0: #if it is the head we draw eyes
                cell.draw(surface, True)
            else:
                cell.draw(surface)

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        #function that checks whether position is where snake is
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0 :
            continue
        else:
            break
    return (x,y)

def drawGrid(width, rows, surface):
    size_between = width // rows

    x = 0 
    y = 0
    for l in range(rows):
        x += size_between
        y += size_between

        #.line(surface,color,start_pos,end_pos)
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))

def redrawWindow(surface):
    global width, rows, s
    surface.fill((0, 0, 0))
    s.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

if __name__ == "__main__":
    #eventually, do a get color function to choose a color for the snake
    #do try and exceptions
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        #pygame tick delay of 50 seconds so game doesn't run too fast
        pygame.time.delay(50)
        #makes sure game doesn't run more than 10 fps
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(rows, s), color=(0, 255, 0))
        redrawWindow(win)