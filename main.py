import pygame
from random import randint
from lib import color, pygame_window, Grid, Key, Game
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
        

class Button:
    def __init__(self, display, pos, action, **kargs):
        self.display = display
        self.surface_active = None
        self.surface_inactive = None
        self.suface = None
        self.pos = pos
        self.action = action
        self.active = False
        self.kargs = {
            'text':'',
            'font':'assets/fonts/texgyrecursor.otf',
            'font_size':40,
            'padding_ns':0,
            'padding_ew':0,
            'bg':color.black,
            'bg_active':color.blue,
            'bd':None,
            'bd_active':None,
            'font_color':color.white,
            'font_color_active':color.light_gray,
            'center_on':'c'
        }
        self.kargs.update(kargs)
        
        self.font = pygame.font.Font(self.kargs['font'], self.kargs['font_size'])
        
        # Create surfaces
        # active
        self.surface_active = self.font.render(self.kargs['text'], True, self.kargs['font_color_active'], self.kargs['bg_active'])
        padding = pygame.Surface([self.surface_active.get_width() + self.kargs['padding_ew'] * 2,
                                  self.surface_active.get_height() + self.kargs['padding_ns'] * 2])
        # the - 3 is because the font has a wierd space added above it 
        padding.blit(self.surface_active, [self.kargs['padding_ew'],self.kargs['padding_ns']-3])
        self.surface_active = padding 
        if self.kargs['bd_active'] != None:
            pygame.draw.rect(self.surface_active, self.kargs['bd_active'], self.surface_active.get_rect(), width=1)
        
        
        # inactive
        self.surface_inactive = self.font.render(self.kargs['text'], True, self.kargs['font_color'], self.kargs['bg'])
        padding = pygame.Surface([self.surface_inactive.get_width() + self.kargs['padding_ew'] * 2,
                                  self.surface_inactive.get_height() + self.kargs['padding_ns'] * 2])
        # the - 3 is because the font has a wierd space added above it 
        padding.blit(self.surface_inactive, [self.kargs['padding_ew'],self.kargs['padding_ns']-3])
        self.surface_inactive = padding 
        if self.kargs['bd'] != None:
            pygame.draw.rect(self.surface_inactive, self.kargs['bd'], self.surface_inactive.get_rect(), width=1)
        
    
    def set_arg(self, arg, value):
        self.kargs[arg] = value
    
    def get_arg(self, arg):
        return self.karg[arg]
    
    def press(self):
        self.action()
    
    def update(self):
        if self.active:
            self.surface = self.surface_active
        else:
            self.surface = self.surface_inactive
                
    def draw(self):
        if self.kargs['center_on'] == 'nw':
            self.display.blit(self.surface, self.pos)
        elif self.kargs['center_on'] == 'c':
            self.display.blit(self.surface, [self.pos[0] - self.surface.get_width() / 2, self.pos[1] + self.surface.get_height() / 2])
    
class Menu:
    def __init__(self, display, actions):
        self.display = display
        self.font_title = pygame.font.Font('assets/fonts/texgyrecursor.otf', 80)
        self.keys = {'up':Key(pygame.K_UP,float('inf'),float('inf')),
                     'down':Key(pygame.K_DOWN,float('inf'),float('inf')),
                     'select':Key(pygame.K_RETURN,float('inf'),float('inf'))}
        self.button_select = 0
        self.buttons = [
            Button(self.display, 
                   [self.display.get_width()/2,200], 
                   action=actions['new_game'], 
                   text='New Game', 
                   padding_ns=0, 
                   padding_ew=10,
                   bd=color.white, 
                   bg=color.black,
                   font_color=color.white,
                   bd_active=color.white,
                   bg_active=color.black,
                   font_color_active=color.red),
            Button(self.display, 
                   [self.display.get_width()/2,400], 
                   action=actions['quit'], 
                   text='Quit', 
                   padding_ns=0, 
                   padding_ew=10,
                   bd=color.white, 
                   bg=color.black,
                   font_color=color.white,
                   bd_active=color.white,
                   bg_active=color.black,
                   font_color_active=color.red)
        ]
        self.buttons[0].active = True
        
    def update(self):
        if self.keys['up'].keypress():
            self.buttons[self.button_select].active = False
            self.button_select += 1
            if self.button_select >= len(self.buttons):
                self.button_select = 0
            self.buttons[self.button_select].active = True
        if self.keys['down'].keypress():
            self.buttons[self.button_select].active = False
            self.button_select -= 1
            if self.button_select < 0:
                self.button_select = len(self.buttons)-1
            self.buttons[self.button_select].active = True
        if self.keys['select'].keypress():
            self.buttons[self.button_select].press()
                
                
        for button in self.buttons:
            button.update()
    
    def draw(self):
        pygame.draw.rect(self.display, color.white, [110,10,580,580], width=1)
        title = self.font_title.render("Tetris", True, color.white)
        self.display.blit(title, [(self.display.get_width() - title.get_width()) / 2, 30])
        for button in self.buttons:
            button.draw()
            
        
        
    def event_handle(self, event):
        pass

class Window(pygame_window.main):
    def __init__(self):
        super().__init__(800, 600, 'TETRIS', corner_image='assets/images/icon.png')
        pygame.font.init()
        self.background_colour = color.black
        
        self.window_i = 0
        self.windows = [Game.Game(self.display), Menu(self.display, {'new_game':lambda:self.swap_window(), 'quit':lambda:print('quit')})]
        
        self.keys = self.windows[self.window_i].keys
        
    def swap_window(self):
        self.window_i += 1
        if self.window_i >= len(self.windows):
            self.window_i = 0
        
    def update(self):
        super().update()
        self.windows[self.window_i].update()
    
    def draw(self):
        super().draw()
        self.windows[self.window_i].draw()
        
    def event_handle(self, event):
        super().event_handle(event)
        self.windows[self.window_i].event_handle(event)

if __name__ == '__main__':
    Window().run()
