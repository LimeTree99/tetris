import pygame
from random import randint
from lib import color, pygame_window, Grid, Key
from lib.shape import *


"""
game design decitions:
    add score for droping blocks
        -only if they are droped all the way
        -1 point for each block droped through
        
todo short term:
    display something whan paused
    have a defeated screen 
    
todo long term:
    a menu screen 
    be able to adjust settings
    resizable to a smaller size 
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
        self.grid = Grid(self.display, 4, 8, [575,35], 25,25)
        self.shape = Shape_J()
        self.shape.add_to_display(self.grid)
        
    def draw(self):
        self.grid.draw()


    
class Game:
    TICK = pygame.USEREVENT + 1
    def __init__(self, display):
        self.display = display
        self.active = False
        self.tick_speed = 500
        
        self.key_rep = 50
        self.first_key_rep = 200
        
        self.keys = {'move_left':Key(pygame.K_LEFT, self.key_rep, self.first_key_rep),
                     'move_right':Key(pygame.K_RIGHT, self.key_rep, self.first_key_rep),
                     'rotate_right':Key(pygame.K_UP,float('inf'),float('inf')),
                     'rotate_left':Key(pygame.K_z,float('inf'),float('inf')),
                     'soft_drop':Key(pygame.K_DOWN,self.key_rep, self.key_rep),
                     'hard_drop':Key(pygame.K_SPACE,float('inf'),float('inf')),
                     'pause':Key(pygame.K_ESCAPE,float('inf'),float('inf'))}
        
        self.grid = Grid(self.display, 20, 10, (280,20), 25, 25)
        self.score = Score(self.display)
        self.next_block = Next_block(self.display)
        
        self.shape = None
        self.start()
        
    def start(self):
        self.active = True
        self.shape = self.rand_shape()
        self.shape.add_to_grid(self.grid)
        self.score.set(0)
        pygame.time.set_timer(Game.TICK, self.tick_speed)
        
    def tick(self):
        if self.active:
            if (self.shape.can_advance(0, 1)):
                self.shape.advance(0, 1)
            else:
                #hit end create new shape
                for row in self.grid.find_full_rows():
                    self.grid.remove_row(row)
                    self.score.add(100)
                    
                self.shape = self.rand_shape()
                
    
    def update(self):
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
            self.score.add(1)
        elif self.keys['hard_drop'].keypress():
            distance = self.shape.hard_drop()
            self.score.add(distance)
            self.tick()
        elif self.keys['pause'].keypress():
            if self.active:
                self.active = False
            else:
                self.active = True
        
        
    def draw(self):
        self.grid.draw()
        self.score.draw()
        self.next_block.draw()
    
    def event_handle(self, event):
        if event.type == Game.TICK:
            self.tick()
        
    def rand_shape(self):
        x = randint(0, 6)
        
        if x == 0:
            shape = Shape_I()
        elif x == 1:
            shape = Shape_J()
        elif x == 2:
            shape = Shape_L()
        elif x == 3:
            shape = Shape_O()
        elif x == 4:
            shape = Shape_S()
        elif x == 5:
            shape = Shape_T()
        elif x == 6:
            shape = Shape_Z()
            
        shape.add_to_grid(self.grid)            
        return shape


class Window(pygame_window.main):
    def __init__(self):
        super().__init__(800, 600, 'TETRIS')
        pygame.font.init()
        self.background_colour = color.black
        
        self.game = Game(self.display)
        self.keys = self.game.keys
        
    def update(self):
        super().update()
        self.game.update()
    
    def draw(self):
        super().draw()
        self.game.draw()
        
    def event_handle(self, event):
        super().event_handle(event)
        self.game.event_handle(event)

if __name__ == '__main__':
    Window().run()
