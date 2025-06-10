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
            
            self.key_rep = 40
            self.first_key_rep = 130
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
                    lines = 0
                    for row in self.grid.find_full_rows():
                        self.grid.remove_row(row)
                        lines += 1
                        
                    if lines == 0:
                        self.score.reset_combo()
                    else:
                        self.score.lines_cleared += lines
                        self.score.add_lines(lines)
                        if self.score.next_level():
                            self.next_level()
                        
                    self.new_shape()
                    
        def next_level(self):            
            self.tick_speed = ((0.8-((self.score.level-1)*0.007))**(self.score.level-1)) * 1000 # taken from tetris wiki 
            pygame.time.set_timer(Game.Game.TICK, int(self.tick_speed))
        
        def update(self):
            if self.active:
                self.score.update()
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
                    self.score.add_score(1)
                elif self.keys['hard_drop'].keypress():
                    distance = self.shape.hard_drop()
                    self.score.add_score(distance * 2)
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
        def __init__(self, display):
            self.display = display
            self.font_numbers = pygame.font.Font('assets/fonts/texgyrecursor.otf', 40)
            self.font_labels = pygame.font.Font('assets/fonts/texgyrecursor.otf', 23)
            self.score = 0
            self.level = 1
            self.level_cap = 20
            self.lines_cleared = 0
            self.combo_count = -1
            self.last_tetris = False
            self.new_level = True
            self.surface = None
            
            self.popup = Game.Popup(self.display, [560, 450], 1000)
            
            self.create_surface()
            
        def draw(self):
            self.display.blit(self.surface, [50,300])
            self.popup.draw()
            
        def update(self):
            self.popup.update()
            
        def create_surface(self):
            score_surface = pygame.Surface([200, 80])
            pygame.draw.rect(score_surface, color.white, [0,30,200,50], width=1)
            score_num = self.font_numbers.render(str(self.score), True, color.white)
            score_surface.blit(score_num, [7,26])
            score_label = self.font_labels.render('Score', True, color.white)
            score_surface.blit(score_label, [60,0])
            
            level_surface = pygame.Surface([200, 80])
            pygame.draw.rect(level_surface, color.white, [0,30,200,50], width=1)
            score_num = self.font_numbers.render(str(self.level), True, color.white)
            level_surface.blit(score_num, [7,26])
            score_label = self.font_labels.render('Level', True, color.white)
            level_surface.blit(score_label, [60,0])
            
            lines_surface = pygame.Surface([200, 80])
            pygame.draw.rect(lines_surface, color.white, [0,30,200,50], width=1)
            score_num = self.font_numbers.render(str(self.lines_cleared), True, color.white)
            lines_surface.blit(score_num, [7,26])
            score_label = self.font_labels.render('Lines', True, color.white)
            lines_surface.blit(score_label, [60,0])
            
            self.surface = pygame.Surface([200, 240])
            self.surface.blit(score_surface, [0,0])
            self.surface.blit(level_surface, [0,80])
            self.surface.blit(lines_surface, [0,160])
        
        def reset_combo(self):
            self.combo_count = -1
            self.last_tetris = False
            self.new_level = False
            
        def add_lines(self, lines):
            add = 0
            if lines == 1:
                add = 100 * self.level
                self.popup.message(f'Single {add}')
            elif lines == 2:
                add = 300 * self.level
                self.popup.message(f'Double {add}')
            elif lines == 3:
                add = 500 * self.level
                self.popup.message(f'Triple {add}')
            elif lines == 4:
                if self.last_tetris:
                    add = int(800 * self.level * 1.5)
                    self.popup.message(f'Tetris Run {add}')
                else:
                    add = 800 * self.level
                    self.last_tetris = True
                    self.popup.message(f'Tetris {add}')
            
            self.combo_count += 1
            if self.combo_count > 0:
                add += 50 * self.combo_count * self.level
                self.popup.message(f'Combo {add}')
            
            old_level = self.level
            self.level = self.lines_cleared // 10 + 1
            if self.level > self.level_cap:
                self.level = self.level_cap
                
            if old_level != self.level:
                self.new_level = True
                
            self.score += add
                
            self.create_surface()
                
        
        def add_score(self, amount):
            self.score += amount
            self.create_surface()
        
        def set(self, amount):
            self.score = amount
            self.create_surface()
            
        def next_level(self):
            return self.new_level
            
        def get_score(self):
            return self.score
        
    class Popup:
        def __init__(self, display, pos, display_time):
            self.display = display
            self.pos = pos
            self.display_time = display_time
            self.on_time = 0
            
            self.font = pygame.font.Font('assets/fonts/texgyrecursor.otf', 17)
            self.surface = None
            self.text = ''
            self.active = False
        
        def message(self, text):
            self.text = text
            self.surface = self.font.render(self.text, True, color.white)
            self.active = True
            self.on_time = pygame.time.get_ticks()
            
        def update(self):
            if self.active:
                if self.on_time + self.display_time < pygame.time.get_ticks():
                    self.active = False
        
        def draw(self):
            if self.active:
                self.display.blit(self.surface, self.pos)
                

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
        
        