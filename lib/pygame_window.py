import pygame
import os


class main:
    def __init__(self,
                 width,
                 height,
                 window_name,
                 corner_image = 'assets/images/flower_corner_image.png',
                 framerate = 60):
        
        self.width = width
        self.height = height
        self.framerate = framerate
        self.end = False
        self.background_on = True
        self.background_colour = (255,255,255)
        self.events = 0
        self.keys = {}
        
        pygame.init()
        self.display = pygame.display.set_mode((self.width,self.height),pygame.RESIZABLE)
        pygame.display.set_caption(window_name)
        icon = pygame.image.load(corner_image)
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        
        

    def update(self):
        pass
    
    def draw(self):
        pass
    
    def event_handle(self, event):
        pass
        
    def run(self):
        while not self.end:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.end = True
                    
                if event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.w, event.h
                    self.display = pygame.display.set_mode((self.width, self.height),
                                                           pygame.RESIZABLE)   
                
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
                                 
                self.event_handle(event)
                
            if self.background_on:
                self.display.fill(self.background_colour)

            self.update()
            self.draw()
            
            pygame.display.update()
            
            self.clock.tick(self.framerate)
        pygame.quit()




if __name__ == '__main__':
    
    game = main(800, 500, 'Working Title')
    game.run()
