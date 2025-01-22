import pygame


class Key:
    def __init__(self, key, rep_time=0, first_rep_time=0, repeat=True):
        self.key = key
        self.rep_time = rep_time
        self.first_rep_time = first_rep_time
        self.repeat = repeat
        self.keydown = False
        self.old_time = 0
        self.event_one_occur = False
        self.event_two_occur = False
        
    def keypress(self):
        """
        Returns:
        true if key is in active state, else false
        """
        state = False
        if self.keydown:
            if not self.event_one_occur:
                state = True
                self.event_one_occur = True
                self.old_time = pygame.time.get_ticks()
            elif not self.event_two_occur:
                if pygame.time.get_ticks() - self.old_time > self.first_rep_time:
                    self.old_time = pygame.time.get_ticks()
                    self.state = True
                    self.event_two_occur = True
            elif pygame.time.get_ticks() - self.old_time > self.rep_time:
                self.old_time = pygame.time.get_ticks()
                state = True
        return state
    
    def set_keydown(self, keydown):
        self.keydown = keydown
        self.event_one_occur = False
        self.event_two_occur = False