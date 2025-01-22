import pygame
from random import randint
from lib import color, pygame_window, Grid, Key
from lib.shape import *


"""
game design decitions:
    add score for droping blocks
        -only if they are droped all the way
        -1 point for each block droped through
        
todo:
    resizable elements 
"""
        
    
class Score:
    def __init__(self, display):
        self.display = display
        self.font = pygame.font.Font('assets/fonts/Helvetica.ttf', 40)
        self.score = 0
        self.surface = None
        self.create_surface()
        
    def draw(self):
        self.display.blit(self.surface, [50,470])
        
    def create_surface(self):
        self.surface = pygame.Surface([200, 50])
        self.surface.fill(color.gray)
        font = self.font.render(str(self.score), True, color.white)
        self.surface.blit(font, [7,7])
    
    def add(self, amount):
        self.score += amount
        self.create_surface()
    
    def set(self, amount):
        self.score = amount
        self.create_surface()
        
        
class Next_block:
    def __init__(self, display):
        self.display = display

    
class Window(pygame_window.main):
    TICK = pygame.USEREVENT + 1
    def __init__(self):
        super().__init__(800, 600, 'TETRIS')
        pygame.font.init()
        
        self.background_colour = color.black
        self.tick_speed = 500
        
        self.key_rep = 50
        self.first_key_rep = 200
        
        self.keys = {'move_left':Key(pygame.K_LEFT, self.key_rep, self.first_key_rep),
                     'move_right':Key(pygame.K_RIGHT, self.key_rep, self.first_key_rep),
                     'rotate_right':Key(pygame.K_UP,float('inf'),float('inf')),
                     'rotate_left':Key(pygame.K_z,float('inf'),float('inf')),
                     'soft_drop':Key(pygame.K_DOWN,self.key_rep, self.key_rep),
                     'hard_drop':Key(pygame.K_SPACE,float('inf'),float('inf'))}
        
        self.grid = Grid(self.display, 20, 10, (280,20), 25, 25)
        self.score = Score(self.display)
        
        self.shape = self.rand_shape()
        pygame.time.set_timer(Window.TICK, self.tick_speed)
        
    def tick(self):
        if (self.shape.can_advance(0, 1)):
            self.shape.advance(0, 1)
        else:
            #hit end create new shape
            for row in self.grid.find_full_rows():
                self.grid.remove_row(row)
                self.score.add(100)
                
            self.shape = self.rand_shape()
                
    
    def update(self):
        super().update()
        if self.keys['move_right'].keypress():
            if self.shape.can_advance(1, 0):
                self.shape.advance(1, 0)
        elif self.keys['move_left'].keypress():
            if self.shape.can_advance(-1, 0):
                self.shape.advance(-1, 0)
        elif self.keys['rotate_right'].keypress():
            if self.shape.can_rotate_right():
                self.shape.rotate_right()
        elif self.keys['rotate_left'].keypress():
            if self.shape.can_rotate_left():
                self.shape.rotate_left()
        elif self.keys['soft_drop'].keypress():
            self.tick()
        elif self.keys['hard_drop'].keypress():
            distance = self.shape.hard_drop()
            self.score.add(distance)
            self.tick()
        
        
    def draw(self):
        super().draw()
        self.grid.draw()
        self.score.draw()
    
    def event_handle(self, event):
        super().event_handle(event)
        if event.type == Window.TICK:
            self.tick()
        elif event.type == pygame.KEYDOWN:
            found = False
            n=0
            actions = list(self.keys.keys())
            while not found and n < len(actions):
                action = actions[n]
                if event.key == self.keys[action].key:
                    found = True
                    self.keys[action].set_keydown(True)
                n += 1
                
        elif event.type == pygame.KEYUP:
            found = False
            n=0
            actions = list(self.keys.keys())
            while not found and n < len(actions):
                action = actions[n]
                if event.key == self.keys[action].key:
                    found = True
                    self.keys[action].set_keydown(False)
                n += 1
        
    def rand_shape(self):
        x = randint(0, 6)
        
        if x == 0:
            shape = Shape_I(self.grid)
        elif x == 1:
            shape = Shape_J(self.grid)
        elif x == 2:
            shape = Shape_L(self.grid)
        elif x == 3:
            shape = Shape_O(self.grid)
        elif x == 4:
            shape = Shape_S(self.grid)
        elif x == 5:
            shape = Shape_T(self.grid)
        elif x == 6:
            shape = Shape_Z(self.grid)
            
        return shape


if __name__ == '__main__':
    Window().run()
