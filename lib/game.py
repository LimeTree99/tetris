import pygame
from random import randint
from lib import Key, Grid
from lib.shape import *


class Game:
    class Game:
        TICK = pygame.USEREVENT + 1
        def __init__(self, display, exit_func):
            self.display = display
            self.exit_func = exit_func
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
            self.score = Game.Score(self.display)
            self.next_block = Game.Next_block(self.display, [575,35], self.rand_shape())
            
            self.shape = None
            self.start()
            
        def start(self):
            self.active = True
            self.grid.clear()
            self.score.set(0)
            self.shape = self.rand_shape()
            self.shape.add_to_grid(self.grid)
            self.score.set(0)
            pygame.time.set_timer(Game.Game.TICK, self.tick_speed)
            
        def tick(self):
            if self.active:
                if (self.shape.can_advance(0, 1)):
                    self.shape.advance(0, 1)
                else:
                    #hit end create new shape
                    for row in self.grid.find_full_rows():
                        self.grid.remove_row(row)
                        self.score.add(100)
                        
                    self.shape = self.next_block.replace(self.rand_shape())
                    if self.grid.range_is_free(self.shape.get_vectors()):
                        self.shape.add_to_grid(self.grid)
                    else:
                        self.active = False
                    
        
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
                # fixes a bug but i don't like this solution
                if self.active:
                    self.score.add(1)
            elif self.keys['hard_drop'].keypress():
                distance = self.shape.hard_drop()
                self.score.add(distance)
                self.tick()
            elif self.keys['pause'].keypress():
                self.exit_func()
                
            
            
        def draw(self):
            self.grid.draw()
            self.score.draw()
            self.next_block.draw()
        
        def event_handle(self, event):
            if event.type == Game.Game.TICK:
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
                        
            return shape


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
            pygame.draw.rect(self.surface, color.white, [0,0,200,50], width=1)
            font = self.font.render(str(self.score), True, color.white)
            self.surface.blit(font, [7,7])
        
        def add(self, amount):
            self.score += amount
            self.create_surface()
        
        def set(self, amount):
            self.score = amount
            self.create_surface()
                

    class Next_block:
        def __init__(self, display, pos, shape):
            self.display = display
            self.pos = pos
            self.grid = Grid(self.display, 2, 4, [pos[0]+25, pos[1]+25], 25,25)
            self.shape = shape
            self.shape.add_to_display(self.grid)
            
        def draw(self):
            pygame.draw.rect(self.display, color.white, [self.pos[0],self.pos[1],150,100], width=1)
            self.grid.draw()
        
        def replace(self, shape:Shape) -> Shape:
            """
            Replace current shape with new shape
            
            Param:
            shape (Shape)   The replacement
            Returns:
            Shape   old shape 
            """
            hold = self.shape
            self.shape = shape
            self.grid.clear()
            self.shape.add_to_display(self.grid)
            return hold
        
        