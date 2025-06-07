import pygame
from lib import color

class Grid:
    def __init__(self, display, rows, columns, position, width, height):
        self.display = display
        self.rows = rows
        self.columns = columns
        self.position = position

        self.width = width
        self.height = height

        self.draw_lines = True
        self.line_color = color.white

        self.grid = [[None for _ in range(self.columns)] for _ in range(self.rows)]


    def set_point(self, pos, thing):
        self.grid[pos[1]][pos[0]] = thing
        
    def set_points(self, pos_list, thing):
        for pos in pos_list:
            self.set_point(pos, thing)
    
    def get_point(self, pos):
        return self.grid[pos[1]][pos[0]]
    
    def is_free(self, pos):
        '''
        check if a grid position has nothing in it and is in bounds
        '''
        available = True
        
        if pos[1] >= self.rows or pos[1] < 0 or pos[0] >= self.columns or pos[0] < 0 or \
                    self.get_point(pos) != None:
            available = False
        return available
    
    def range_is_free(self, range, ignore=[]) -> bool:
        """
        check if a list of (x,y) vectors are free
        
        Param:
        Range [(x,y)]:      list of vectors to check if free
        ignore [(x,y)]:     list of vectors to ignore in the range
        
        Returns:
        True if all valid vectors are free
        """
        free = True
        n=0
        while free and n < len(range):
            block = range[n]
            if block not in ignore:
                if not self.is_free(block):
                    free = False           
            n += 1
        return free
                
        

    def draw(self):
        for y in range(self.rows):
            for x in range(self.columns):
                if self.get_point([x,y]) is not None:
                    pygame.draw.rect(self.display,
                                     self.get_point([x,y]),
                                     [self.position[0] + x * self.width,
                                      self.position[1] + y * self.height,
                                      self.width, self.height])
        if self.draw_lines:
            for i in range(self.rows + 1):
                pygame.draw.line(self.display, self.line_color,
                                 (self.position[0], self.position[1] + i * self.height),
                                 (self.position[0]+ self.width * self.columns,
                                  self.position[1] + i * self.height))
            for i in range(self.columns + 1):
                pygame.draw.line(self.display, self.line_color,
                                 (self.position[0]+ i * self.width, self.position[1]),
                                 (self.position[0]+ i * self.width,
                                  self.position[1] + self.height * self.rows))
                
    def find_full_rows(self) -> list:
        """
        find rowns in the grid that are full
        
        Returns:
        [(int)]     list of all full rows 
        """
        full_rows = []
        
        for row_num, row in enumerate(self.grid):
            if None not in row:
                full_rows.append(row_num)
                
        return full_rows
    
    def remove_row(self, row:int) -> None:
        """
        pop row from grid list then add new row at top 
        
        Param:
        row (int):  the row to be poped
        """
        self.grid.pop(row)
        self.grid.insert(0, [None for _ in range(self.columns)])
        
    def clear(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self.grid[y][x] = None  
                
    def add_shape_display(self, shape):
        pass
    
    def remove_shape_display(self, shape):
        self.set_points(shape.display, None)
    
    def add_shape(self, shape):
        pass
    
    def remove_shape(self, shape):
        self.set_points(shape.shapes[shape.direction], None)

    def _print(self):
        for i in self.grid:
            print(i)