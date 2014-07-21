# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 23:37:53 2014

@author: sophie

Generating all dem maze solvers from scratch!
"""

import pygame, random, math, time
import heapq
from pygame.locals import *


class Cell(object):  
    def __init__(self, pos, size):
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        self.reachable = True
        self.x = pos[0]
        self.y = pos[1]
        self.g = 0 #cost to move from starting cell to given cell
        self.h = 0 #cost to move from given cell to ending cell
        self.f = 0 #sum of g and h
        self.parent = None
        
class Player:
    """Our moving block"""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        
class AStar_Model:
    """implements our maze solving alg"""
    def __init__ (self, screen_size):
        self.player = Player(32, 32)
        self.cells = []
        self.end_rect = None
        self.screen_size = screen_size
        self.start_button = pygame.Rect(550, 250, 100, 100)
        self.start_AStar = False
        self.alg_done = True
        
        self.open = [] #cells currently in open list, still processing
        heapq.heapify(self.open)
        self.closed = set() #cells in closed list, we already know they are part of best path
        self.grid = 10 #grid height       
         
        self.grid_size = self.screen_size / 10
        self.construct_grid()
#        self.construct_environment()
    
    def construct_grid(self):
        grid_size = self.grid_size
        x = y = 0
        while x < self.screen_size:
            while y < self.screen_size:
                if x == (self.screen_size - grid_size) and y == (self.screen_size - grid_size):
                    self.end_rect = pygame.Rect(x, y, grid_size, grid_size)
                    return
                self.cells.append(Cell((x, y), grid_size))                
                y += grid_size
            x += grid_size
            y = 0
            
    def init_AStar(self):
        print "Starting AStar"
        self.start = self.get_cell(0,0)
        self.end = self.end_rect
    
    def get_heuristic(self, cell):
        return 50*(abs(cell.x - self.end.x) + abs(cell.y - self.end.y)) #we arbitrary set 50 as the cost

    def get_cell(self, x, y):
        return self.cells[x * self.grid + y]
        
    def get_adjacent_cells(self, cell):
        grid_size = self.grid_size
        cells = []
        if cell.x < self.grid - grid_size:
            cells.append(self.get_cell(cell.x + grid_size, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y - grid_size))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x - grid_size, cell.y))
        if cell.y < self.grid - grid_size:
            cells.append(self.get_cell(cell.x, cell.y + grid_size))
        return cells
        
    def display_path(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            print "path: cell: %d, %d" % (cell.x, cell.y)
        self.alg_done = True
    
    def update_cell(self, adj, cell):
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g
    
    def process(self):
        heapq.heappush(self.open, (self.start.f, self.start))
        while len(self.open):
            f, cell = heapq.heappop(self.open)
            self.closed.add(cell)
            if cell is self.end:
                self.display_path()
                break
            adj_cells = self.get_adjacent_cells(cell)
            for c in adj_cells:
                if c.reachable and c not in self.closed:
                    if (c.f, c) in self.open:
                        if c.g > cell.g + 50:
                            self.update_cell(c, cell)
                        else:
                            self.update_cell(c, cell)
                            heapq.heappush(self.open, (c.f, c))
                    else:
                        self.update_cell(c, cell)
                        heapq.heappush(self.open, (c.f, c))
            
    
    
    def update(self):
        """Updates with each pass"""
        if self.start_AStar:
            self.alg_done = False
            self.init_AStar()
            
            
                
class PyGameWindowView:
    """draws our pretty maze"""
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        self.screen.fill(pygame.Color(255,255,255))
#        pygame.draw.rect(self.screen, pygame.Color(109, 109, 109), self.model.player.rect) #Player
        pygame.draw.rect(self.screen, pygame.Color(97, 255, 85), self.model.end_rect)
        pygame.draw.rect(self.screen, pygame.Color(255,222,0), self.model.start_button)
        for cell in self.model.cells: #Draws each wall block
            if cell.reachable == False:
                pygame.draw.rect(screen, pygame.Color(70, 198, 198), cell.rect)
            elif cell.reachable == True:
                pygame.draw.rect(screen, pygame.Color(0, 0, 0), cell.rect, 2)
            
        pygame.display.update()
        
        
class Controller:
    """takes user input and reflects accordingly"""
    def __init__(self, model):
        self.model = model
    
    def handle_pygame_mouse(self, event):
        """takes position of mouse click and turns square separate color"""
        x, y = event.pos        
        for cell in self.model.cells:
            if cell.rect.collidepoint(x, y):
                cell.reachable = not cell.reachable
        if self.model.start_button.collidepoint(x, y):
            self.model.start_AStar = True

if __name__ == "__main__":
    pygame.init()
    size = (700,500)
    screen = pygame.display.set_mode(size)
    model = AStar_Model(500)
    view = PyGameWindowView(model, screen)
    controller = Controller(model)
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                controller.handle_pygame_mouse(event)
        model.update()
        view.draw()
        if model.alg_done:
            time.sleep(0.001)
        else:
            time.sleep(100)
        
    pygame.quit()