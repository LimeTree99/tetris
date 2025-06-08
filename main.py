import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # disables pygame welcome message
import pygame, pickle
from lib import color, pygame_window, Key, Game, Util


"""
game design decitions: According to tetris standard
    score (I am not implimenting T spins at this time)
        Single 	                100 * level
        Double 	                300 * level
        Triple 	                500 * level
        Tetris 	                800 * level 
        Back-to-Back tetris 	Tetris score × 1.5 (excluding soft drop and hard drop) 
        Combo 	                50 * combo count * level
        Soft drop 	            1 per cell
        Hard drop 	            2 per cell 
        
        
todo short term: 
    there may be a bug with saving the score, investigate
    change Shape.add_to_display(Grid) to Grid.add_to_display(Shape) it feels more logical
    moving left and right feel slugish, adjust key rep speeds 
    display a popup for double, tripple, etc.
    save score, level, lines cleared, game duration 
    
todo long term:
    be able to adjust settings
    make update and drawing algorithms not redo the whole thing every frame
    resizable to a smaller size (probably wont happen)
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
        '''
        Param:
        display     pygame.Surface
        actions     [[name(str), action(func)]]
        '''
        self.display = display
        self.font_title = pygame.font.Font('assets/fonts/texgyrecursor.otf', 100)
        self.font_credits = pygame.font.Font('assets/fonts/texgyrecursor.otf', 10)
        self.font_score = pygame.font.Font('assets/fonts/texgyrecursor.otf', 20)
        self.keys = {'up':Key(pygame.K_UP,float('inf'),float('inf')),
                     'down':Key(pygame.K_DOWN,float('inf'),float('inf')),
                     'select':Key(pygame.K_RETURN,float('inf'),float('inf'))}
        
        button_settings = {
            'padding_ns':0, 
            'padding_ew':10,
            'bd':color.white, 
            'bg':color.black,
            'font_color':color.white,
            'bd_active':color.white,
            'bg_active':color.black,
            'font_color_active':color.red_pale
        }
        self.button_select = 0
        self.buttons = []
        for i in range(len(actions)):
            self.buttons.append(Button(self.display, 
                                       [self.display.get_width()/2,150 + i * 100],
                                       text=actions[i][0], 
                                       action=actions[i][1],
                                       **button_settings),)
        
        self.buttons[0].active = True
        
        # load score
        try:
            fh = open('.save.d', 'rb')
            scores = pickle.load(fh)
            self.score_top = scores[0]
            self.score_last = scores[-1]
            fh.close()
        except:
            self.score_top = 0
            self.score_last = 0
        
    def update(self):
        if self.keys['up'].keypress():
            self.buttons[self.button_select].active = False
            self.button_select -= 1
            if self.button_select < 0:
                self.button_select = len(self.buttons)-1
            self.buttons[self.button_select].active = True
        if self.keys['down'].keypress():
            self.buttons[self.button_select].active = False
            self.button_select += 1
            if self.button_select >= len(self.buttons):
                self.button_select = 0
            self.buttons[self.button_select].active = True
        if self.keys['select'].keypress():
            self.buttons[self.button_select].press()
                
                
        for button in self.buttons:
            button.update()
    
    def draw(self):
        pygame.draw.rect(self.display, color.white, [110,10,580,580], width=1)
        title = self.font_title.render("Tetris", True, color.white)
        self.display.blit(title, [(self.display.get_width() - title.get_width()) / 2, 10])
        credits = self.font_credits.render("Ghost Flower", True, color.white)
        self.display.blit(credits, [610, 570])
        
        #scores
        top_0_buff = max(len(str(self.score_top)), len(str(self.score_last))) - len(str(self.score_top))
        last_0_buff = max(len(str(self.score_top)), len(str(self.score_last))) - len(str(self.score_last))
        
        top_score = Util.text_vertical(self.font_score, f'TOP {'0'*top_0_buff}{self.score_top}', True, color.white)
        self.display.blit(top_score, [130,165])
        top_score = Util.text_vertical(self.font_score, f'LST {'0'*last_0_buff}{self.score_last}', True, color.white)
        self.display.blit(top_score, [660,165])
        
        for button in self.buttons:
            button.draw()
            
    def event_handle(self, event):
        pass

class Window(pygame_window.main):
    def __init__(self):
        super().__init__(800, 600, 'TETRIS', corner_image='assets/images/icon.png')
        pygame.font.init()
        self.background_colour = color.black
        
        self.game = None
        
        
        
        self.menu = Menu(self.display, [['Continue', lambda:self.swap_window()],
                                        ['New Game', lambda:self.new_game()],
                                        ['Settings', lambda:print('Settings')],
                                        ['Quit', lambda:self.quit()]])
        self.keys = {}
        self.window_cur = ''
        self.windows = {'game':None, 'menu':None}
        self.new_game()
        self.new_menu()
        self.go_to('menu')
        
        
        
    
    def go_to(self, window:str):
        self.window_cur = window
        self.keys = self.windows[self.window_cur].keys
    
    def new_menu(self):
        self.windows['menu'] = self.menu = Menu(self.display, [['Continue', lambda:self.go_to('game')],
                                                               ['New Game', lambda:self.new_game()],
                                                               ['Settings', lambda:print('Settings')],
                                                               ['Quit', lambda:self.quit()]])
        self.menu.update()
        self.go_to('menu')
    
    def new_game(self):
            self.windows['game'] = Game.Game(self.display, lambda:self.new_menu())
            self.go_to('game')
        
    def update(self):
        super().update()
        self.windows[self.window_cur].update()
    
    def draw(self):
        super().draw()
        self.windows[self.window_cur].draw()
        
    def event_handle(self, event):
        super().event_handle(event)
        self.windows[self.window_cur].event_handle(event)
    
    def quit(self):
        super().quit()

if __name__ == '__main__':
    Window().run()
