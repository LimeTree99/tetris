import pygame, pickle
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
            self.tick_speed = 1000
            self.level = 1
            self.lines = 0
            
            self.key_rep = 50
            self.first_key_rep = 200
            self.can_hold = True
            self.rand_bag = []
            
            self.keys = {'move_left':Key(pygame.K_LEFT, self.key_rep, self.first_key_rep),
                        'move_right':Key(pygame.K_RIGHT, self.key_rep, self.first_key_rep),
                        'rotate_right':Key(pygame.K_UP,float('inf'),float('inf')),
                        'rotate_left':Key(pygame.K_z,float('inf'),float('inf')),
                        'soft_drop':Key(pygame.K_DOWN,self.key_rep, self.key_rep),
                        'hard_drop':Key(pygame.K_SPACE,float('inf'),float('inf')),
                        'hold':Key(pygame.K_c,float('inf'),float('inf')),
                        'pause':Key(pygame.K_ESCAPE,float('inf'),float('inf'))}
            
            self.grid = Grid(self.display, 20, 10, (280,20), 25, 25)
            self.score = Game.Score(self.display)
            self.next_block = Game.Block_display(self.display, [575,35], self.rand_shape(), label='Next')
            self.hold_block = Game.Block_display(self.display, [80,35], label='Hold')
            
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
            
        def save_score(self):
            try:
                fh = open('.save.d', 'rb')
                score_list = pickle.load(fh)
                fh.close()
                score_list.append(self.score.get_score())
                if self.score.get_score() > score_list[0]:
                    score_list.insert(0, self.score.get_score())
                
            except:
                score_list = [self.score.get_score()]
                
            fh = open('.save.d', 'wb')
            pickle.dump(score_list, fh)
            fh.close()
            
        def new_shape(self):
            self.shape = self.next_block.replace(self.rand_shape())
            self.can_hold = True
            if self.grid.range_is_free(self.shape.get_vectors()):
                self.shape.add_to_grid(self.grid)
            else:
                self.shape.add_to_grid(self.grid)
                self.save_score()
                self.active = False
            
            
        def tick(self):
            if self.active:
                if (self.shape.can_advance(0, 1)):
                    self.shape.advance(0, 1)
                else:
                    #hit end create new shape
                    for row in self.grid.find_full_rows():
                        self.grid.remove_row(row)
                        self.score.add(100)
                        self.lines += 1
                        if self.lines % 10 == 0:
                            self.next_level()
                        
                    self.new_shape()
                    
        def next_level(self):
            
            if self.level != 20:
                self.level += 1
            print(f'level {self.level}')
            
            self.tick_speed = ((0.8-((self.level-1)*0.007))**(self.level-1)) * 1000 # taken from tetris wiki 
            pygame.time.set_timer(Game.Game.TICK, int(self.tick_speed))
        
        def update(self):
            if self.active:
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
                elif self.keys['hold'].keypress() and self.can_hold:
                    self.can_hold = False
                    self.grid.remove_shape(self.shape)
                    self.shape.reset()
                    self.shape = self.hold_block.replace(self.shape)
                    if self.shape == None:
                        self.shape = self.rand_shape()
                    self.shape.add_to_grid(self.grid)
                    
                    
            if self.keys['pause'].keypress():
                self.exit_func()
                
            
            
        def draw(self):
            self.grid.draw()
            self.score.draw()
            self.next_block.draw()
            self.hold_block.draw()
        
        def event_handle(self, event):
            if event.type == Game.Game.TICK:
                self.tick()
            
        def rand_shape(self):
            if len(self.rand_bag) == 0:
                self.rand_bag = [i for i in range(0,7)]
                            
            x = self.rand_bag.pop(randint(0, len(self.rand_bag)-1))
            
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
        def __init__(self, display, label=''):
            self.display = display
            self.font = pygame.font.Font('assets/fonts/texgyrecursor.otf', 40)
            self.score = 0
            self.surface = None
            self.create_surface()
            
        def draw(self):
            self.display.blit(self.surface, [50,470])
            
        def create_surface(self):
            self.surface = pygame.Surface([200, 50])
            pygame.draw.rect(self.surface, color.white, self.surface.get_rect(), width=1)
            font = self.font.render(str(self.score), True, color.white)
            self.surface.blit(font, [7,-1])
        
        def add(self, amount):
            self.score += amount
            self.create_surface()
        
        def set(self, amount):
            self.score = amount
            self.create_surface()
            
        def get_score(self):
            return self.score
                

    class Block_display:
        def __init__(self, display, pos, shape=None, label=''):
            self.display = display
            self.pos = pos
            self.shape = shape
            self.label = label
            self.grid = Grid(self.display, 2, 4, [pos[0]+25, pos[1]+25], 25,25)
            if self.shape != None:
                self.shape.add_to_display(self.grid)
                
            self.font = pygame.font.Font('assets/fonts/texgyrecursor.otf', 23)
            self.label_surface = self.font.render(self.label, True, color.white, color.black)
            
        def draw(self):
            pygame.draw.rect(self.display, color.white, [self.pos[0],self.pos[1],150,100], width=1)
            self.display.blit(self.label_surface, [self.pos[0]+45, self.pos[1]-15])
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
        
        