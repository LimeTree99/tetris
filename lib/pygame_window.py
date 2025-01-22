import pygame
import os


class main:
    def __init__(self,
                 width,
                 height,
                 window_name,
                 corner_image = os.path.split(__file__)[0] + '/images/flower_corner_image.png',
                 framerate = 60):
        
        self.width = width
        self.height = height
        self.framerate = framerate
        self.end = False
        self.background_on = True
        self.background_colour = (255,255,255)
        self.events = 0
        
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
