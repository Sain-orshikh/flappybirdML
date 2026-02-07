import random
import pygame
import config

class Player:
    
    def __init__(self):
        #Bird
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.velocity = 0
        self.flap = False
        self.alive = True
        #AI
        self.decision = None

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground.rect)
    
    def sky_collision(self):
        return bool(self.y <= 30)
    
    def pipe_collision(self):
        for p in config.pipes:
            if pygame.Rect.colliderect(self.rect, p.bottom_rect) or pygame.Rect.colliderect(self.rect, p.top_rect):
                return True
        return False
        
    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            #Gravity
            self.velocity +=0.25
            self.y += self.velocity
            self.rect.y = int(self.y)
            if self.velocity > 5:
                self.velocity = 5
        else:
            self.alive = False
            self.flap = False
            self.velocity = 0

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.velocity = -5
        if self.velocity >= 3:
            self.flap = False

    #AI related function

    def think(self):
        self.decision = random.uniform(0, 1)
        if self.decision > 0.73:
            self.bird_flap()