import pygame


class Util:
    def text_vertical(font:pygame.font.Font, text:str, antialias, color, background=None) -> pygame.Surface:
        '''
        Create a pygame.Surface object with the text diplayed verticaly

        Returns:
        pygame.Surface  
        '''
        surface = pygame.Surface([0,0])
        for c in text:
            char_surface = font.render(c, antialias, color, background)
            surface_hold = surface
            surface = pygame.Surface([max(surface_hold.get_width(), char_surface.get_width()),
                                      surface_hold.get_height() + char_surface.get_height()])
            surface.blit(surface_hold, [0,0])
            surface.blit(char_surface, [0,surface_hold.get_height()])
        
        return surface
    
    
        
            
            