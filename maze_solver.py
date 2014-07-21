# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 07:55:30 2014

@author: sophie

This tutorial will walk you through a simple implementation of a maze solver
program. We will use two algorithms, recursion and the more sophisticated
A* search. Some python techniques we'll be using include:
 - Classes
 - List manipulation
 - Recursive functions
 
 """

import heapq

class Cell(object):
    def __init__ (self, x, y, reachable):
        """Initializes new cell. x and y define coordinates. Reachable defines
        wall or not wall"""
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        
class AStar(object):
    def __init__(self):
        print "init astar"
        self.op = []
        heapq.heapify(self.op)
        self.cl = set()
        self.cells = []
        self.gridHeight = 6
        self.gridWidth = 6
        
    def init_grid(self):
        print "initgrid"
        walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),
                 (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(0,0)
        self.end = self.get_cell(5, 5)

    
    def get_heuristic(self, cell):
        print "getting heruistic"
        return 10*(abs(cell.x - self.end.x) + abs(cell.y - self.end.y))
        
    def get_cell(self, x, y):
        print "getting cell"
        return self.cells[x * self.gridHeight + y]
    
    def get_adjacent_cells(self, cell):
        print "getting adj cells"
        cells = []
        if cell.x < self.gridWidth - 1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.gridHeight - 1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        print "len of cells", len(cells)
        return cells
    
    def display_path(self):
        print "display path"
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            print "path: cell: %d, %d" % (cell.x, cell.y)
    
    def update_cell(self, adj, cell):
        print "updating cell"
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g
        
    def process(self):
        print "process started"
        heapq.heappush(self.op, (self.start.f, self.start))
        print len(self.op)
        while len(self.op):
            print "in while loop"
            f, cell = heapq.heappop(self.op)
            self.cl.add(cell)
            if cell is self.end:
                print "cell at self.end"
                self.display_path()
                break
            adj_cells = self.get_adjacent_cells(cell)
            print "adding adj_cells"
            for c in adj_cells:
                print "for c in adj_cells"
                if c.reachable and c not in self.cl:
                    print "first if"
                    if (c.f, c) in self.op:
                        print "second if"
                        if c.g > cell.g + 10:
                            print "third if"
                            self.update_cell(c, cell)
                        else:
                            print "pushing to heap"
                            self.update_cell(c, cell)
                            heapq.heappush(self.op, (c.f, c))
                    else:
                        self.update_cell(c, cell)
                        heapq.heappush(self.op, (c.f, c))
                            
                            
alg = AStar()
alg.init_grid()
alg.process()