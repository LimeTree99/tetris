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
        self.surface = None
        self.pos = pos
        self.action = action
        self.kargs = {
            'text':'',
            'font':'assets/fonts/Helvetica.ttf',
            'font_size':10,
            'bg':color.black,
            'bg_active':color.blue,
            'bd':None,
            'bd_active':None,
            'font_color':color.gray,
            'font_color_active':color.light_gray,
            'center_on':'c'
        }
        self.kargs.update(kargs)
        
        self.font = pygame.font.Font(self.kargs['font'], self.kargs['font_size'])
        
    def update(self):
        self.surface = self.font_title.render(self.kargs['text'], True, self.kargs['font_color'], self.kargs['bg'])
        self.surface.blit(self.surface, [10,10])
    
    def draw(self):
        self.display.blit(self.surface, self.pos)
    
class Menu:
    def __init__(self, display):
        self.display = display
        self.font_title = pygame.font.Font('assets/fonts/Helvetica.ttf', 80)
        self.keys = {}
        self.buttons = [Button(self.display, [10,10], print('hi'), text='hi')]
        
    def update(self):
        pass
    
    def draw(self):
        pygame.draw.rect(self.display, (0,100,100), [110,10,580,580])
        title = self.font_title.render("Tetris", True, color.white)
        self.display.blit(title, [(self.display.get_width() - title.get_width()) / 2, 30])
        
    def event_handle(self, event):
        pass

class Window(pygame_window.main):
    def __init__(self):
        super().__init__(800, 600, 'TETRIS', corner_image='assets/images/icon.png')
        pygame.font.init()
        self.background_colour = color.black
        
        self.window_i = 0
        self.windows = [Game.Game(self.display), Menu(self.display)]
        
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
